from sqlalchemy import Column, DateTime
from typing import List
from typing import Optional
from sqlalchemy import func
from sqlalchemy import DATETIME, ForeignKey, Numeric
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

username = "postgres"
password = "csclassluc"
engine = create_engine("postgresql+psycopg2://" + username + ":" + password + "@localhost/postgres")

# Define Classes/Tables
class Base(DeclarativeBase):
    pass

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

# --- Data Insertion ---
with Session(engine) as session:
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
    session.add_all(patients)
    session.commit()  # Commit patients first to get their IDs
    
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

# --- Query ---
print("## Finding Highest LOC Patients and the EMT's who treated them | EMT Wages")
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