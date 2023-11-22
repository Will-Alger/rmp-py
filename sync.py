from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from database import Database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import insert as mysql_insert
import datetime

# sqlite models
from models.sqliteProfessor import Professor as SQLiteProfessor
from models.sqliteReview import Review as SQLiteReview

# mysql models
from models.mysqlProfessor import Professor as MySQLProfessor
from models.mysqlReview import Review as MySQLReview

sqlite_engine = create_engine("sqlite:///C:/xampp/htdocs/nku/rmp/database/db.sqlite")
SQLiteSession = sessionmaker(bind=sqlite_engine)
mySql = Database()
sqliteSession = SQLiteSession()

batch_size = 500

def syncProfessors():
    print("Gathering existing ids in mysql...")
    with mySql as session:
        existing_ids = {prof.id for prof in session.query(MySQLProfessor.id).all()}
    print("Existing ids collected")

    print("Collecting all sqlite professors...")
    all_sqlite_professors = sqliteSession.query(SQLiteProfessor).all()
    print("All sqlite professors collected into memory")

    print("filtering sqlite professors by existing ids")
    sqlite_professors = [p for p in all_sqlite_professors if p.id not in existing_ids]
    print("filtering complete")

    new_data = []
    for i, sqlite_professor in enumerate(sqlite_professors):
        print("adding professor " + sqlite_professor.id)
        mysql_professor_data = {
            'id': sqlite_professor.id,
            'typename': sqlite_professor.typename,
            'firstName': sqlite_professor.firstName,
            'lastName': sqlite_professor.lastName,
            'schoolName': sqlite_professor.schoolName,
            'schoolId': sqlite_professor.schoolId,
            'numRatings': sqlite_professor.numRatings,
            'avgDifficulty': sqlite_professor.avgDifficulty,
            'avgRating': sqlite_professor.avgRating,
            'department': sqlite_professor.department,
            'wouldTakeAgainPercent': sqlite_professor.wouldTakeAgainPercent,
            'legacyId': sqlite_professor.legacyId,
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now()
        }
        new_data.append(mysql_professor_data)

        # If we've reached the batch size, insert the records and start a new batch
        if (i + 1) % batch_size == 0:
            print("Batch completed")
            with mySql as session:
                session.bulk_insert_mappings(MySQLProfessor, new_data)
                session.commit()
            new_data = []

    # Insert any remaining records
    if new_data:
        with mySql as session:
            session.bulk_insert_mappings(MySQLProfessor, new_data)
            session.commit()
            
# def syncReviews():
#     print("Gathering existing review ids in mysql to avoid insert conflicts...")
#     with mySql as session:
#         existing_ids = {review.id for review in session.query(MySQLReview.id).all()}
#     print("Existing ids collected, " + str(len(existing_ids)) + " reviews currently present")
    
#     print("Collecting first batch of sqlite reviews...")
#     sqlite_reviews_batch = sqliteSession.query(SQLiteReview).yield_per(5000000)
    
#     current_time = datetime.datetime.now()
#     new_data = []
#     for i, sqlite_review in enumerate(sqlite_reviews_batch):
#         mysql_review_data = {
#             'id': sqlite_review.id,
#             'typename': sqlite_review.typename,
#             'attendanceMandatory': sqlite_review.attendanceMandatory,
#             'clarityRating': sqlite_review.clarityRating,
#             'class': sqlite_review.class_,
#             'comment': sqlite_review.comment,
#             'createdByUser': sqlite_review.createdByUser,
#             'date': sqlite_review.date,
#             'difficultyRating': sqlite_review.difficultyRating,
#             'flagStatus': sqlite_review.flagStatus,
#             'grade': sqlite_review.grade,
#             'helpfulRating': sqlite_review.helpfulRating,
#             'isForCredit': sqlite_review.isForCredit,
#             'isForOnlineClass': sqlite_review.isForOnlineClass,
#             'legacyId': sqlite_review.legacyId,
#             'ratingTags': sqlite_review.ratingTags,
#             'teacherNote': sqlite_review.teacherNote,
#             'textbookUse': sqlite_review.textbookUse,
#             'thumbsDownTotal': sqlite_review.thumbsDownTotal,
#             'thumbsUpTotal': sqlite_review.thumbsUpTotal,
#             'wouldTakeAgain': sqlite_review.wouldTakeAgain,
#             'teacherId': sqlite_review.teacherId,
#             'qualityRating': sqlite_review.qualityRating,
#             'created_at': current_time,
#             'updated_at': current_time
#         }
#         new_data.append(mysql_review_data)
#         # If we've reached the batch size, insert the records and start a new batch
#         if (i + 1) % batch_size == 0:
#             try:
#                 with mySql as session:
#                     session.bulk_insert_mappings(MySQLReview, new_data)
#                     session.commit()
#                     print(str(i) + " succesfully inserted on first attempt")
#                 new_data = []
#             except Exception as e:
#                 print("Conflict occurred during bulk insert at batch #{}, filtering and retrying.".format(i))
        
