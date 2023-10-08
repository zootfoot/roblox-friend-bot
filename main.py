#this breaks every few minutes, so you have to restart it
#this is a bot that sends friend requests to all the users in the database

#^ GITHUB COPILOT WROTE ALL OF THIS. I DIDNT TYPE ANY OF THAT GRRRR

import requests
import sqlite3
import time

ROBLOSECURITY_TOKEN = "roblos cookie here pls"

headers = {
    "Cookie": f".ROBLOSECURITY={ROBLOSECURITY_TOKEN}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://www.roblox.com/",
    "Origin": "https://www.roblox.com",
}

response = requests.post('https://auth.roblox.com/v1/usernames/validate', headers=headers)
csrf_token = response.headers['x-csrf-token']

database_connection = sqlite3.connect("friedrich.db")
cursor = database_connection.cursor()

cursor.execute("SELECT id FROM users WHERE role = 'Admin'")
users_to_add = cursor.fetchall()
cursor.close()

def send_friend_request(user_id):
    headers['X-CSRF-TOKEN'] = csrf_token
    response = requests.post(
        f"https://friends.roblox.com/v1/users/{user_id}/request-friendship",
        headers=headers,
        json={"friendshipOriginSourceType": 0},
    )
    if response.status_code == 200 or (response.status_code == 400 and "Already exists" in response.text):
        sent_requests_file = open("sent_requests.txt", "a+")
        sent_requests_file.write(str(user_id) + "\n")
        sent_requests_file.close()
        print(f"Sent friend request to user ID: {user_id}")
    else:
        print(f"Failed to send friend request to user ID: {user_id}")
        print(f"Response: {response.text}")

users_to_add = sorted(users_to_add, reverse=True)

sent_requests_file = open("sent_requests.txt", "a+")
sent_requests_file.seek(0)
sent_requests = set(sent_requests_file.read().splitlines())
sent_requests_file.close()

for user_id in users_to_add:
    user_id = user_id[0]
    if str(user_id) not in sent_requests:
        send_friend_request(user_id)
        time.sleep(10)