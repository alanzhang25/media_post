from instagrapi import Client
from instagrapi.exceptions import LoginRequired

import os, argparse, logging, sqlite3, pickle, random, time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

USERNAME = 'memez__4__life'
PASSWORD = 'memez4life'

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
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for 'manual'
    parser_manual = subparsers.add_parser("manual", help="(Manual) Download a specifc amount of videos from one profile and upload them immediately")
    parser_manual.add_argument('profile', type=str, help='Instagram profile to download')
    parser_manual.add_argument('count', type=int, help='Number of posts to download')
    
    # Subparser for 'subtract'
    parser_auto = subparsers.add_parser("automatic", help="Everyday download the latest videos from every profile in our list, and then have a CRON to upload these videos. This idea follows a queue like data structure.")

    # Add more subparsers if nesscary

    # Connect to the SQLite database

    args = parser.parse_args()

    conn = sqlite3.connect('account_information.sqlite')
    cur = conn.cursor()

    cl = Client()
    login_user(cl)

    if args.command == "manual":
        logging.info("manual execution")

        #TODO: Add logic to check if a manual run user is present in sql table, if not add it.
        cur.execute(f"SELECT username, number_of_saved, user_id, last_used_post_id FROM profiles WHERE username=\"{parser_manual.profile}\"")
        rows = cur.fetchall()


        profiles = [Profile(*row) for row in rows]
        profile = profiles[0]

        download_path = "videos"
        create_video_dir(download_path)

        list_of_videos = download_videos_from_user(cl, profile, conn, cur, download_path, args.count)

        random.shuffle(list_of_videos)
        with open('video_objects.pkl', 'wb') as f:
            pickle.dump(list_of_videos, f)

    elif args.command == "automatic":
        logging.info("automatic execution")

        download_path = "videos"
        create_video_dir(download_path)
        
        cur.execute(f"SELECT username, number_of_saved, user_id, last_used_post_id FROM profiles")
        rows = cur.fetchall()
        profiles = [Profile(*row) for row in rows]

        list_of_videos = []

        with open('video_objects.pkl', 'rb') as f:
            list_of_videos = pickle.load(f)

        for profile in profiles:
            temp = download_videos_from_user(cl, profile, conn, cur, download_path)
            list_of_videos = list_of_videos + temp

        random.shuffle(list_of_videos)
        with open('video_objects.pkl', 'wb') as f:
            pickle.dump(list_of_videos, f)

    else:
        parser.print_help()
        return
    
    # Close the cursor and connection
    cur.close()
    conn.close()
    
def create_video_dir(path):
    os.makedirs(path, exist_ok=True)

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
        logging.info(f"An error occurred: {e}")

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
                logging.info("Success with session")
            except LoginRequired:
                logging.info("Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(USERNAME, PASSWORD)
            login_via_session = True
        except Exception as e:
            logging.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logging.info("Attempting to login via username and password. username: %s" % USERNAME)
            if cl.login(USERNAME, PASSWORD):
                login_via_pw = True
        except Exception as e:
            logging.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")

def update_sql_tbl (conn, cursor, last_used_post_id, user):

    try:
        # Formulate the UPDATE statement
        update_statement = """
        UPDATE profiles
        SET last_used_post_id = ?
        WHERE username = ?
        """
        
        # Execute the UPDATE statement
        cursor.execute(update_statement, (last_used_post_id, user))
        
        # Commit the transaction
        conn.commit()
        logging.info(f"Employee with id {user} had their last_video_id updated to {last_used_post_id}.")
    
    except sqlite3.Error as error:
        logging.info(f"Error occurred while updating the table: {error}")

def download_videos_from_user(cl: Client ,insta_profile: Profile, conn, cursor, download_folder, max_count=20):
    user_id = insta_profile.user_id
    medias = cl.user_clips(user_id, amount=max_count) 

    list_of_videos = []
    last_media_id = None

    for index, media in enumerate(medias, start=1):
        if (media.id == insta_profile.last_used_post_id):
            break
        rand_num = random.random()
        if rand_num < 0.8:
            logging.info("Did not download video due to chance")
            continue

        try: 
            path = cl.video_download_by_url(media.video_url, folder=download_folder)
            random_time = random.randint(5, 8)
            time.sleep(random_time)
            logging.info(str(path))
        except:
            continue

        list_of_videos.append(Video_Object(path, process_caption_txt(media.caption_text), media.user))
        last_media_id = media.id

    if last_media_id is not None:
        update_sql_tbl(conn, cursor, last_media_id, insta_profile.username)

    return list_of_videos

if __name__ == "__main__":
    main()