from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

from sqlalchemy import create_engine

engine = create_engine("sqlite:///data.db", echo=True, future=True)

Base = declarative_base()

date_email = Table(
    "date_email",
    Base.metadata,
    Column("date", ForeignKey('date.date')),
    Column("email", ForeignKey('email.email_address')),
)


class Email(Base):
    __tablename__ = "email"
    email_address = Column(String(30), primary_key=True, unique=True)
    dates = relationship("Date", secondary=date_email, back_populates="email_addresses")


class Date(Base):
    __tablename__ = "date"
    date = Column(String(20), primary_key=True, unique=True)
    email_addresses = relationship("Email", secondary=date_email, back_populates="dates")

Base.metadata.create_all(engine)

def register(date, email) -> None:
    """
    Register the date and email into the database.
    It is many-to-many relationship, i.e. a date can have
    many subscribers and a subscriber may subscribe to many dates.
    """
    with Session(engine) as session:

        date_ = session.scalar(select(Date).where(Date.date == date))
        email_ = session.scalar(select(Email).where(Email.email_address == email))
        
        if not date_:
            date_ = Date(date=date)
        
        if not email_:
            email_ = Email(email_address=email)

        date_.email_addresses.append(email_)
        session.add(date_)
        session.commit()

    return True
    

def get_dates_from_database() -> list:
    """
    Get a list of dates we need to check from the database.
    """
    with Session(engine) as session:
        dates = session.scalars(select(Date))
        date_strings = [date.date for date in dates]

    return date_strings

def get_emails_by_date(date: str) -> list:
    """
    Get a list of email strings by the date.
    """

    with Session(engine) as session:
        date_ = session.scalar(select(Date).where(Date.date == date))
        emails = date_.email_addresses
        emails = [email.email_address for email in emails]
    
    return emails
