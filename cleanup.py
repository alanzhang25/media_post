import shutil, os, logging

logger = logging.getLogger()

def main():
    video_folder = "videos"
    file_path = 'video_objects.pkl'

    # Check if the video folder exists and then remove it
    if os.path.exists(video_folder):
        shutil.rmtree(video_folder)
        logger.info("Removed video folder.")
    else:
        logger.info("Video folder does not exist.")

    # Check if the file exists and then remove it
    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info("Removed video_objects.pkl file.")
    else:
        logger.info("video_objects.pkl file does not exist.")


if __name__ == "__main__":
    main()