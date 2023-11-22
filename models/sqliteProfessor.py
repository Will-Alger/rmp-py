from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Professor(Base):
    __tablename__ = 'professors'

    id = Column(String, primary_key=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    typename = Column(String, nullable=False)
    schoolName = Column(String, nullable=False)
    schoolId = Column(String, nullable=False)
    numRatings = Column(Integer, nullable=False)
    avgDifficulty = Column(Float, nullable=False)
    avgRating = Column(Float, nullable=False)
    department = Column(String, nullable=False)
    wouldTakeAgainPercent = Column(Float, nullable=False)
    legacyId = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"<Professor(id='{self.id}', firstName='{self.firstName}', lastName='{self.lastName}')>"
