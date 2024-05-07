from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging, os, time, random

logger = logging.getLogger()
USERNAME = 'chalant_ttrp'
PASSWORD = 'alanetai2332'

def login_user(cl: Client):
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """
    session = cl.load_settings("session.json")

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

def create_video_list(base_path):
    """
    Process all files in a directory and its subdirectories.

    :param base_path: The base directory to start the recursive file listing.
    """
    videos = []
    for dirpath, dirnames, filenames in os.walk(base_path):
        # print(f"Currently in directory: {dirpath}")
        video_path = ""
        description = ""

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            # print(f"Processing file: {file_path}")
            if filename.endswith(".mp4"):
                video_path = file_path
            elif filename.endswith(".txt"):
                with open(file_path, 'r', encoding='utf-8') as file:
                    description = file.read().strip()

        if video_path and description:
            videos.append( {
                'video': video_path,
                'description': description
            })

    # print(videos)
    return videos

base_directory = '../videos'  # Change this to your directory path
videos = create_video_list(base_directory)


cl = Client()
login_user(cl)

for video in videos:
    video_path, description = video["video"], video["description"]
    print("Video Path: " + video_path)
    print("Description: " + description)
    cl.clip_upload(video_path, description)
    print("SUCCESS!")
    random_time = random.randint(30, 60)
    print("Sleeping for " + str(random_time) + " secs")
    time.sleep(random_time)


