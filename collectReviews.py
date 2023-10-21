from RMPScraper import RMPScraper
from db import SQLiteManager
scraper = RMPScraper()

db_manager = SQLiteManager('E:/rmp-py-db/rmp-py.db')

def insert_reviews(data, connection):
    cursor = connection.cursor()
    
    try:
         teacherID = data['node']['id']
    except Exception as e:
        print(f"error getting teacher id: {str(e)} ")
        return
    

    ratings = data['node']['ratings']
    
    if ratings is None:
        print(f"No accessible ratings for teacher id: {teacherID}")
        return

    edges = ratings['edges']
       
    for edge in edges:
        try:
            cursor.execute('''INSERT INTO Reviews (
            id,
            typename,
            attendanceMandatory,
            clarityRating,
            class,
            comment,
            createdByUser,
            date,
            difficultyRating,
            flagStatus,
            grade,
            helpfulRating,
            isForCredit,
            isForOnlineClass,
            legacyId,
            ratingTags,
            teacherNote,
            textbookUse,
            thumbsDownTotal,
            thumbsUpTotal,
            wouldTakeAgain,
            teacherId) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (
                edge['node']["id"],
                edge['node']["__typename"],
                edge['node']["attendanceMandatory"],
                edge['node']["clarityRating"],
                edge['node']["class"],
                edge['node']["comment"],
                edge['node']["createdByUser"],
                edge['node']["date"],
                edge['node']["difficultyRating"],
                edge['node']["flagStatus"],
                edge['node']["grade"],
                edge['node']["helpfulRating"],
                edge['node']["isForCredit"],
                edge['node']["isForOnlineClass"],
                edge['node']["legacyId"],
                edge['node']["ratingTags"],
                edge['node']["teacherNote"],
                edge['node']["textbookUse"],
                edge['node']["thumbsDownTotal"],
                edge['node']["thumbsUpTotal"],
                edge['node']["wouldTakeAgain"],
                teacherID
            ))
        except Exception as e:
            print(f"Error occurred: {e}")
            continue

    connection.commit()
    
import time
with db_manager.get_connection() as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT id, numRatings FROM Teachers WHERE numRatings >= 5")

    all_rows = cursor.fetchall()
    total_rows = len(all_rows) 

    start_time = time.time()
    for count, row in enumerate(all_rows,1):
        id = row[0]
        numRatings = row[1]
        
        try:
            reviews = scraper.get_reviews(id, False, count=numRatings)
        except Exception as e:
            print(f"Error getting reviews for id {id}: {str(e)}")
            continue  # Skip this iteration and move to the next one
        
        insert_reviews(reviews, connection)

        end_time = time.time()
        elapsed_time_seconds = end_time - start_time
        hours, rem = divmod(elapsed_time_seconds, 3600)
        minutes, seconds = divmod(rem, 60)

        print(f'Processed {count}/{total_rows} rows. Elapsed time: {int(hours)}:{int(minutes)}:{int(seconds)} (HH:MM:SS)')   

end_time = time.time()
elapsed_time = end_time - start_time
elapsed_time_hours = elapsed_time // 3600
elapsed_time_minutes = (elapsed_time % 3600) // 60
elapsed_time_seconds = (elapsed_time % 60)

print(f"Elapsed run time: {int(elapsed_time_hours)} hours, {int(elapsed_time_minutes)} minutes, {int(elapsed_time_seconds)} seconds")