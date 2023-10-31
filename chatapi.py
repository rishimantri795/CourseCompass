import requests

course = input("What course are you interested in? ")

if course == "PHYS 172" or course == "PHYS172" or course == 'phys 172' or course == 'phys172':
    files = [
    ('file', ('file', open('PHYS172_F23_Syllabus&Schedule_2023-10-05.pdf','rb'), 'application/octet-stream'))]
elif course == "MA 261" or course == "MA261" or course == 'ma 261' or course == 'ma261':
    files = [
    ('file', ('file', open('syllabus_ma261_fa23.pdf','rb'), 'application/octet-stream'))]
elif course == "CS 159" or course == "CS159" or course == 'cs 159' or course == 'cs159':
    files = [
    ('file', ('file', open('syllabus.pdf','rb'), 'application/octet-stream'))]
elif course == "ENGR 133" or course == "ENGR133" or course == 'engr 133' or course == 'engr133':
    files = [
    ('file', ('file', open('ENGR 133_Fa23_Syllabus_V4.pdf','rb'), 'application/octet-stream'))]

headers = {
    'x-api-key': 'sec_AZ2dsLvF11l5eFMuq3ICSpkkREDPiJVB'
}

response = requests.post(
    'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)

if response.status_code == 200:
    sourceid = response.json()['sourceId']
else:
    print('Status:', response.status_code)
    print('Error:', response.text)

headers = {
    'x-api-key': 'sec_AZ2dsLvF11l5eFMuq3ICSpkkREDPiJVB',
    "Content-Type": "application/json",
}


question = input("What's your question? ")

data = {
    'sourceId': response.json()['sourceId'],
    'messages': [
        {
            'role': "user",
            'content': question,
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