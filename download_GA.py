import sys, subprocess, time, logging

logger = logging.getLogger()

python_executable = sys.executable

try:
    command = [python_executable, 'download.py', "automatic"]
    
    subprocess.run(command)
    logger.info("=============================")
    logger.info("Download Succesful!")
    logger.info("=============================")
except Exception as e:
    logger.info("Exception: " + str(e))