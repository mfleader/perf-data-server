import sys
import requests

print(
    requests.post('api_url', files = {'file': open(sys.argv[1], 'rb')})
)