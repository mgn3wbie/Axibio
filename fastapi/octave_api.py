import requests
import os

# todo : use parameters to make it more flexible
# todo : url or just path, user and token
def fetch_all_events():
    api_url = os.environ["API_URL"]
    auth_headers = {"X-Auth-token": os.environ["API_AUTH_TOKEN"], "X-Auth-User": os.environ["API_AUTH_USER"]}
    response = requests.get(api_url, headers=auth_headers)
    return response
