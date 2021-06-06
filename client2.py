import requests

while True:
    user_input = input("What do you want to do? \n :")
    url = f"http://localhost:5000/?input={user_input}"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text + '\n')
