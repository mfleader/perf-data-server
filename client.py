import sys, os
import requests


api_url = 'http://localhost:8080/api'

# can get username and clustername from oc cluster-info
payload = {
    'username': 'mleader',
    'clustername': 'localdev'
}

with open(sys.argv[1], 'rb') as f:
    print(
        requests.post(
            api_url, 
            files = {'file': f},
            data = payload)
    )

# print(
#     requests.post(
#         api_url, 
#         files = {
#             'file': open(sys.argv[1], 'rb'),
#             'b': open(sys.argv[2], 'rb')})
# )
