import requests

files = [
    ('file', ('file', open('PHYS172_F23_Syllabus&Schedule_2023-10-05.pdf','rb'), 'application/octet-stream'))
]
headers = {
    'x-api-key': 'sec_AZ2dsLvF11l5eFMuq3ICSpkkREDPiJVB'
}

response = requests.post(
    'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)

if response.status_code == 200:
    print('Source ID:', response.json()['sourceId'])
else:
    print('Status:', response.status_code)
    print('Error:', response.text)



headers = {
    'x-api-key': 'sec_AZ2dsLvF11l5eFMuq3ICSpkkREDPiJVB',
    "Content-Type": "application/json",
}

data = {
    'sourceId': response.json()['sourceId'],
    'messages': [
        {
            'role': "user",
            'content': "Where are office hours for the professor?",
        }
    ]
}

response = requests.post(
    'https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)

if response.status_code == 200:
    print('Result:', response.json()['content'])
else:
    print('Status:', response.status_code)
    print('Error:', response.text)