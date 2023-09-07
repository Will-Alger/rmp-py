import requests
import json


""" 
    Notes: pretty sure passing a cursor is optional. If you don't pass the cursor it just uses the first one?



"""

url = "https://www.ratemyprofessors.com/graphql"

request_amt = 4
# payload_dict = {
#     "query": """
#         query TeacherSearchPaginationQuery(
#             $count: Int!
#             $cursor: String
#             $query: TeacherSearchQuery!
#         ) {
#             search: newSearch {
#                 ...TeacherSearchPagination_search_1jWD3d
#             }
#         }

#         fragment TeacherSearchPagination_search_1jWD3d on newSearch {
#             teachers(query: $query, first: $count, after: $cursor) {
#                 didFallback
#                 edges {
#                     cursor
#                     node {
#                         ...TeacherCard_teacher
#                         id
#                         __typename
#                     }
#                 }
#                 pageInfo {
#                     hasNextPage
#                     endCursor
#                 }
#                 resultCount
#                 filters {
#                     field
#                     options {
#                         value
#                         id
#                     }
#                 }
#             }
#         }

#         fragment TeacherCard_teacher on Teacher {
#             id
#             legacyId
#             avgRating
#             numRatings
#             ...CardFeedback_teacher
#             ...CardSchool_teacher
#             ...CardName_teacher
#             ...TeacherBookmark_teacher
#         }

#         fragment CardFeedback_teacher on Teacher {
#             wouldTakeAgainPercent
#             avgDifficulty
#         }

#         fragment CardSchool_teacher on Teacher {
#             department
#             school {
#                 name
#                 id
#             }
#         }

#         fragment CardName_teacher on Teacher {
#             firstName
#             lastName
#         }

#         fragment TeacherBookmark_teacher on Teacher {
#             id
#             isSaved
#         }
#     """,
#     "variables": {
#         "count": request_amt,
#         "cursor": "YXJyYXljb25uZWN0aW9uOjg2MA",
#         "query": {
#             "text": "",
#             "schoolID": "U2Nob29sLTY5OQ==",
#             "fallback": True,
#             "departmentID": None
#         }
#     }
# }

# payload_dict2 = {
#     "query": """
#     query RatingsListQuery(
#       $count: Int!
#       $id: ID!
#       $courseFilter: String
#       $cursor: String
#     ) { 
#       node(id: $id) {
#         __typename
#         ... on Teacher {
#           ...RatingsList_teacher_4pguUW
#         }
#         id
#       }
#     }

#     fragment RatingsList_teacher_4pguUW on Teacher {
#       id
#       legacyId
#       lastName
#       numRatings
#       school {
#         id
#         legacyId
#         name
#         city
#         state
#         avgRating
#         numRatings
#       }
#       ...Rating_teacher
#       ...NoRatingsArea_teacher
#       ratings(first: $count, after: $cursor, courseFilter: $courseFilter) {
#         edges {
#           cursor
#           node {
#             ...Rating_rating
#             id
#             __typename
#           }
#         }
#         pageInfo {
#           hasNextPage
#           endCursor
#         }
#       }
#     }

#     fragment Rating_teacher on Teacher {
#       ...RatingFooter_teacher
#       ...RatingSuperHeader_teacher
#       ...ProfessorNoteSection_teacher
#     }

#     fragment NoRatingsArea_teacher on Teacher {
#       lastName
#       ...RateTeacherLink_teacher
#     }

#     fragment Rating_rating on Rating {
#       comment
#       flagStatus
#       createdByUser
#       teacherNote {
#         id
#       }
#       ...RatingHeader_rating
#       ...RatingSuperHeader_rating
#       ...RatingValues_rating
#       ...CourseMeta_rating
#       ...RatingTags_rating
#       ...RatingFooter_rating
#       ...ProfessorNoteSection_rating
#     }

#     fragment RatingHeader_rating on Rating {
#       legacyId
#       date
#       class
#       helpfulRating
#       clarityRating
#       isForOnlineClass
#     }

#     fragment RatingSuperHeader_rating on Rating {
#       legacyId
#     }

#     fragment RatingValues_rating on Rating {
#       helpfulRating
#       clarityRating
#       difficultyRating
#     }

#     fragment CourseMeta_rating on Rating {
#       attendanceMandatory
#       wouldTakeAgain
#       grade
#       textbookUse
#       isForOnlineClass
#       isForCredit
#     }

#     fragment RatingTags_rating on Rating {
#       ratingTags
#     }

