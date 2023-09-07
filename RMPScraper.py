from constants import query_headers, url
import requests
import json
import os

class RMPScraper:
    def __init__(self):
        # do something
        pass


    def get_professors(self, schoolID, **kwargs):
        # get the graphql query schema
        with open('./graphql/QueryProfessors.graphql', 'r') as file:
            queryProfessors = file.read().replace('\n', '')

        # set default values
        count = kwargs.get('count', 5)
        cursor = kwargs.get('cursor', '')
        text = kwargs.get('text', '') 
        fallback = kwargs.get('fallback', True)
        departmentID = kwargs.get('departmentID', None)

        payload = {
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
        payload = json.dumps(payload)
        response = requests.request("POST", url, headers=query_headers, data=payload)
        data = response.json()
        if not os.path.exists('./output'):
            os.makedirs('./output')
        with open('./output/professors.json', 'w') as f:
            json.dump(data, f, indent=4)


    def get_reviews(self, professorID, **kwargs):
        # get the graphql query schema
        with open('./graphql/QueryReviews.graphql', 'r') as file:
            queryReviews = file.read().replace('\n', '')

        # set default values
        count = kwargs.get('count', 5)
        cursor = kwargs.get('cursor', '')
        courseFilter = kwargs.get('courseFilter', None)

        payload = {
            "query": queryReviews,
            "variables": {
                "count": count,
                "id": professorID, # professor ID
                "courseFilter": courseFilter,
                "cursor": "" # review to start from (OPTIONAL)
            }
        }

        payload = json.dumps(payload)
        response = requests.request("POST", url, headers=query_headers, data=payload)
        data = response.json()
        if not os.path.exists('./output'):
            os.makedirs('./output')
        with open('./output/reviews.json', 'w') as f:
            json.dump(data, f, indent=4)
