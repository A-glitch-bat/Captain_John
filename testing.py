import requests

response = requests.get("http://100.85.192.92/")
print("Status Code:", response.status_code)
print("Response Text:", response.text)
