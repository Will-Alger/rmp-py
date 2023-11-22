from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(String, primary_key=True)
    typename = Column(String)
    attendanceMandatory = Column(String)
    clarityRating = Column(Integer)
    class_ = Column('class', String)  # 'class' is a reserved keyword in Python, hence the underscore
    comment = Column(String)
    createdByUser = Column(Boolean)
    date = Column(String)
    difficultyRating = Column(Integer)
    flagStatus = Column(String)
    grade = Column(String)
    helpfulRating = Column(Integer)
    isForCredit = Column(Boolean)
    isForOnlineClass = Column(Boolean)
    legacyId = Column(Integer)
    ratingTags = Column(String)
    teacherNote = Column(String)
    textbookUse = Column(Integer)
    thumbsDownTotal = Column(Integer)
    thumbsUpTotal = Column(Integer)
    wouldTakeAgain = Column(Integer)
    teacherId = Column(String)
    qualityRating = Column(Float)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)