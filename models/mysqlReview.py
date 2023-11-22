from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(String(255), primary_key=True)
    typename = Column(Text)
    attendanceMandatory = Column(Text)
    clarityRating = Column(Integer)
    class_ = Column('class', Text)
    comment = Column(Text)
    createdByUser = Column(Boolean)
    date = Column(Text)
    difficultyRating = Column(Integer)
    flagStatus = Column(Text)
    grade = Column(Text)
    helpfulRating = Column(Integer)
    isForCredit = Column(Boolean)
    isForOnlineClass = Column(Boolean)
    legacyId = Column(Integer)
    ratingTags = Column(Text)
    teacherNote = Column(Text)
    textbookUse = Column(Integer)
    thumbsDownTotal = Column(Integer)
    thumbsUpTotal = Column(Integer)
    wouldTakeAgain = Column(Integer)
    teacherId = Column(String(255))
    qualityRating = Column(Numeric(precision=8, scale=2))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)