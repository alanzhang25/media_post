import subprocess, time, logging

logger = logging.getLogger()

python_executable = "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"

### FILL IN THIS INFORMATION ###
profile_to_download = "needless.mp4"
count_of_posts = 2
####

try:
    command = [python_executable, 'download.py', profile_to_download, str(count_of_posts)]
    subprocess.run(command)
    logger.info("=============================")
    logger.info("Finished Downloading")
    logger.info("=============================")


    time.sleep(10)

    command = [python_executable, 'instagram/instagram.py']
    subprocess.run(command)
    logger.info("=============================")
    logger.info("Finished Uploading to Instagram")
    logger.info("=============================")

    time.sleep(15)

    command = [python_executable, 'tiktok/tiktok.py']
    subprocess.run(command)
    logger.info("=============================")
    logger.info("Finished Uploading to TikTok")
    logger.info("=============================")

    time.sleep(3)
except Exception as e:
    logger.info("Exception: " + str(e))

command = [python_executable, 'cleanup.py']
subprocess.run(command)