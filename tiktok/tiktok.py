from tiktok_uploader.upload import upload_videos
from tiktok_uploader.auth import AuthBackend

import os, time, random

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


# Example usage
base_directory = 'videos'  # Change this to your directory path
videos = create_video_list(base_directory)

auth = AuthBackend(cookies='tiktok/cookies.txt')

failed_videos = []
for video in videos:
    new_caption = video["description"] + " #fyp"
    temp_vid = [{"video": video["video"], "description": new_caption}]
    failed_videos.append(upload_videos(videos=temp_vid, auth=auth, headless=True))
    print("SUCCESS!")
    random_time = random.randint(30, 60)
    print("Sleeping for " + str(random_time) + " secs")
    time.sleep(random_time)
    
# for video in failed_videos: # each input video object which failed
#     print(f'{video['video']} with description "{video['description']}" failed')