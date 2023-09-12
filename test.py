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
db_manager = SQLiteManager('my_database.db')

with open('./schema.sql', 'r') as f:
    schema = f.read()

with db_manager.get_connection() as connection:
    cursor = connection.cursor()
    cursor.executescript(schema)

# INSERT PROFESSOR QUERY DATA













# with open('us-colleges.txt', 'r') as file:
#     for line in file:
#         # Split the line at the first '(' and strip unnecessary spaces
#         school_name = line.split('(')[0].strip()
#         schoolQuery = scraper.get_school(school_name)
#         if (len(schoolQuery) >= 10) : 
#             print(school_name)
#             break;
# scraper.get_school('Abilene Christian University', True)