#     fragment RatingFooter_rating on Rating {
#       id
#       comment
#       adminReviewedAt
#       flagStatus
#       legacyId
#       thumbsUpTotal
#       thumbsDownTotal
#       thumbs {
#         thumbsUp
#         thumbsDown
#         computerId
#         id
#       }
#       teacherNote {
#         id
#       }
#     }

#     fragment ProfessorNoteSection_rating on Rating {
#       teacherNote {
#         ...ProfessorNote_note
#         id
#       }
#       ...ProfessorNoteEditor_rating
#     }

#     fragment ProfessorNote_note on TeacherNotes {
#       comment
#       ...ProfessorNoteHeader_note
#       ...ProfessorNoteFooter_note
#     }

#     fragment ProfessorNoteEditor_rating on Rating {
#       id
#       legacyId
#       class
#       teacherNote {
#         id
#         teacherId
#         comment
#       }
#     }

#     fragment ProfessorNoteHeader_note on TeacherNotes {
#       createdAt
#       updatedAt
#     }

#     fragment ProfessorNoteFooter_note on TeacherNotes {
#       legacyId
#       flagStatus
#     }

#     fragment RateTeacherLink_teacher on Teacher {
#       legacyId
#       numRatings
#       lockStatus
#     }

#     fragment RatingFooter_teacher on Teacher {
#       id
#       legacyId
#       lockStatus
#       isProfCurrentUser
#     }

#     fragment RatingSuperHeader_teacher on Teacher {
#       firstName
#       lastName
#       legacyId
#       school {
#         name
#         id
#       }
#     }

#     fragment ProfessorNoteSection_teacher on Teacher {
#       ...ProfessorNote_teacher
#       ...ProfessorNoteEditor_teacher
#     }

#     fragment ProfessorNote_teacher on Teacher {
#       ...ProfessorNoteHeader_teacher
#       ...ProfessorNoteFooter_teacher
#     }

#     fragment ProfessorNoteEditor_teacher on Teacher {
#       id
#     }

#     fragment ProfessorNoteHeader_teacher on Teacher {
#       lastName
#     }

#     fragment ProfessorNoteFooter_teacher on Teacher {
#       legacyId
#       isProfCurrentUser
#     }
#     """,
#     "variables": {
#         "count": 50,
#         "id": "VGVhY2hlci02OTY2NTk=",
#         "courseFilter": None,
#         "cursor": "YXJyYXljb25uZWN0aW9uOjA"
#     }
# }

with open('./graphql/QueryProfessors.graphql', 'r') as file:
    queryProfessors = file.read().replace('\n', '')

with open('./graphql/QueryReviews.graphql', 'r') as file:
    queryReviews = file.read().replace('\n', '')

# payload_dict = {
#     "query" : queryProfessors,
#     "variables": {
#         "count": 500,
#         "cursor": "", # <-- This is the cursor to the teacher to start getting professors from. In our case, we want to use the first one (MIGHT BE OPTIONAL)
#         "query": {
#             "text": "", # <-- A string can be passed here to search by professor name
#             "schoolID": "U2Nob29sLTY5OQ==",
#             "fallback": True,
#             "departmentID": None
#         }
#     }
# }

def create_professor_payload(count, schoolID, text="", cursor="",  fallback=True, departmentID=None):
    payload_dict = {
        "query" : queryProfessors,
        "variables": {
            "count": count,
            "cursor": cursor,
            "query": {
                "text": text, 
                "schoolID": schoolID,
                "fallback": fallback,
                "departmentID": departmentID
            }
        }
    }
    return payload_dict
payload_dict = create_professor_payload(5, "U2Nob29sLTY5OQ==")

payload_dict2 = {
    "query": queryReviews,
    "variables": {
        "count": 1,
        "id": "VGVhY2hlci02OTY2NTk=", # <-- this is the professor ID associated with the reviews
        "courseFilter": None,
        "cursor": "" # <-- This is the cursor for the first review on the page (MIGHT BE OPTIONAL)
    }
}


payload = json.dumps(payload_dict)

headers = {
  'Accept': '*/*',
  'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
  'Authorization': 'Basic dGVzdDp0ZXN0',
  'Connection': 'keep-alive',
  'Content-Type': 'application/json',
  'DNT': '1',
  'Origin': 'https://www.ratemyprofessors.com',
  'Referer': 'https://www.ratemyprofessors.com/search/professors/699?q=*',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin'
}

response = requests.request("POST", url, headers=headers, data=payload)

# Convert the response content to JSON
data = response.json()

# Write the data to 'output.json'
with open('output.json', 'w') as f:
    json.dump(data, f, indent=4)



