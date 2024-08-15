from instagrapi import Client
from instagrapi.exceptions import LoginRequired


USERNAME = 'memez__4__life'
PASSWORD = 'memez4life'

cl = Client()

try:
    a = cl.login(USERNAME, PASSWORD)
    print(a)
    print("______")
    print(cl.get_settings())
except Exception as e:
    print(f"An error occurred: {e}")

cl.dump_settings('/tmp/dump.json')
# had to manually print the json settings because this wasn't writing to it
