import instaloader
from instaloader import Profile

import os
import shutil

def move_files_to_folder(source_folder, parent_folder):
    files = os.listdir(source_folder)
    mp4_files = [f for f in files if f.endswith('.mp4')]
    txt_files = [f for f in files if f.endswith('.txt')]
    
    # Pairing each mp4 with a txt and moving them to new subfolders
    for i, mp4 in enumerate(mp4_files):
        base_name = mp4.split('.')[0]
        txt = f"{base_name}.txt"
        
        if txt in txt_files:
            # Create a new folder for the pair
            new_folder = os.path.join(parent_folder, f"vid {i+1}")
            os.makedirs(new_folder, exist_ok=True)
            
            # Move the mp4 and txt to the new folder
            shutil.move(os.path.join(source_folder, mp4), os.path.join(new_folder, mp4))
            shutil.move(os.path.join(source_folder, txt), os.path.join(new_folder, txt))

    if not os.listdir(source_folder):
        shutil.rmtree(source_folder)
        print("Copied videos over into folder")
    else:
        print("Source folder is not empty.")

def download_instagram_videos(profile_name, download_folder, max_count):
    """Downloads a limited number of the most recent videos from an Instagram profile.
    """

    L = instaloader.Instaloader(download_video_thumbnails=False, download_comments=False, compress_json=False, save_metadata=False)
    L.login("alanetai2332","alanetai!")
    profile = Profile.from_username(L.context, profile_name)

    count = 0
    for post in profile.get_posts():
        if count >= max_count:
            break
        print(post.caption)
        count+=1
        L.download_post(post, target=profile.username)

    move_files_to_folder(profile_name, download_folder)
    
if __name__ == "__main__":

    profile_to_download = "lostboykal.v2"
    download_path = "videos" 
    max_posts = 3

    download_instagram_videos(profile_to_download, download_path, max_posts)