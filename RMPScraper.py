from constants import query_headers, url
import requests
import json
import os

class RMPScraper:
    def __init__(self):
        # do something
        pass

    def get_school(self, name):
        querySchool = read_graphql('QuerySchool.graphql')
        payload = {
            "query" : querySchool,
            "variables" : {
                "query" : {
                    "text" : name
                }
            }
        }
        data = send_request(payload, url, query_headers)
        # write to data file for testing purposes
        write_to_file(data, 'university.json')
        return data


    def get_professors(self, schoolID, **kwargs):
        queryProfessors = read_graphql('QueryProfessors.graphql')
        # set default values
        count = kwargs.get('count', 5)
        cursor = kwargs.get('cursor', '')
        name = kwargs.get('name', '') 
        fallback = kwargs.get('fallback', True)
        departmentID = kwargs.get('departmentID', None)

        payload = {
            "query" : queryProfessors,
            "variables": {
                "count": count,
                "cursor": cursor,
                "query": {
                    "text": name, 
                    "schoolID": schoolID,
                    "fallback": fallback,
                    "departmentID": departmentID
                }
            }
        }
        data = send_request(payload, url, query_headers)
        # write to data file for testing purposes
        write_to_file(data, 'professors.json')
        return data
        
    def get_reviews(self, professorID, **kwargs):
        queryReviews = read_graphql('QueryReviews.graphql')
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
        data = send_request(payload, url, query_headers)
        # write to data file for testing purposes
        write_to_file(data, 'reviews.json')
        return data


''' 
    HELPER METHODS
'''
def read_graphql(file_name):
    with open(f'./graphql/{file_name}', 'r') as file:
        return file.read().replace('\n', '')

def send_request(payload, url, headers):
    payload = json.dumps(payload)
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code != 200:
        raise Exception(f"Request failed with status {response.status_code}")
    data = response.json()
    return data

def write_to_file(data, filename):
    output_dir = './output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_path = os.path.join(output_dir, filename)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

    