#                 filtered_reviews = [review for review in new_data if review['id'] not in existing_ids]
        
#                 try:
#                     with mySql as session:
#                         session.bulk_insert_mappings(MySQLReview, filtered_reviews)
#                         session.commit()
#                         print("Successfully inserted after filtering.")
#                     new_data = []
#                 except Exception as err:
#                     print(f"Error during second attempt at batch #{i}: ", err)
#                     raise err
    
#     # Insert any remaining records
#     if new_data:
#         try:
#             with mySql as session:
#                 session.bulk_insert_mappings(MySQLReview, new_data)
#                 session.commit()
#         except Exception as e:
#             print(f"Error during bulk insert of final batch: ", e)
    
#             # Retry insertion after filtering
#             try:
#                 print("Filtering sqlite reviews by existing ids")
#                 filtered_reviews = [review for review in new_data if review['id'] not in existing_ids]
#                 print("Filtering complete")
#                 with mySql as session:
#                     session.bulk_insert_mappings(MySQLReview, filtered_reviews)
#                     session.commit()
#             except Exception as e:
#                 print(f"Error during filtered bulk insert of final batch: ", e) 
#                 raise e
    
#     print("All operations completed.")

from multiprocessing import Pool
import os
import threading

def process_batch(reviews, current_time):
    worker_id = "[ Worker: " + str(os.getpid()) + " ]"
    new_data = []
    for i, sqlite_review in enumerate(reviews):
        mysql_review_data = {
            'id': sqlite_review.id,
            'typename': sqlite_review.typename,
            'attendanceMandatory': sqlite_review.attendanceMandatory,
            'clarityRating': sqlite_review.clarityRating,
            'class': sqlite_review.class_,
            'comment': sqlite_review.comment,
            'createdByUser': sqlite_review.createdByUser,
            'date': sqlite_review.date,
            'difficultyRating': sqlite_review.difficultyRating,
            'flagStatus': sqlite_review.flagStatus,
            'grade': sqlite_review.grade,
            'helpfulRating': sqlite_review.helpfulRating,
            'isForCredit': sqlite_review.isForCredit,
            'isForOnlineClass': sqlite_review.isForOnlineClass,
            'legacyId': sqlite_review.legacyId,
            'ratingTags': sqlite_review.ratingTags,
            'teacherNote': sqlite_review.teacherNote,
            'textbookUse': sqlite_review.textbookUse,
            'thumbsDownTotal': sqlite_review.thumbsDownTotal,
            'thumbsUpTotal': sqlite_review.thumbsUpTotal,
            'wouldTakeAgain': sqlite_review.wouldTakeAgain,
            'teacherId': sqlite_review.teacherId,
            'qualityRating': sqlite_review.qualityRating,
            'created_at': current_time,
            'updated_at': current_time
        }
        new_data.append(mysql_review_data)
    try:
        with mySql as session:
            session.bulk_insert_mappings(MySQLReview, new_data)
            session.commit()
            print(worker_id + " succesfully inserted on first attempt")
    except Exception as e:
        print("Conflict occured, do nothing!")
        print(worker_id + " Conflict occurred during bulk insert, filtering and retrying...")
        # filtered_reviews = [review for review in new_data if review['id'] not in existing_ids]
        # if filtered_reviews:
        #     try:
        #         with mySql as session:
        #             session.bulk_insert_mappings(MySQLReview, filtered_reviews)
        #             session.commit()
        #         print(worker_id + " Successfully inserted after filtering.")
        #     except Exception as e:
        #         print(worker_id + " Error during second attempt at insertion ")
        # else:
        #     print("[ Worker: " + str(os.getpid()) + " ] Filtering resulted in no reviews being inserted ")

    
