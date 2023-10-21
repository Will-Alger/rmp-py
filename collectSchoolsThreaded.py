from RMPScraper import RMPScraper
from db import SQLiteManager
scraper = RMPScraper()

db_manager = SQLiteManager('E:/rmp-py-db/rmp-py.db')

def insert_schools(data, connection):
    cursor = connection.cursor()
    count = 0   
    for school in data: 
        try:
            cursor.execute('''INSERT INTO schools (
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
                        socialActivities) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
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
            print("success: "+ str(school['node']["id"]) + " " +
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
            count = count + 1
            print(f"Error occurred: {e}")
            if count > 10 : quit();
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
            
            schoolName = row[0]

            try:
                schools = scraper.get_school(schoolName, False)
            except Exception as e:
                print(f"Error getting school for name {schoolName}: {str(e)}")
                continue
            
            insert_schools(schools, connection)
        
            with lock:
                end_time = time.time()
                elapsed_time_seconds = end_time - start_time
                hours, rem = divmod(elapsed_time_seconds, 3600)
                minutes, seconds = divmod(rem, 60)
                count = total_rows - queue.qsize()
                print(f'Processed {count}/{total_rows} rows. Elapsed time: {int(hours)}:{int(minutes)}:{int(seconds)} (HH:MM:SS)')
            queue.task_done()



NUM_THREADS = 50  # Adjust this value based on your needs

with db_manager.get_connection() as connection:
    cursor = connection.cursor();
    
    cursor.execute("""
        SELECT DISTINCT schoolName
        FROM Teachers
    """)
 
    all_rows = cursor.fetchall()
    total_rows = len(all_rows) 

    start_time = time.time()
    
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