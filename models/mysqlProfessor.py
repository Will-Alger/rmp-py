from sqlalchemy import create_engine, Column, Integer, String, Float, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Professor(Base):
    __tablename__ = 'professors'

    id = Column(String(255), primary_key=True)
    typename = Column(String(255), nullable=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String(255), nullable=False)
    schoolName = Column(String(255), nullable=False)
    schoolId = Column(String(255), nullable=False, index=True)
    numRatings = Column(Integer, nullable=False)
    avgDifficulty = Column(Float(precision=2), nullable=False)
    avgRating = Column(Float(precision=2), nullable=False)
    department = Column(String(255), nullable=False)
    wouldTakeAgainPercent = Column(Float(precision=2), nullable=False)
    legacyId = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
