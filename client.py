import sys, os
import requests


api_url = 'http://localhost:8080/api'
os.environ['TEST_SUFFIX'] = 'smoke'
os.environ['WORKLOAD_TYPE'] = 'test'


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
