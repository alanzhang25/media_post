import subprocess, time, shutil


python_executable = "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"

### FILL IN THIS INFORMATION ###
profile_to_download = "doof3d"
count_of_posts = 2
####

try:
    command = [python_executable, 'download.py', profile_to_download, str(count_of_posts)]
    subprocess.run(command)
    print("=============================")
    print("Finished Downloading")
    print("=============================")


    time.sleep(10)

    command = [python_executable, 'instagram/instagram.py']
    subprocess.run(command)
    print("=============================")
    print("Finished Uploading to Instagram")
    print("=============================")

    time.sleep(15)

    command = [python_executable, 'tiktok/tiktok.py']
    subprocess.run(command)
    print("=============================")
    print("Finished Uploading to TikTok")
    print("=============================")

    time.sleep(3)
except Exception as e:
    print("Exception: " + str(e))

command = [python_executable, 'cleanup.py']
subprocess.run(command)