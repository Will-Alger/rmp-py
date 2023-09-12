
from RMPScraper import RMPScraper
import os

# Instantiate the scraper object
scraper = RMPScraper()

schoolQuery = scraper.get_school("Northern Kentucky University")

# Search the json for the school ID
# This style of 'indexing in' [][][]... will need to be cleaned up later
schoolID = schoolQuery[0]["node"]["id"]

# Do a single query to get the total number of professors
# professorQuery = scraper.get_professors(
#     schoolID, 
#     count=1,
# )

# Grab the number of professors in the university from the response
# num_professors = professorQuery['data']['search']['teachers']['resultCount']

# Grab a professor
professors = professorQuery = scraper.get_professors(
    # schoolID, 
    cursor="",
    count=12, # count is a required field
    name="" # name is optional. pass '' to have no search parameters
)

# Get the first teacher from that list
teacherData = professors['edges'][0]['node']
teacherID = teacherData['id']
teacherReviewCount = teacherData['numRatings']

def print_teacher_info(node):
    print("\n")
    print(f"Teacher Name: {node['firstName']} {node['lastName']}")
    print(f"ID: {node['id']}")
    print(f"Department: {node['department']}")
    print(f"School: {node['school']['name']}")
    print(f"Average Difficulty: {node['avgDifficulty']}")
    print(f"Average Rating: {node['avgRating']}")
    print(f"Would Take Again Percent: {node['wouldTakeAgainPercent']}%")
    print(f"Number of Ratings: {node['numRatings']}")
    print("\n\n\n")

# Clear the console
os.system('cls' if os.name == 'nt' else 'clear')
print_teacher_info(teacherData)

#
teacherReviews = scraper.get_reviews(
    teacherID,
    count=teacherReviewCount,
)

ratings = teacherReviews['node']['ratings']['edges']
   
def print_review_details(reviews):
    for review in reviews:
        node = review['node']
        print(f"Class: {node['class']}")
        print(f"Comment: {node['comment']}")
        print(f"Date: {node['date']}")
        print(f"Difficulty Rating: {node['difficultyRating']}")
        print(f"Grade: {node['grade']}")
        print(f"Helpful Rating: {node['helpfulRating']}")
        print(f"Attendance Mandatory: {node['attendanceMandatory']}")
        print(f"Tags: {node['ratingTags']}")
        print("------")
        print("\n")

print_review_details(ratings)

print("Number of reviews collected == teacher review count? --> " + str(teacherReviewCount == len(ratings)))






