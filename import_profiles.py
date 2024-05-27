from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from download import Profile, login_user, USERNAME, PASSWORD

import os, argparse, logging, sqlite3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


cl = Client()
login_user(cl)


prof_to_be_inserted = {
    "dlckpics_memedaily": 0,
    "memescatalyst": 0,  
    "ra.sigma.memes": 0, 
    "uncooked_bread23": 0, 
    "doof3d": 0, 
    "squidwordmemes2": 0, 
    "summer.sleepyhead": 0, 
    "cenowtf": 0,
    "friedoptimusprime": 0,
    "needless.mp3": 0,
    "percsfo": 0, 
    "greeeencum": 0, 
    "breasts": 0,
    "internets_highlights": 0,
}

list_of_rows = []
for key in prof_to_be_inserted:
    user_id = cl.user_id_from_username(key)
    media = cl.user_clips_v1(user_id, amount=2)
    last_used_post_id = media[1].id
    temp = Profile(key, prof_to_be_inserted[key], user_id, last_used_post_id)
    list_of_rows.append(temp)
    print(temp)


conn = sqlite3.connect('account_information.sqlite')
cur = conn.cursor()

insert_query = '''
INSERT INTO profiles (username, number_of_saved, user_id, last_used_post_id)
VALUES (?, ?, ?, ?)
'''

data_to_insert = [(p.username, p.number_of_saved, p.user_id, p.last_used_post_id) for p in list_of_rows]
try:
    cur.executemany(insert_query, data_to_insert)
    conn.commit()
    print("All profiles inserted successfully.")
except sqlite3.IntegrityError as e:
    print("A database error occurred:", e)
finally:
    conn.close()

