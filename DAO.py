from models.mysqlProfessor import Professor
from models.mysqlReview import Review
from sqlalchemy import text
from datetime import datetime
from database import Database
from RMPScraper import RMPScraper
db = Database()
scraper = RMPScraper()




'''
    input: scraped data
    output: list of mysql professor models
'''
def convertToProfessorModel(data):
    professors = []
    for edge in data['edges']:
        professor = Professor(
            typename=edge['node']["__typename"],
            avgDifficulty=edge['node']["avgDifficulty"],
            avgRating=edge['node']["avgRating"],
            department=edge['node']["department"],
            firstName=edge['node']["firstName"],
            id=edge['node']["id"],
            lastName=edge['node']["lastName"],
            legacyId=edge['node']["legacyId"],
            numRatings=edge['node']["numRatings"],
            schoolId=edge['node']["school"]["id"],
            schoolName=edge['node']["school"]["name"],
            wouldTakeAgainPercent=edge['node']["wouldTakeAgainPercent"]
        )
        professors.append(professor)
    return professors

def bulk_insert_professors(professor_data, session):
    fields = "(typename, avgDifficulty, avgRating, department, firstName, id, lastName, legacyId, numRatings, schoolId, schoolName, wouldTakeAgainPercent)"
    placeholder = "(:typename, :avgDifficulty, :avgRating, :department, :firstName, :id, :lastName, :legacyId, :numRatings, :schoolId, :schoolName, :wouldTakeAgainPercent)"
    placeholders = ', '.join([placeholder for _ in professor_data])
    query = f"INSERT IGNORE INTO professors {fields} VALUES {placeholders}"
    params = [{k: v for k, v in vars(professor).items()} for professor in professor_data]
    session.execute(text(query), params)
    session.commit()

'''
    input: scraped data
    output: list of mysql review models
'''
def convertToReviewModel(data):
    reviews  = []
    teacherId = data['node']['id']
    for edge in data['node']['ratings']['edges']:
        review = Review(
            id = edge['node']["id"],
            typename = edge['node']["__typename"],
            attendanceMandatory = edge['node']["attendanceMandatory"],
            clarityRating = edge['node']["clarityRating"],
            class_ = edge['node']["class"],
            comment = edge['node']["comment"],
            createdByUser = edge['node']["createdByUser"],
            date = edge['node']["date"],
            difficultyRating = edge['node']["difficultyRating"],
            flagStatus = edge['node']["flagStatus"],
            grade = edge['node']["grade"],
            helpfulRating = edge['node']["helpfulRating"],
            isForCredit = edge['node']["isForCredit"],
            isForOnlineClass = edge['node']["isForOnlineClass"],
            legacyId = edge['node']["legacyId"],
            ratingTags = edge['node']["ratingTags"],
            teacherNote = edge['node']["teacherNote"],
            textbookUse = edge['node']["textbookUse"],
            thumbsDownTotal = edge['node']["thumbsDownTotal"],
            thumbsUpTotal = edge['node']["thumbsUpTotal"],
            wouldTakeAgain = edge['node']["wouldTakeAgain"],
            teacherId = teacherId,
            qualityRating = edge['node']['qualityRating'],
            created_at = datetime.now(),
            updated_at  =datetime.now()
        )
        reviews.append(review)
    return reviews

def bulk_insert_reviews(review_data, session):
    fields = "(id, typename, attendanceMandatory, clarityRating, class, comment, createdByUser, date, difficultyRating, flagStatus, grade, helpfulRating, isForCredit, isForOnlineClass, legacyId, ratingTags, teacherNote, textbookUse, thumbsDownTotal, thumbsUpTotal, wouldTakeAgain, teacherId, qualityRating, created_at, updated_at)"
    placeholder = "(:id, :typename, :attendanceMandatory, :clarityRating, :class_, :comment, :createdByUser, :date, :difficultyRating, :flagStatus, :grade, :helpfulRating, :isForCredit, :isForOnlineClass, :legacyId, :ratingTags, :teacherNote, :textbookUse, :thumbsDownTotal, :thumbsUpTotal, :wouldTakeAgain, :teacherId, :qualityRating, :created_at, :updated_at)"
    placeholders = ', '.join([placeholder for _ in review_data])
    query = f"INSERT IGNORE reviews {fields} VALUES {placeholders}"
    params = [{k: v for k, v in vars(review).items()} for review in review_data]
    session.execute(text(query), params)
    session.commit()
    
# data = scraper.get_professors(name="Nicholas Caporusso")
# professors = convertToProfessorModel(data)
data = scraper.get_reviews("VGVhY2hlci0yNjAxNjU1", count=50)
reviews = convertToReviewModel(data)

for review in reviews:
    print (review.id)

with db as session:
    bulk_insert_reviews(reviews, session)