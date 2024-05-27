import sys, subprocess, time, logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Starting the script...")

python_executable = sys.executable

try:
    command = [python_executable, 'download.py', "automatic"]
    
    subprocess.run(command)
    logging.info("=============================")
    logging.info("Download Succesful!")
    logging.info("=============================")
except Exception as e:
    logging.info("Exception: " + str(e))