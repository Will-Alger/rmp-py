from RMPScraper import RMPScraper
from database import Database
import time
import threading
from queue import Queue

scraper = RMPScraper()
db_manager = Database()


def insert_schools(data, db_session):
    count = 0
    for school in data:
        try:
            db_session.execute('''INSERT INTO schools (
                        id,
                        legacyId,
                        name,
                        numRatings,
                        state,
                        campusCondition,
                        campusLocation,
                        careerOpportunities,
                        clubAndEventActivities,
                        foodQuality,
                        internetSpeed,
                        libraryCondition,
                        schoolReputation,
                        schoolSafety,
                        schoolSatisfaction,
                        socialActivities) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                               (
                                   school['node']["id"],
                                   school['node']["legacyId"],
                                   school['node']["name"],
                                   school['node']["numRatings"],
                                   school['node']["state"],
                                   school['node']['summary']["campusCondition"],
                                   school['node']['summary']["campusLocation"],
                                   school['node']['summary']["careerOpportunities"],
                                   school['node']['summary']["clubAndEventActivities"],
                                   school['node']['summary']["foodQuality"],
                                   school['node']['summary']["internetSpeed"],
                                   school['node']['summary']["libraryCondition"],
                                   school['node']['summary']["schoolReputation"],
                                   school['node']['summary']["schoolSafety"],
                                   school['node']['summary']["schoolSatisfaction"],
                                   school['node']['summary']["socialActivities"]
                               ))
            print("success: " + str(school['node']["id"]) + " " +
                  str(school['node']["legacyId"]) + " " +
                  str(school['node']["name"]) + " " +
                  str(school['node']["state"]) + "\n"
                  )
        except Exception as e:
            print(str(school['node']["id"]) + " " +
                  str(school['node']["legacyId"]) + " " +
                  str(school['node']["name"]) + " " +
                  str(school['node']["state"]) + "\n"
                  )
            count += 1
            print(f"Error occurred: {e}")
            if count > 10: quit();
            continue

    db_session.commit();


def worker(queue, lock):
    with db_manager as db:  # Context manager for DB connection
        while True:
            row = queue.get()
            if row is None:
                break

            schoolName = row[0]
            try:
                schools = scraper.get_school(schoolName, False)
            except Exception as e:
                print(f"Error getting school for name {schoolName}: {str(e)}")
                continue

            insert_schools(schools, db)

            with lock:
                # Time tracking code remains the same
                pass
            queue.task_done()


NUM_THREADS = 50  # Adjust this value based on your needs

with db_manager as db:
    all_rows = db.query("SELECT DISTINCT schoolName FROM professors")
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
