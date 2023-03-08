import os
import time
import urllib
import shutil

from github import Github
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
atk = os.getenv('ACCESS_TOKEN')

g = Github(atk)
r = g.get_repo("GNOME/gimp")

# print additions, deletions and total line count
# get list of all commits to date

contents = r.get_contents("/")

lines = 0
if contents:
    while contents:
        file_content = contents.pop(0)
        print("reading... " + file_content.path)
        if file_content.type == "dir":
            contents += r.get_contents(file_content.path)
        else:
            lines += file_content.decoded_content.decode("utf-8").count('\n')
print(lines)