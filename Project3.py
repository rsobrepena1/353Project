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

#Rumyr
class EMT(Base):
    __tablename__ = "emt"

    eID: Mapped[int] = mapped_column(Integer, primary_key=True)
    eName: Mapped[str] = mapped_column(String(30))
    eLOC: Mapped[int] = mapped_column(Integer)
    eWage: Mapped[float] = mapped_column(Numeric(5, 2))
    coned_modules: Mapped[List["ConEd"]] = relationship(
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
    EMT(eID=14, eLOC=3, eName='Wilson, Sam', eWage=28.75),
    EMT(eID=15, eLOC=1, eName='Barnes, Bucky', eWage=36.50)
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

    session.add_all(emts + modules)
    session.commit()


with Session(engine) as session:
#Query: Module Completion and EMTs (Rumyr)
    print("## JOIN QUERY: EMTs and their Completed Modules ##")
    stmt = (
        select(EMT.eName, ConEd.mName, ConEd.cDate)
        .join(ConEd)
    )
    results = session.execute(stmt).all()

    for eName, mName, cDate in results:
        print(f"EMT: {eName}, Module: {mName}, Completion Date: {cDate}")
