import instaloader
from instaloader import Profile
from instaloader import Post

import os, shutil, argparse

class InstaProfile:
    # dictonary of instagram username to number of saved posts they have so we can skip those
    prof_to_num_of_saved = {
        "shimu_aep": 3,
    }

    def __init__(self, profile_name: str):
        self.profile_name = profile_name
        if profile_name in InstaProfile.prof_to_num_of_saved:
            self.number_of_saved_posts = InstaProfile.prof_to_num_of_saved[profile_name]
        else:
            self.number_of_saved_posts = 0
            print(f"Warning: Profile '{profile_name}' not found. Setting number of saved posts to 0.")

def main():
    parser = argparse.ArgumentParser(description="Download profile posts.")
    parser.add_argument('profile', type=str, help='Instagram profile to download')
    parser.add_argument('count', type=int, help='Number of posts to download')

    
    args = parser.parse_args()
    profile = InstaProfile(args.profile)


    download_path = "videos" 
    os.makedirs(download_path)
    download_instagram_videos(profile, download_path, args.count)

def process_txt_file(file_path):
    """
    Checks the word count in the text file. If the file contains more than 15 words, 
    it changes the content to "follow for more". It also removes any non-BMP (Basic Multilingual Plane) characters.
    Then, it overwrites the original file with the updated content.

    Args:
    file_path (str): The path to the text file to update.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        cleaned_text = ''.join(char for char in text if ord(char) <= 0xFFFF)
        if len(cleaned_text.split()) > 15:
            cleaned_text = "follow for more"

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_text)

        print("File processed successfully. Updates have been applied based on word count.")

    except FileNotFoundError:
        print("The file specified was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


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
            
            process_txt_file(os.path.join(source_folder, txt))
            # Move the mp4 and txt to the new folder
            shutil.move(os.path.join(source_folder, mp4), os.path.join(new_folder, mp4))
            shutil.move(os.path.join(source_folder, txt), os.path.join(new_folder, txt))

    if not os.listdir(source_folder):
        shutil.rmtree(source_folder)
        print("Copied videos over into folder")
    else:
        print("Source folder is not empty.")

def download_instagram_videos(insta_profile: InstaProfile, download_folder, max_count):
    """Downloads a limited number of the most recent videos from an Instagram profile.
    """

    L = instaloader.Instaloader(download_video_thumbnails=False, download_comments=False, compress_json=False, save_metadata=False)
    L.login("alanetai2332","alanetai!")
    profile = Profile.from_username(L.context, insta_profile.profile_name)

    count = 0
    num_skips = insta_profile.number_of_saved_posts
    for index, post in enumerate(profile.get_posts()):
        if not post.is_video:
            continue
        if num_skips > 0:
            num_skips-=1
            continue
        if count >= max_count:
            break
        count+=1
        L.download_post(post, target=profile.username)

    move_files_to_folder(insta_profile.profile_name, download_folder)
    
if __name__ == "__main__":
    main()