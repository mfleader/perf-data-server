import sys
import requests

api_url = 'http://localhost:8080/api'

print(
    requests.post(
        api_url, 
        files = {'file': open(sys.argv[1], 'rb')})
)