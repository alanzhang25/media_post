from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging, os, time, random, pickle

USERNAME = 'chalant_ttrp'
PASSWORD = 'alanetai2332'
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Video_Object:
    def __init__(self, video_path, caption, user):
        self.video_path = video_path
        self.caption = caption
        self.user = user
    
    def __repr__(self):
        return f"Video_Object(video_path={self.video_path}, caption={self.caption}, user={self.user})"
    

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
                logger.info("Success with session")
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
    
    with open('video_objects.pkl', 'rb') as f:
        list_of_video_objects = pickle.load(f)

    for video_object in list_of_video_objects:
        videos.append( {
            'video': video_object.video_path,
            'description': video_object.caption
        })

    logger.info(videos)
    return videos

base_directory = 'videos'  # Change this to your directory path
videos = create_video_list(base_directory)


cl = Client()
login_user(cl)

try:
    for video in videos:
        video_path, description = video["video"], video["description"]
        logger.info("Video Path: " + str(video_path))
        logger.info("Description: " + description)
        cl.clip_upload(video_path, description)
        logger.info("SUCCESS!")
        random_time = random.randint(30, 60)
        logger.info("Sleeping for " + str(random_time) + " secs")
        time.sleep(random_time)
except Exception as e:
    logger.info("Error: " + str(e))
