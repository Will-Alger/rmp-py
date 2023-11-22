from RMPScraper import RMPScraper
from database import Database
from sqlalchemy import text
from sqlalchemy.dialects.mysql import insert
from models.professor import Professor
import time

scraper = RMPScraper()
db_manager = Database()

'''
    pseudo logic:

    request (qamt)
    while pageInfo.hasNextPage == true
        request (qamt, endcursor)
        write to db contents
        delay
    
'''


def insert_teachers(data, session):
    for edge in data['edges']:
        try:
            stmt = insert(Professor).values(
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

            # Execute the statement
            session.execute(stmt)
        except Exception as e:
            continue
            print(f"Error occurred: {e}")
    session.commit()


def insert_teachers_batch(data, session):
    professors_data = []
    for edge in data['edges']:
        professor = {
            'typename': edge['node']["__typename"],
            'avgDifficulty': edge['node']["avgDifficulty"],
            'avgRating': edge['node']["avgRating"],
            'department': edge['node']["department"],
            'firstName': edge['node']["firstName"],
            'id': edge['node']["id"],
            'lastName': edge['node']["lastName"],
            'legacyId': edge['node']["legacyId"],
            'numRatings': edge['node']["numRatings"],
            'schoolId': edge['node']["school"]["id"],
            'schoolName': edge['node']["school"]["name"],
            'wouldTakeAgainPercent': edge['node']["wouldTakeAgainPercent"]
        }
        professors_data.append(professor)

    if professors_data:
        # session.execute(insert(Professor), professors_data)
        # session.commit()
        stmt = insert(Professor).values(professors_data)
        do_nothing_stmt = stmt.on_duplicate_key_update(
            id=stmt.inserted.id  # Assuming 'id' is the primary key or a unique field
        )
        session.execute(do_nothing_stmt)
        session.commit()


x = 1
current = scraper.get_professors(count=2000)
with db_manager as session:
    session.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    start_time = time.time()
    insert_teachers_batch(current, session)
    x *= 1000
    print(x)

    while current['pageInfo']['hasNextPage'] == True:
        current = scraper.get_professors(
            count=1000,
            cursor=current['pageInfo']['endCursor'],
        )
        insert_teachers(current, session)
        x *= 1000
        print(x)
    end_time = time.time()  # Record the end time after exiting the loop

    elapsed_time_hours = (end_time - start_time) / 3600
    print(f"Elapsed run time: {elapsed_time_hours} hours")
