from RMPScraper import RMPScraper
from db import SQLiteManager
scraper = RMPScraper()



'''
    pseudo logic:

    request (qamt)
    while pageInfo.hasNextPage == true
        request (qamt, endcursor)
        write to db contents
        delay
    
'''

# Usage
db_manager = SQLiteManager('E:/rmp-py-db/rmp-py.db')



def insert_teacher(data, connection):
    cursor = connection.cursor()

    cursor.execute('''INSERT INTO Teachers (
        typename,
        avgDifficulty,
        avgRating,
        department,
        firstName,
        id,
        isSaved,
        lastName,
        legacyId,
        numRatings,
        schoolId,
        schoolName,
        wouldTakeAgainPercent) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
        (
            data["__typename"],
            data["avgDifficulty"],
            data["avgRating"],
            data["department"],
            data["firstName"],
            data["id"],
            data["isSaved"],
            data["lastName"],
            data["legacyId"],
            data["numRatings"],
            data["school"]["id"],
            data["school"]["name"],
            data["wouldTakeAgainPercent"]
        )
    )
    connection.commit()

def insert_teachers(data, connection):
    cursor = connection.cursor()
    for edge in data['edges']:
        try:
            cursor.execute('''INSERT INTO Teachers (
            typename,
            avgDifficulty,
            avgRating,
            department,
            firstName,
            id,
            isSaved,
            lastName,
            legacyId,
            numRatings,
            schoolId,
            schoolName,
            wouldTakeAgainPercent) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (
                edge['node']["__typename"],
                edge['node']["avgDifficulty"],
                edge['node']["avgRating"],
                edge['node']["department"],
                edge['node']["firstName"],
                edge['node']["id"],
                edge['node']["isSaved"],
                edge['node']["lastName"],
                edge['node']["legacyId"],
                edge['node']["numRatings"],
                edge['node']["school"]["id"],
                edge['node']["school"]["name"],
                edge['node']["wouldTakeAgainPercent"]
            ))
        except :
           continue

    connection.commit()

import time

# FIRST QUERY
current = scraper.get_professors(count=1000)
with db_manager.get_connection() as connection:

    # with open('./schema.sql', 'r') as f:
    #     schema = f.read()
    #     cursor = connection.cursor()
    #     cursor.executescript(schema)
    start_time = time.time()  # Add a start time right before the loop begins
    while (current['pageInfo']['hasNextPage'] == True):
        insert_teachers(current, connection)
        current = scraper.get_professors(
            count=1000,
            cursor=current['pageInfo']['endCursor']
            )
        
        time.sleep(1)
    end_time = time.time()  # Record the end time after exiting the loop

    # Calculate the elapsed time and print it out in hours
    elapsed_time_hours = (end_time - start_time) / 3600
    print(f"Elapsed run time: {elapsed_time_hours} hours")












# with open('us-colleges.txt', 'r') as file:
#     for line in file:
#         # Split the line at the first '(' and strip unnecessary spaces
#         school_name = line.split('(')[0].strip()
#         schoolQuery = scraper.get_school(school_name)
#         if (len(schoolQuery) >= 10) : 
#             print(school_name)
#             break;
# scraper.get_school('Abilene Christian University', True)
