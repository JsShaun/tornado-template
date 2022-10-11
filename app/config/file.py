import base64
import re
import os


BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
STATIC = BASEDIR + "/static"
PHOTO = BASEDIR + "/static/photo/"
LOGS = BASEDIR + "/logs"
WORDS = BASEDIR + "/static/pub_banned_words.txt"
with open(WORDS) as f:
    data = ""
    for i in f:
        data += base64.b64decode(i).decode().replace("\n","|")
        PATTERN = re.compile(data)
