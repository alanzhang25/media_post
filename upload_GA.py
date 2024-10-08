import pickle, logging, random, time, os, requests

from instagrapi import Client
from tiktok_uploader.upload import upload_videos
from tiktok_uploader.auth import AuthBackend 
from instagrapi.exceptions import LoginRequired
 

USERNAME = 'memez__4__life'
PASSWORD = 'memez4life'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Video_Object:

    def __init__(self, video_path, caption, user):
        self.video_path = video_path
        self.caption = caption
        self.user = user
    
    def __repr__(self):
        return f"Video_Object(video_path={self.video_path}, caption={self.caption}, user={self.user})"


def delete_file(file_path):
    """
    Delete a file at the specified path.

    Args:
    file_path (str): The path of the file to delete.
    """
    try:
        os.remove(file_path)
        logging.info(f"File '{file_path}' has been deleted successfully.")
    except FileNotFoundError:
        logging.info(f"File '{file_path}' not found.")
    except PermissionError:
        logging.info(f"Permission denied: unable to delete '{file_path}'.")
    except Exception as e:
        logging.info(f"Error occurred while deleting the file '{file_path}': {e}")

    file_path = file_path + ".jpg"
    try:
        os.remove(file_path)
        logging.info(f"File '{file_path}' has been deleted successfully.")
    except FileNotFoundError:
        logging.info(f"File '{file_path}' not found.")
    except PermissionError:
        logging.info(f"Permission denied: unable to delete '{file_path}'.")
    except Exception as e:
        logging.info(f"Error occurred while deleting the file '{file_path}': {e}")

def pop_first_element():
    with open('video_objects.pkl', 'rb') as file:
        my_list = pickle.load(file)
    
    if (len(my_list) <= 0):
        logging.info("Exiting since pickle file is empty")
        os._exit(0)
    
    first_element = my_list.pop(0)
    
    with open('video_objects.pkl', 'wb') as file:
        pickle.dump(my_list, file)

    video_obj = {
            'video': str(first_element.video_path),
            'description': first_element.caption
        }
    return video_obj


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
    
    cl.login_flow
    time.sleep(random.randint(3,8))

def disable_insta_workflow(workflow_id):
    repo_owner = "alanzhang25"
    repo_name = "media_post"
    github_token = os.getenv('GITHUB_PAT')

    # GitHub API endpoint to disable the workflow
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/workflows/{workflow_id}/disable"

    # Headers for the request
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Make the request to disable the workflow
    response = requests.put(url, headers=headers)

    if response.status_code == 204:
        print("Workflow disabled successfully!")
    else:
        print(f"Failed to disable workflow: {response.status_code}")
        print(response.json())

video = pop_first_element()

cl = Client()
login_user(cl)

try:
    video_path, description = video["video"], video["description"]
    logging.info("Video Path: " + str(video_path))
    logging.info("Description: " + description)
    cl.clip_upload(video_path, description)
    logging.info("Uploaded to Instagram!")
except Exception as e:
    logging.info("Error: " + str(e))
    disable_insta_workflow("uploader.yml")
    disable_insta_workflow("downloader.yml")


# random_time = random.randint(8, 12)
# logging.info("Sleeping for " + str(random_time) + " secs")
# time.sleep(random_time)

# try:
#     auth = AuthBackend(cookies='tiktok/cookies.txt')
# except Exception as e:
#     logging.debug("Authentication error: " + str(e))

# temp = [video]
# try:
#     failed = upload_videos(videos=temp, auth=auth, headless=True)
#     logging.info("Uploaded to TikTok!")
# except Exception as e:
#     logging.debug("Error: " + str(e))
        
# for video in failed: # each input video object which failed
#     logging.debug(f'{video["video"]} with description "{video["description"]}" failed')
delete_file(video["video"])