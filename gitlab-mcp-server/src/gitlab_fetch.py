import requests

headers = {"PRIVATE-TOKEN": "REMOVED_SECRETVjd2-oma2m-SU39V_LBy"}
response = requests.get("http://192.168.100.68/api/v4/projects", headers=headers)

print(response.json())  # Process the response
