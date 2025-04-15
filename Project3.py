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
from sqlalchemy import Date
from datetime import date

username = "postgres"
password = "csclassluc"
#DB Connection: create_engine(DBMS_name+driver://<username>:<password>@<hostname>/<database_name>)
engine = create_engine("postgresql+psycopg2://" + username + ":" + password +"@localhost/postgres")

#Define Classes/Tables
class Base(DeclarativeBase):
    pass

#Rumyr/Erick
class EMT(Base):
    __tablename__ = "emt"

    eID: Mapped[int] = mapped_column(Integer, primary_key=True)
    eName: Mapped[str] = mapped_column(String(30))
    eLOC: Mapped[int] = mapped_column(Integer)
    eWage: Mapped[float] = mapped_column(Numeric(5, 2))
    coned_modules: Mapped[List["ConEd"]] = relationship(
        back_populates="emt", cascade="all, delete-orphan"
    )
    patient: Mapped[List["Patient"]] = relationship(
        back_populates="emt", cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"EMT(id={self.eID!r}, eName={self.eName!r})"

#Rumyr
class ConEd(Base):
    __tablename__ = "coned"
  
    mID: Mapped[int] = mapped_column(Integer, primary_key=True)
    mName: Mapped[str] = mapped_column(String(50))
    mDate: Mapped[Date] = mapped_column(Date)
    cDate: Mapped[Date] = mapped_column(Date)
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
class ambulance(Base):
    __tablename__ = "ambulance"
   
    rNumber: Mapped[int] = mapped_column(Integer, primary_key=True)  #Primary Key
    lCheck: Mapped[str] = mapped_column(Date, nullable=False)  
    mAge: Mapped[int] = mapped_column(Integer, nullable=False)  
    equipment: Mapped[str] = mapped_column(String(100), nullable=False) 
    emt: Mapped[List["emt"]] = relationship(back_populates="ambulance", cascade="all, delete-orphan")
    
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

    #TransportedBy Attributes, EXTENDING TABLE HERE NOT ADDING A NEW ONE
    bPressure: Mapped[float] = mapped_column(Numeric)
    pPulse: Mapped[float] = mapped_column(Numeric)
    oLevel: Mapped[float] = mapped_column(Numeric)

    #Connection
    eID: Mapped[int] = mapped_column(Integer, ForeignKey("emt.eID"))
    emt: Mapped["EMT"] = relationship(back_populates="patient")
    
    def __repr__(self) -> str:
        return f"Patient(pID={self.pID!r}, pName={self.pName!r}, vitals(bPressure, pPulse, oLevel) = [{self.bPressure}, {self.pPulse}, {self.oLevel}])"

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
        ConEd(mID=1, mName='Stroke Care', mDate=date(2025, 3, 21), cDate=date(2025, 3, 21), eID=1),
        ConEd(mID=2, mName='Respiratory Issues', mDate=date(2025, 3, 22), cDate=date(2025, 3, 22), eID=2),
        ConEd(mID=3, mName='Cardiac Problems', mDate=date(2025, 3, 23), cDate=date(2025, 3, 23), eID=3),
        ConEd(mID=4, mName='Psychiatric Safety', mDate=date(2025, 3, 24), cDate=date(2025, 3, 24), eID=4),
        ConEd(mID=5, mName='Trauma Care', mDate=date(2025, 3, 25), cDate=date(2025, 3, 25), eID=5),
        ConEd(mID=6, mName='Motor Vehicle Collisions', mDate=date(2025, 3, 26), cDate=date(2025, 3, 26), eID=6),
        ConEd(mID=7, mName='Dementia', mDate=date(2025, 3, 27), cDate=date(2025, 3, 27), eID=7),
        ConEd(mID=8, mName='Work Safety', mDate=date(2025, 3, 28), cDate=date(2025, 3, 28), eID=8),
        ConEd(mID=9, mName='Obstetrics', mDate=date(2025, 3, 29), cDate=date(2025, 3, 29), eID=9),
        ConEd(mID=10, mName='Stroke Care', mDate=date(2025, 3, 21), cDate=date(2025, 3, 21), eID=10),
        ConEd(mID=11, mName='Respiratory Issues', mDate=date(2025, 3, 22), cDate=date(2025, 3, 22), eID=11),
        ConEd(mID=12, mName='Cardiac Problems', mDate=date(2025, 3, 23), cDate=date(2025, 3, 23), eID=12),
        ConEd(mID=13, mName='Psychiatric Safety', mDate=date(2025, 3, 24), cDate=date(2025, 3, 24), eID=13)
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
        Facility(fName='Valley General Hospital', fAddress='101 Valley Rd', fNumber=109, dID=1),
        Facility(fName='Mountain Rescue Base', fAddress='567 Pine Rd', fNumber=106, dID=1),

        Facility(fName='East Ambulance Service', fAddress='456 State Ave', fNumber=102, dID=2),
        Facility(fName='Coastal Ambulance Service', fAddress='345 Beach Ave', fNumber=110, dID=2),
        Facility(fName='Sunset Health Center', fAddress='456 Sunset Blvd', fNumber=111, dID=2),

        Facility(fName='South Response Station', fAddress='789 Tree Rd', fNumber=103, dID=3),
        Facility(fName='Clearwater EMS Base', fAddress='111 Clearwater Dr', fNumber=114, dID=3),
        Facility(fName='Lakeview Medical Center', fAddress='890 Oak Blvd', fNumber=107, dID=3),

        Facility(fName='West Fire Department', fAddress='135 W Brown Ave', fNumber=104, dID=4),
        Facility(fName='Hilltop Rescue Station', fAddress='789 Hill Rd', fNumber=112, dID=4),

        Facility(fName='Central Care Center', fAddress='246 Main St', fNumber=105, dID=5),
        Facility(fName='Golden Gate Medical', fAddress='321 Gate Dr', fNumber=113, dID=5),

        Facility(fName='Riverbend EMS Station', fAddress='234 River Rd', fNumber=108, dID=6),

        Facility(fName='Redwood Health Facility', fAddress='222 Redwood St', fNumber=115, dID=7),
        Facility(fName='Lakeview Medical Center', fAddress='890 Oak Blvd', fNumber=107, dID=7),

        Facility(fName='Seaside Ambulance Center', fAddress='333 Seaside Rd', fNumber=116, dID=8),
        Facility(fName='Sunset Health Center', fAddress='456 Sunset Blvd', fNumber=111, dID=8),
        Facility(fName='Hilltop Rescue Station', fAddress='789 Hill Rd', fNumber=112, dID=8)
    ]


    session.add_all(emts + modules + dispatchers + facilities + ambulance)
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

# Query: DispatcherFacilityCount (Ethan); prints dispatchers by name and id, and the count of facilities that they coordinate with
    stmt = (
        select(Dispatch.dID, Dispatch.dName, Facility.fName)
        .join(Facility, Dispatch.dID == Facility.dID)
    )

    results = session.execute(stmt).all()

    dispatcher_facility_counts = {}
    for row in results:
        dID, dName, fName = row
        if (dID, dName) not in dispatcher_facility_counts:
            dispatcher_facility_counts[(dID, dName)] = 0
        dispatcher_facility_counts[(dID, dName)] += 1

    for (dID, dName), count in dispatcher_facility_counts.items():
        print(f"{dName} (ID {dID}) coordinates with {count} facilities")
