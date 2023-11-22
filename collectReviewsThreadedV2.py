from RMPScraper import RMPScraper
from database import Database
import time
import threading
from queue import Queue

scraper = RMPScraper()
db_manager = Database()


def insert_reviews(data, db_session):
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
            # Adjusted query for MySQL syntax if necessary
            db_session.execute('''INSERT INTO reviews (
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
            teacherId,
            qualityRating
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',  # Adjust placeholders
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
                                   teacherID,
                                   edge['node']['qualityRating'],
                               ))
        except Exception as e:
            print(f"Error occurred: {e}")
            continue

    db_session.commit()


def worker(queue, lock):
    with db_manager as db:  # Using the context manager for the DB connection
        while True:
            row = queue.get()
            if row is None:
                break

            id, numRatings = row
            try:
                reviews = scraper.get_reviews(id, False, count=numRatings)
            except Exception as e:
                print(f"Error getting reviews for id {id}: {str(e)}")
                continue

            insert_reviews(reviews, db)

            with lock:
                end_time = time.time()
                elapsed_time_seconds = end_time - start_time
                hours, rem = divmod(elapsed_time_seconds, 3600)
                minutes, seconds = divmod(rem, 60)
                count = total_rows - queue.qsize()
                print(
                    f'Processed {count}/{total_rows} rows. Elapsed time: {int(hours)}:{int(minutes)}:{int(seconds)} (HH:MM:SS)')
                pass
            queue.task_done()


NUM_THREADS = 50  # Adjust this value based on your needs

with db_manager as db:
    all_rows = db.query(
        '''
        SELECT t.id, t.numRatings FROM professors t 
        JOIN reviews r ON t.id = r.teacherID 
        WHERE t.numRatings >= 5 
        AND r.qualityRating IS NULL GROUP BY t.id HAVING COUNT(r.qualityRating IS NULL) > 0;
        ''')
    total_rows = len(all_rows)
    start_time = time.time()
    queue = Queue()
    lock = threading.Lock()

    for row in all_rows:
        queue.put(row)

    for _ in range(NUM_THREADS):
        thread = threading.Thread(target=worker, args=(queue, lock))
        thread.start()

    queue.join()

    for _ in range(NUM_THREADS):
        queue.put(None)

end_time = time.time()
elapsed_time = end_time - start_time
elapsed_time_hours = elapsed_time // 3600
elapsed_time_minutes = (elapsed_time % 3600) // 60
elapsed_time_seconds = (elapsed_time % 60)

print(
    f"Elapsed run time: {int(elapsed_time_hours)} hours, {int(elapsed_time_minutes)} minutes, {int(elapsed_time_seconds)} seconds")
