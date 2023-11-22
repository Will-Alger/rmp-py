from graphql.constants import query_headers, url
import requests
import json
import os


class RMPScraper:
    def __init__(self):
        # do something
        pass

    def get_school(self, name, log=False):
        querySchool = read_graphql('QuerySchool.graphql')
        payload = {
            "query": querySchool,
            "variables": {
                "query": {
                    "text": name
                }
            }
        }
        data = send_request(payload, url, query_headers)['data']['newSearch']['schools']['edges']
        if log: write_to_file(data, 'university.json')
        return data

    def get_professors(self, log=False, **kwargs, ):
        queryProfessors = read_graphql('QueryProfessors.graphql')
        
        # Optional arguments
        schoolID = kwargs.get('schoolID', '')
        count = kwargs.get('count', 5)
        cursor = kwargs.get('cursor', '')
        name = kwargs.get('name', '')
        fallback = kwargs.get('fallback', True)
        departmentID = kwargs.get('departmentID', None)
        
        payload = {
            "query": queryProfessors,
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
        data = send_request(payload, url, query_headers)['data']['search']['teachers']
        if log: write_to_file(data, 'professors.json')
        return data


    def get_reviews(self, professorID, log=False, **kwargs):
        queryReviews = read_graphql('QueryReviews.graphql')
        
        # optional arguments
        count = kwargs.get('count', 5)
        cursor = kwargs.get('cursor', '')
        courseFilter = kwargs.get('courseFilter', None)
        
        payload = {
            "query": queryReviews,
            "variables": {
                "count": count,
                "id": professorID,
                "courseFilter": courseFilter,
                "cursor": cursor
            }
        }
        data = send_request(payload, url, query_headers)['data']
        if log: write_to_file(data, 'reviews.json')
        return data


''' 
    HELPER METHODS
'''


def read_graphql(file_name):
    with open(f'./graphql/{file_name}', 'r') as file:
        return file.read().replace('\n', '')


import time


def send_request(payload, url, headers, max_retries=10):
    payload = json.dumps(payload)

    for i in range(max_retries):  # define maximum number of retries
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            response.raise_for_status()
            data = response.json()
            return data
        except (requests.exceptions.RequestException, Exception) as e:
            print(f"Error occurred: {e}. Retrying ({i + 1}/{max_retries})")
            time.sleep(300)
    raise Exception("Failed to send request after maximum retries.")


def write_to_file(data, filename):
    output_dir = './output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_path = os.path.join(output_dir, filename)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
