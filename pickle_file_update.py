import pickle, logging, random, time, os, requests


class Video_Object:

    def __init__(self, video_path, caption, user):
        self.video_path = video_path
        self.caption = caption
        self.user = user
    
    def __repr__(self):
        return f"Video_Object(video_path={self.video_path}, caption={self.caption}, user={self.user})"
    


    import os

list_of_paths = set()
def print_file_paths(directory):
    # Walk through all files and directories in the given directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Construct the full file path
            file_path = os.path.join(root, file)
            file_path = file_path[file_path.find("videos/"):]
            list_of_paths.add(file_path)

# Replace 'path_to_directory' with the path to the directory you want to scan
directory = 'videos'
print_file_paths(directory)
print(len(list_of_paths))

with open('video_objects.pkl', 'rb') as file:
    my_list = pickle.load(file)

new_list = []
print (len(my_list))
count = 0
for element in my_list:
    string = str(element.video_path).replace("/home/runner/work/media_post/media_post/", "")
    if string in list_of_paths:
        count+=1
        # new_list.append(element)
        # random.shuffle(new_list)
        # with open('video_objects.pkl', 'wb') as f:
        #     pickle.dump(new_list, f)

print(count)