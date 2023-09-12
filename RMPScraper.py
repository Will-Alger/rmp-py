from constants import query_headers, url
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
            "query" : querySchool,
            "variables" : {
                "query" : {
                    "text" : name
                }
            }
        }
        data = send_request(payload, url, query_headers)['data']['newSearch']['schools']['edges']
        if log : write_to_file(data, 'university.json')
        return data

    '''
    get_professors():
    
        Args:
            schoolID (str): Required parameter to specify the ID of the school.
    
        Optional keyword arguments (**kwargs):
            count (int): Number of professors to return, defaults to 5 if not specified.
            cursor (str): The professorID from where to start collecting professors in pagination,
                            useful for large queries with many results. Default is an empty string.
            name (str): If specified, narrows down the search to the provided professor's name.
                        By default, it's an empty string.
            fallback (bool): If true, the query should fallback to default behavior if error.
                            It's set as True by default.
            departmentID (str): If specified, filters the results by department.
                                Returns professors related only to the provided departmentID.
    
        Returns:
            List of dictionary objects each representing a professor.
    
        Example Usage:
            get_professors("VGVhY2hlci0yNjAxNjU1", name="John Bob")
    '''

    def get_professors(self, log=False, **kwargs,):
        queryProfessors = read_graphql('QueryProfessors.graphql')
        schoolID = kwargs.get('schoolID', '')
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
        data = send_request(payload, url, query_headers)['data']['search']['teachers']
        if log : write_to_file(data, 'professors.json')
        return data

    '''
    get_reviews():
 
         Optional keyword arguments (**kwargs):
             count (int): Number of reviews to return, defaults to 5 if not specified.
             cursor (str): The reviewID from where to start collecting reviews in pagination,
                           useful for large queries with many results.
             courseFilter (str): If specified, filters the results by course type.
                                 Returns reviews related only to the provided courseID.
 
         Returns:
             List of dictionary objects each representing a review.
 
         Example Usage:
             get_reviews(VGVhY2hlci0yNjAxNjU1, count=25)
     
    '''   
    def get_reviews(self, professorID, log=False, **kwargs):
        queryReviews = read_graphql('QueryReviews.graphql')
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
        if log : write_to_file(data, 'reviews.json')
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

    

