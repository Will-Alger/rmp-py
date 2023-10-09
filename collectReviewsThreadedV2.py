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
import threading
from queue import Queue

def worker(queue, lock):
    with db_manager.get_connection() as connection:
        while True:
            row = queue.get()
            if row is None: 
                break
            
            id = row[0]
            numRatings = row[1]

            try:
                reviews = scraper.get_reviews(id, False, count=numRatings)
            except Exception as e:
                print(f"Error getting reviews for id {id}: {str(e)}")
                continue
            
            insert_reviews(reviews, connection)
        
            with lock:
                end_time = time.time()
                elapsed_time_seconds = end_time - start_time
                hours, rem = divmod(elapsed_time_seconds, 3600)
                minutes, seconds = divmod(rem, 60)
                count = total_rows - queue.qsize()
                print(f'Processed {count}/{total_rows} rows. Elapsed time: {int(hours)}:{int(minutes)}:{int(seconds)} (HH:MM:SS)')
            queue.task_done()



NUM_THREADS = 15  # Adjust this value based on your needs

with db_manager.get_connection() as connection:
    cursor = connection.cursor()
    # cursor.execute("""
    #     SELECT t.id, t.numRatings 
    #     FROM Teachers t
    #     WHERE t.numRatings >= 5 
    #     AND t.numRatings != (SELECT COUNT(*) FROM Reviews r WHERE r.teacherID = t.id)
    # """)
    cursor.execute("""
        SELECT t.id, t.numRatings
        FROM Teachers t
        LEFT JOIN Reviews r ON t.id = r.teacherID
        WHERE t.numRatings >= 5
        GROUP BY t.id
        HAVING COUNT(r.teacherID) != t.numRatings
    """)
    # cursor.execute("""
    #     SELECT t.id, t.numRatings 
    #     FROM Teachers t
    #     WHERE t.numRatings >= 5 
    #     AND t.id NOT IN (SELECT r.teacherID FROM Reviews r)
    # """)
    all_rows = cursor.fetchall()
    total_rows = len(all_rows) 

    start_time = time.time()

    # Reverse the order of rows
    # all_rows = all_rows[::-1]
    
    queue = Queue()
    lock = threading.Lock()

    for row in all_rows:
        queue.put(row)

    for _ in range(NUM_THREADS):
        thread = threading.Thread(target=worker, args=(queue, lock))
        thread.start()

    # Wait for all tasks to complete
    queue.join()

    # Signal worker threads to exit
    for _ in range(NUM_THREADS):
        queue.put(None)

end_time = time.time()
elapsed_time = end_time - start_time
elapsed_time_hours = elapsed_time // 3600
elapsed_time_minutes = (elapsed_time % 3600) // 60
elapsed_time_seconds = (elapsed_time % 60)

print(f"Elapsed run time: {int(elapsed_time_hours)} hours, {int(elapsed_time_minutes)} minutes, {int(elapsed_time_seconds)} seconds")