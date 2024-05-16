from instagrapi import Client
from instagrapi.exceptions import LoginRequired

import os, argparse, logging, sqlite3, pickle

logger = logging.getLogger()

USERNAME = 'chalant_ttrp'
PASSWORD = 'alanetai2332'

class Profile:
    def __init__(self, username, number_of_saved, user_id, last_used_post_id):
        self.username = username
        self.number_of_saved = number_of_saved
        self.user_id = user_id
        self.last_used_post_id = last_used_post_id

    def __str__(self):
        return (f"Profile(username={self.username}, "
                f"number_of_saved={self.number_of_saved}, "
                f"user_id={self.user_id}, "
                f"last_used_post_id={self.last_used_post_id})")
    
class Video_Object:
    def __init__(self, video_path, caption, user):
        self.video_path = video_path
        self.caption = caption
        self.user = user
    
    def __repr__(self):
        return f"Video_Object(video_path={self.video_path}, caption={self.caption}, user={self.user})"

def main():
    """
    There are two kinds of ways we would want to run our logic.

    1) (Manual) Download a specifc amount of videos from one profile and upload them immediately

    2) (Automatic) Everyday download the latest videos from every profile in our list, and then have a CRON to upload these videos. This idea follows
    a queue like data structure.
    """
    parser = argparse.ArgumentParser(description="Download profile posts.")
    parser.add_argument('profile', type=str, help='Instagram profile to download')
    parser.add_argument('count', type=int, help='Number of posts to download')

    
    args = parser.parse_args()

    # Connect to the SQLite database

    #TODO: Add logic to check if a manual run user is present in sql table, if not add it.
    conn = sqlite3.connect('account_information.sqlite')
    cur = conn.cursor()
    cur.execute(f"SELECT username, number_of_saved, user_id, last_used_post_id FROM profiles WHERE username=\"{args.profile}\"")
    rows = cur.fetchall()


    profiles = [Profile(*row) for row in rows]
    profile = profiles[0]


    download_path = "videos" 
    os.makedirs(download_path)

    download_videos_from_user(profile, download_path, args.count)


#TODO: remove @s
def process_caption_txt(text):
    """
    Checks the word count in the text file. If the file contains more than 15 words, 
    it changes the content to "follow for more". It also removes any non-BMP (Basic Multilingual Plane) characters.
    Then, it overwrites the original file with the updated content.

    Args:
    file_path (str): The path to the text file to update.
    """
    try:
        cleaned_text = ''.join(char for char in text if ord(char) <= 0xFFFF)
        if len(cleaned_text.split()) > 15:
            cleaned_text = "follow for more"

        return cleaned_text
    except Exception as e:
        print(f"An error occurred: {e}")

def login_user(cl: Client):
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """
    session = cl.load_settings("instagram/session.json")

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(USERNAME, PASSWORD)
            cl.delay_range = [1, 3]
            # check if session is valid
            try:
                cl.get_timeline_feed()
                print("Success with session")
            except LoginRequired:
                logger.info("Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(USERNAME, PASSWORD)
            login_via_session = True
        except Exception as e:
            logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info("Attempting to login via username and password. username: %s" % USERNAME)
            if cl.login(USERNAME, PASSWORD):
                login_via_pw = True
        except Exception as e:
            logger.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")

def download_videos_from_user(insta_profile: Profile, download_folder, max_count):
    cl = Client()
    login_user(cl)
    user_id = insta_profile.user_id
    medias = cl.user_clips(user_id, amount=max_count) 

    list_of_videos = []
    for index, media in enumerate(medias, start=1):
        path = cl.video_download_by_url(media.video_url, folder=download_folder)
        print(str(path))

        list_of_videos.append(Video_Object(path, process_caption_txt(media.caption_text), media.user))


    with open('video_objects.pkl', 'wb') as f:
        pickle.dump(list_of_videos, f)

if __name__ == "__main__":
    main()