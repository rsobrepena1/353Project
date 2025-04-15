#NOTE: Drop the address & user_account tables before running this script
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import Numeric
from sqlalchemy import DateTime
from datetime import datetime

username = "postgres"
password = "csclassluc"
#DB Connection: create_engine(DBMS_name+driver://<username>:<password>@<hostname>/<database_name>)
engine = create_engine("postgresql+psycopg2://" + username + ":" + password +"@localhost/postgres")

#Define Classes/Tables
class Base(DeclarativeBase):
    pass

#Rumyr/Erick/Alexis
class EMT(Base):
    __tablename__ = "emt"

    eID: Mapped[int] = mapped_column(Integer, primary_key=True)
    eName: Mapped[str] = mapped_column(String(30))
    eLOC: Mapped[int] = mapped_column(Integer)
    eWage: Mapped[float] = mapped_column(Numeric(5, 2))
    coned_modules: Mapped[List["ConEd"]] = relationship(
        back_populates="emt", cascade="all, delete-orphan"
    )

    transported_pID: Mapped[int] = mapped_column(Integer, ForeignKey("patient.pID"), nullable=True)
    bPressure: Mapped[float] = mapped_column(Numeric(5,1), nullable=False)
    pPulse: Mapped[int] = mapped_column(Integer, nullable=False)
    oLevel: Mapped[float] = mapped_column(Numeric(5,1), nullable=False)

    patient: Mapped[List["Patient"]] = relationship(
        back_populates="emt", cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"EMT(id={self.eID!r}, eName={self.eName!r}), transported_pID={self.transported_pID},"
        f"bPressure={self.bPressure}, pPulse={self.pPulse}, oLevel={self.oLevel})"

#Rumyr
class ConEd(Base):
    __tablename__ = "coned"
  
    mID: Mapped[int] = mapped_column(Integer, primary_key=True)
    mName: Mapped[str] = mapped_column(String(50))
    mDate: Mapped[datetime] = mapped_column(DateTime)
    cDate: Mapped[datetime] = mapped_column(DateTime)
    eID: Mapped[int] = mapped_column(ForeignKey("emt.eID"))
    emt: Mapped["EMT"] = relationship(back_populates="coned_modules")
    def __repr__(self) -> str:
        return f"ConEd(id={self.mID!r}, mName={self.mName!r}, cDate={self.cDate!r}, eID={self.eID!r})"

#Ethan
class Dispatch(Base):
    __tablename__ = 'dispatch'

    dID: Mapped[int] = mapped_column(primary_key=True)
    dName: Mapped[str] = mapped_column(String, nullable=False)
    dWage: Mapped[Numeric] = mapped_column(Numeric, nullable=False)

    facilities: Mapped[list["Facility"]] = relationship("Facility", back_populates="dispatch")
#Ethan
class Facility(Base):
    __tablename__ = 'facility'

    fID: Mapped[int] = mapped_column(primary_key=True)
    fName: Mapped[str] = mapped_column(String, nullable=False)
    fAddress: Mapped[str] = mapped_column(String, nullable=False)
    fNumber: Mapped[int] = mapped_column(Integer, nullable=False)

    dID: Mapped[int] = mapped_column(ForeignKey("dispatch.dID"))
    dispatch: Mapped[Dispatch] = relationship("Dispatch", back_populates="facilities")

#Alexis 
class Ambulance(Base):
    __tablename__ = "ambulance"
   
    rNumber: Mapped[int] = mapped_column(Integer, primary_key=True)  #Primary Key
    lCheck: Mapped[str] = mapped_column(DateTime, nullable=False)  
    mAge: Mapped[int] = mapped_column(Integer, nullable=False)  
    equipment: Mapped[str] = mapped_column(String(100), nullable=False) 
    emt: Mapped[List["EMT"]] = relationship(back_populates="ambulance", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"Ambulance(rNumber={self.rNumber!r}, equipment={self.equipment!r}, lCheck={self.lCheck!r}, mAge={self.mAge!r})"

#Erick
class Patient(Base):
    __tablename__ = "patient"

    #Attributes
    pID: Mapped[int] = mapped_column(Integer, primary_key=True)
    pName: Mapped[str] = mapped_column(String(40))
    pBirthDate: Mapped[datetime] = mapped_column(DateTime)
    pAddress: Mapped[str] = mapped_column(String(100))
    pNumber: Mapped[str] = mapped_column(String(50))

    #Connection
    eID: Mapped[int] = mapped_column(Integer, ForeignKey("emt.eID"))
    emt: Mapped["EMT"] = relationship(back_populates="patient")
    
    def __repr__(self) -> str:
        return f"Patient(pID={self.pID!r}, pName={self.pName!r})"

# Create tables
Base.metadata.create_all(engine)

# Insert Data
with Session(engine) as session:
#Rumyr
    emts = [
        EMT(eID=1, eLOC=2, eName='Regan, Bracken', eWage=30.15),
        EMT(eID=2, eLOC=1, eName='Park, Grant', eWage=42.00),
        EMT(eID=3, eLOC=3, eName='Rogers, Steve', eWage=35.50),
        EMT(eID=4, eLOC=2, eName='Stark, Tony', eWage=50.00),
        EMT(eID=5, eLOC=1, eName='Romanoff, Natasha', eWage=45.00),
        EMT(eID=6, eLOC=3, eName='Banner, Bruce', eWage=40.75),
        EMT(eID=7, eLOC=2, eName='Odinson, Thor', eWage=60.00),
        EMT(eID=8, eLOC=1, eName='Barton, Clint', eWage=38.25),
        EMT(eID=9, eLOC=2, eName='Parker, Peter', eWage=30.00),
        EMT(eID=10, eLOC=3, eName='Maximoff, Wanda', eWage=42.43),
        EMT(eID=11, eLOC=2, eName='Strange, Doctor', eWage=32.00),
        EMT(eID=12, eLOC=1, eName='TChalla, King', eWage=24.00),
        EMT(eID=13, eLOC=3, eName='Danvers, Carol', eWage=30.00),
        EMT(eID=14, eLOC=3, eName='Jerry, Tom', eWage=28.75),
        EMT(eID=15, eLOC=1, eName='Barnes, Bucky', eWage=36.50),
        EMT(eID=16, eLOC=3, eName='Wilson, Sam', eWage=40.50),
        EMT(eID=17, eLOC=3, eName='Carter, Peggy', eWage=38.00)
        ]
    #Rumyr
    modules = [
        ConEd(mID=1, mName='Stroke Care', mDate=datetime(2025, 3, 21), cDate=datetime(2025, 3, 21), eID=1),
        ConEd(mID=2, mName='Respiratory Issues', mDate=datetime(2025, 3, 22), cDate=datetime(2025, 3, 22), eID=2),
        ConEd(mID=3, mName='Cardiac Problems', mDate=datetime(2025, 3, 23), cDate=datetime(2025, 3, 23), eID=3),
        ConEd(mID=4, mName='Psychiatric Safety', mDate=datetime(2025, 3, 24), cDate=datetime(2025, 3, 24), eID=4),
        ConEd(mID=5, mName='Trauma Care', mDate=datetime(2025, 3, 25), cDate=datetime(2025, 3, 25), eID=5),
        ConEd(mID=6, mName='Motor Vehicle Collisions', mDate=datetime(2025, 3, 26), cDate=datetime(2025, 3, 26), eID=6),
        ConEd(mID=7, mName='Dementia', mDate=datetime(2025, 3, 27), cDate=datetime(2025, 3, 27), eID=7),
        ConEd(mID=8, mName='Work Safety', mDate=datetime(2025, 3, 28), cDate=datetime(2025, 3, 28), eID=8),
        ConEd(mID=9, mName='Obstetrics', mDate=datetime(2025, 3, 29), cDate=datetime(2025, 3, 29), eID=9),
        ConEd(mID=10, mName='Stroke Care', mDate=datetime(2025, 3, 21), cDate=datetime(2025, 3, 21), eID=10),
        ConEd(mID=11, mName='Respiratory Issues', mDate=datetime(2025, 3, 22), cDate=datetime(2025, 3, 22), eID=11),
        ConEd(mID=12, mName='Cardiac Problems', mDate=datetime(2025, 3, 23), cDate=datetime(2025, 3, 23), eID=12),
        ConEd(mID=13, mName='Psychiatric Safety', mDate=datetime(2025, 3, 24), cDate=datetime(2025, 3, 24), eID=13)
    ]
    #Ethan
    dispatchers = [
        Dispatch(dID=1, dName='Claus, Santa', dWage=30.00),
        Dispatch(dID=2, dName='Frost, Jack', dWage=28.50),
        Dispatch(dID=3, dName='Iverson, Allen', dWage=26.90),
        Dispatch(dID=4, dName='Bees, Apple', dWage=24.50),
        Dispatch(dID=5, dName='Doe, John', dWage=27.00),
        Dispatch(dID=6, dName='Smith, Terry', dWage=28.00),
        Dispatch(dID=7, dName='Black, Jack', dWage=29.00),
        Dispatch(dID=8, dName='Man, Iron', dWage=32.00)
    ]
    #Ethan
    facilities = [
        Facility(fName='North Hospital', fAddress='123 Smith St', fNumber=101, dID=1),
        Facility(fName='East Ambulance Service', fAddress='456 State Ave', fNumber=102, dID=1),
        Facility(fName='East Ambulance Service', fAddress='456 State Ave', fNumber=102, dID=2),
        Facility(fName='West Fire Department', fAddress='135 W Brown Ave', fNumber=104, dID=2),
        Facility(fName='South Response Station', fAddress='789 Tree Rd', fNumber=103, dID=3),
        Facility(fName='West Fire Department', fAddress='135 W Brown Ave', fNumber=104, dID=4),
        Facility(fName='Central Care Center', fAddress='246 Main St', fNumber=105, dID=5)
    ]

    #Erick
    patients = [
        Patient(pID=1, pName='John Doe', pBirthDate=datetime(1985, 7, 12), pAddress='123 Maple St, Springfield, IL', pNumber='555-1234'),
        Patient(pID=2, pName='Jane Smith', pBirthDate=datetime(1990, 3, 25), pAddress='456 Oak St, Denver, CO', pNumber='555-5678'),
        Patient(pID=3, pName='Michael Johnson', pBirthDate=datetime(1978, 9, 14), pAddress='789 Pine St, Austin, TX', pNumber='555-9012'),
        Patient(pID=4, pName='Emily Davis', pBirthDate=datetime(2000, 11, 30), pAddress='321 Birch St, Seattle, WA', pNumber='555-3456'),
        Patient(pID=5, pName='Daniel Brown', pBirthDate=datetime(1965, 5, 20), pAddress='654 Cedar St, Miami, FL', pNumber='555-7890'),
        Patient(pID=6, pName='Jessica Wilson', pBirthDate=datetime(1989, 8, 8), pAddress='987 Willow St, Boston, MA', pNumber='555-2345'),
        Patient(pID=7, pName='Matthew Martinez', pBirthDate=datetime(1995, 6, 15), pAddress='159 Elm St, Phoenix, AZ', pNumber='555-6789'),
        Patient(pID=8, pName='Sarah Taylor', pBirthDate=datetime(1972, 12, 5), pAddress='753 Fir St, Chicago, IL', pNumber='555-0123'),
        Patient(pID=9, pName='Christopher Anderson', pBirthDate=datetime(1983, 4, 22), pAddress='852 Redwood St, Portland, OR', pNumber='555-4567'),
        Patient(pID=10, pName='Amanda Thomas', pBirthDate=datetime(1998, 2, 10), pAddress='369 Spruce St, Dallas, TX', pNumber='555-8901'),
        Patient(pID=11, pName='Joshua White', pBirthDate=datetime(1976, 10, 17), pAddress='147 Cypress St, Atlanta, GA', pNumber='555-2346'),
        Patient(pID=12, pName='Olivia Harris', pBirthDate=datetime(1992, 7, 29), pAddress='258 Magnolia St, San Francisco, CA', pNumber='555-6780'),
        Patient(pID=13, pName='Jose Sanchez', pBirthDate=datetime(2002, 6, 19), pAddress='4128 Mulberry Lane, Springfield, IL 62704', pNumber='435-7781'),
        Patient(pID=14, pName='Maria Lopez', pBirthDate=datetime(1998, 11, 25), pAddress='720 Oak Street, Denver, CO 80203', pNumber='555-9821'),
        Patient(pID=15, pName='Juan Martinez', pBirthDate=datetime(2000, 7, 20), pAddress='20 Cooper Square, New York, NY', pNumber='542-5397'),
        Patient(pID=16, pName='Ethan Miller', pBirthDate=datetime(1985, 7, 12), pAddress='123 Maple St, Springfield, IL', pNumber='555-1234'),
        Patient(pID=17, pName='Lily Roberts', pBirthDate=datetime(1990, 3, 25), pAddress='456 Oak St, Denver, CO', pNumber='555-5678')
    ]


    session.add_all(emts + modules + dispatchers + facilities + patients)
    session.commit()


with Session(engine) as session:
#Query: Module Completion and EMTs (Rumyr)
    stmt = (
        select(EMT.eName, ConEd.mName, ConEd.cDate)
        .join(ConEd)
    )
    results = session.execute(stmt).all()

    for eName, mName, cDate in results:
        print(f"EMT: {eName}, Module: {mName}, Completion Date: {cDate}")

# Query: DispatcherAndFacility (Ethan)
    with Session() as session:
    stmt = (
        select(Dispatch.dName, Facility.fName, Facility.fAddress)
        .join(Facility)
    )
    results = session.execute(stmt).all()

    for dName, fName, fAddress in results:
        print(f"Dispatcher: {dName}, Facility: {fName}, Address: {fAddress}")


    #Query TrainingPay - Alexis Fenderson
     stmt = (
    select(EMT.eID, EMT.eName,
        func.count(ConEd.mID).label("Courses Completed"),
        ConEd.mName.label("Recent Course"),
        EMT.eWage.label("Wages")
    )
        .join(ConEd, EMT.eID == ConEd.eID) 
        .group_by(EMT.eID, EMT.eName, EMT.eWage, ConEd.mName)
        .order_by(func.count(ConEd.mID).desc())  

    )

        results = session.execute(stmt).all()

        for row in results:
        print(row)

# Query for Finding Highest LOC Patients and the EMT's who treated them | EMT Wages
with Session(engine) as session:
    max_eLOC = session.execute(select(func.max(EMT.eLOC))).scalar()

    join_query = session.execute(
        select(EMT.eName, Patient.pName, EMT.eWage, EMT.eID)
        .join(EMT.patient)
        .where(EMT.eLOC == max_eLOC)
    )

    print("Format: [eName, pName, eWage, eID]\n ----------------------------")
    for join in join_query:
        print(f"{join}")
"""

Erick Version

class Patient(Base):
    __tablename__ = "patient"
    
    #Patient Information
    pID: Mapped[int] = mapped_column(Integer, primary_key=True)
    pName: Mapped[str] = mapped_column(String(40))
    pBirthDate: Mapped[datetime] = mapped_column(DateTime)
    pAddress: Mapped[str] = mapped_column(String(100))
    pNumber: Mapped[str] = mapped_column(String(50))
    #relation, 1-n for patients
    emts: Mapped[List["EMT"]] = relationship(back_populates="patient")

class EMT(Base):
    __tablename__ = "emt"
    
    # EMT attributes
    eID: Mapped[int] = mapped_column(Integer, primary_key=True)
    eName: Mapped[str] = mapped_column(String(30))
    eLOC: Mapped[int] = mapped_column(Integer)
    eWage: Mapped[float] = mapped_column(Numeric(5,2))
    #pID is an fk considering we extended EMT
    pID: Mapped[int] = mapped_column(Integer, ForeignKey("patient.pID"))
    
    # transportedBy attributes
    bPressure: Mapped[float] = mapped_column(Numeric)
    pPulse: Mapped[float] = mapped_column(Numeric)
    oLevel: Mapped[float] = mapped_column(Numeric)
    #the connection back to emt
    patient: Mapped["Patient"] = relationship(back_populates="emts")

# Create tables
Base.metadata.create_all(engine)

    
    emts = [
        EMT(eID=1, eLOC=2, eName='Regan, Bracken', eWage=30.15, pID=1, bPressure=120.0, pPulse=72.0, oLevel=98.0),
        EMT(eID=2, eLOC=1, eName='Park, Grant', eWage=42.00, pID=2, bPressure=118.0, pPulse=75.0, oLevel=97.0),
        EMT(eID=3, eLOC=3, eName='Rogers, Steve', eWage=35.50, pID=3, bPressure=115.0, pPulse=80.0, oLevel=96.0),
        EMT(eID=4, eLOC=2, eName='Stark, Tony', eWage=50.00, pID=4, bPressure=130.0, pPulse=65.0, oLevel=99.0),
        EMT(eID=5, eLOC=1, eName='Romanoff, Natasha', eWage=45.00, pID=5, bPressure=125.0, pPulse=70.0, oLevel=97.0),
        EMT(eID=6, eLOC=3, eName='Banner, Bruce', eWage=40.75, pID=6, bPressure=140.0, pPulse=90.0, oLevel=95.0),
        EMT(eID=7, eLOC=2, eName='Odinson, Thor', eWage=60.00, pID=7, bPressure=135.0, pPulse=85.0, oLevel=94.0),
        EMT(eID=8, eLOC=1, eName='Barton, Clint', eWage=38.25, pID=8, bPressure=128.0, pPulse=78.0, oLevel=96.0),
        EMT(eID=9, eLOC=2, eName='Parker, Peter', eWage=30.00, pID=9, bPressure=122.0, pPulse=82.0, oLevel=98.0),
        EMT(eID=10, eLOC=3, eName='Maximoff, Wanda', eWage=42.43, pID=10, bPressure=119.0, pPulse=76.0, oLevel=97.0),
        EMT(eID=11, eLOC=2, eName='Strange, Doctor', eWage=32.00, pID=11, bPressure=132.0, pPulse=72.0, oLevel=96.0),
        EMT(eID=12, eLOC=1, eName='TChalla, King', eWage=24.00, pID=12, bPressure=126.0, pPulse=74.0, oLevel=98.0),
        EMT(eID=13, eLOC=3, eName='Danvers, Carol', eWage=30.00, pID=13, bPressure=124.0, pPulse=68.0, oLevel=97.0),
        EMT(eID=14, eLOC=3, eName='Jerry, Tom', eWage=28.75, pID=14, bPressure=118.0, pPulse=80.0, oLevel=96.0),
        EMT(eID=15, eLOC=1, eName='Barnes, Bucky', eWage=36.50, pID=15, bPressure=130.0, pPulse=75.0, oLevel=95.0),
        EMT(eID=16, eLOC=3, eName='Wilson, Sam', eWage=40.50, pID=16, bPressure=128.0, pPulse=78.0, oLevel=97.0),
        EMT(eID=17, eLOC=3, eName='Carter, Peggy', eWage=38.00, pID=17, bPressure=122.0, pPulse=82.0, oLevel=98.0)
    ]
    session.add_all(emts)
    session.commit()
"""
