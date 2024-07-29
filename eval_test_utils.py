import requests

import app_logger as log

def mock_query(string):
    url = "http://52.4.226.198/api/query"
    payload = {"query": string}  # Replace with actual payload data
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            log.info("Request was successful")
            # print("Response data:", response.json())
            log.debug('MOCK QUERY RESPONSE OBJECT KEYS:', response.json().keys())
            # return response.json()['body']
            return response.json()
        else:
            log.info(f"Request failed with status code: {response.status_code}")
    except Exception as e:
        log.info(f"An error occurred: {e}")



