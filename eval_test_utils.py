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
            return response.json()['body']
        else:
            log.info(f"Request failed with status code: {response.status_code}")
    except Exception as e:
        log.info(f"An error occurred: {e}")


def extract_from_mock_query_response(response):
    # creates context using 'text' from each 'node' in response's 'source_nodes'. also deletes any instances of '\n'
    log.debug('RESPONSE IS:', response)
    log.debug('RESPONSE TYPE IS:', type(response))

    source_nodes = response['source_nodes']
    context_list = [source_node['node']['text'].replace('\n', '') for source_node in source_nodes] 
    context = '\n\n'.join(context_list)

    output = response['response']

    return [context, output]
