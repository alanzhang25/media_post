from tiktok_uploader.upload import upload_videos
from tiktok_uploader.auth import AuthBackend

import os, time, random, pickle, logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Video_Object:
    def __init__(self, video_path, caption, user):
        self.video_path = video_path
        self.caption = caption
        self.user = user
    
    def __repr__(self):
        return f"Video_Object(video_path={self.video_path}, caption={self.caption}, user={self.user})"
    
def create_video_list(base_path):
    """
    Process all files in a directory and its subdirectories.

    :param base_path: The base directory to start the recursive file listing.
    """
    videos = []
    
    with open('video_objects.pkl', 'rb') as f:
        list_of_video_objects = pickle.load(f)

    for video_object in list_of_video_objects:
        path = str(video_object.video_path)
        first_index = path.find('videos')
        videos.append( {
            'video': str(path[first_index:]),
            'description': video_object.caption
        })

    # logging.debug(videos)
    return videos

def video_complete(video):
    logging.debug("SUCCESS!")
    random_time = random.randint(30, 60)
    logging.debug("Sleeping for " + str(random_time) + " secs")
    time.sleep(random_time)

base_directory = 'videos'
videos = create_video_list(base_directory)

try:
    auth = AuthBackend(cookies='tiktok/cookies.txt')
except Exception as e:
    logging.debug("Authentication error: " + str(e))

failed = []
try:
    failed = upload_videos(videos=videos, auth=auth, headless=True, on_complete=video_complete)
except Exception as e:
    logging.info("Error: " + str(e))
        
for video in failed: # each input video object which failed
    logging.debug(f'{video["video"]} with description "{video["description"]}" failed')