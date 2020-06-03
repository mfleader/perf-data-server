import sys
import requests

api_url = 'http://localhost:8080/api'

with open(sys.argv[1], 'rb') as f:
    print(
        requests.post(
            api_url, 
            files = {'file': f})
    )

# print(
#     requests.post(
#         api_url, 
#         files = {
#             'file': open(sys.argv[1], 'rb'),
#             'b': open(sys.argv[2], 'rb')})
# )