if __name__ == "__main__":
    with open('output_ids.txt', 'r') as file:
        id_list = [line.strip() for line in file.readlines()]
    current_time = datetime.datetime.now()
    sqlite_reviews_batch = sqliteSession.query(SQLiteReview).filter(SQLiteReview.id.in_(id_list)).all()
    process_batch(sqlite_reviews_batch, current_time)
    
    # print("Collecting existing ids in mysql")
    # with mySql as session:
    #     existing_ids_mysql = {review.id for review in session.query(MySQLReview.id).all()}
    # print(f"Existing ids collected, {len(existing_ids_mysql)} reviews currently present")
    
    # print("Collecting existing ids in sqlite")
    # existing_ids_sqlite = {review.id for review in sqliteSession.query(SQLiteReview.id).all()}
    # print(f"Existing ids collected, {len(existing_ids_sqlite)} reviews currently present")
    
    # missing_in_mysql = existing_ids_sqlite - existing_ids_mysql
    # print(f"There are {len(missing_in_mysql)} reviews present in SQLite but missing in MySQL")
    
    # # Write missing ids to a file
    # with open('output_ids.txt', 'w') as f:
    #     for id in missing_in_mysql:
    #         f.write(f'{id}\n')
    
    # difference = existing_ids_sqlite.difference(existing_ids_mysql)
    # print("Number of ids in sqlite but not in mysql: ", len(difference))
    
    # with Pool(processes=10) as pool:
    #     offset = 0
    #     size = 500
    #     while True:
    #         sqlite_reviews_batch = sqliteSession.query(SQLiteReview).offset(offset).limit(size).all()
    #         if not sqlite_reviews_batch:
    #             break
    #         pool.apply_async(process_batch, (sqlite_reviews_batch, existing_ids, current_time))
    #         offset += size
    # pool.close()
    # pool.join()
    
    # with Pool(processes=10) as pool:
    #     total_rows = sqliteSession.query(SQLiteReview).count()
    #     size = 500
    #     for offset in range(total_rows, -1, -size):
    #         sqlite_reviews_batch = sqliteSession.query(SQLiteReview).offset(max(0, offset-size)).limit(size).all()
    #         if not sqlite_reviews_batch:
    #             break
    #         pool.apply_async(process_batch, (sqlite_reviews_batch, current_time))
    # pool.close()
    # pool.join()
    
# if __name__ == "__main__":
#     current_time = datetime.datetime.now()
#     print("Collecting existing ids")
#     with mySql as session:
#         existing_ids = {review.id for review in session.query(MySQLReview.id).all()}
#     print("Existing ids collected, " + str(len(existing_ids)) + " reviews currently present")

#     with Pool(processes=10) as pool:
#         total_rows = sqliteSession.query(SQLiteReview).filter(~SQLiteReview.id.in_(existing_ids)).count()
#         size = 1000
#         for offset in range(total_rows, -1, -size):
#             sqlite_reviews_batch = sqliteSession.query(SQLiteReview)\
#                                                 .filter(~SQLiteReview.id.in_(existing_ids))\
#                                                 .offset(max(0, offset-size))\
#                                                 .limit(size)\
#                                                 .all()
#             if not sqlite_reviews_batch:
#                 break
#             pool.apply_async(process_batch, (sqlite_reviews_batch, existing_ids, current_time))
#     pool.close()
#     pool.join()