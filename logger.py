import logging
import sys
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

root = os.path.split(os.path.abspath(sys.argv[0]))[0]
file_handler = logging.FileHandler(filename=root + "/signIn.log", encoding="utf-8", mode="a")
file_handler.setLevel(logging.INFO)
log_formatter = logging.Formatter('%(asctime)s[%(levelname)s]: %(message)s')
file_handler.setFormatter(log_formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
