import bsdiff4
import os
import time
import urllib

from github import Github
from datetime import datetime
from dotenv import load_dotenv

def populate(contents, repo, path, sha):
    if contents:
        os.makedirs(path, exist_ok=True)
        while contents:
            file_content = contents.pop(0)
            print("downloading... " + file_content.path)
            if file_content.type == "dir":
                os.makedirs(file_content.path, exist_ok=True)
                contents += repo.get_contents(file_content.path, ref=sha)
            else:
                urllib.request.urlretrieve(file_content.download_url, file_content.path)

def download_commits(atk, PATH, LOOK_BACK):

    g = Github(atk)
    r = g.get_user().get_repo('zephyr')

    until = datetime.today()
    since = until.replace(year=until.year-LOOK_BACK)
    commits = r.get_commits(path=PATH, since=since, until=until)
    
    earliest_commit = commits[commits.totalCount-1]
    latest_commit = commits[0]

    if (earliest_commit.sha == latest_commit.sha):
        print("No commits within the last 2 years")

    # get build for commit LOOK_BACK years ago
    contents = r.get_contents(PATH, ref=earliest_commit.sha)
    print("getting commit at " + earliest_commit.commit.author.date.strftime('%d/%m/%Y') + " from " + earliest_commit.html_url)
    populate(contents, r, PATH, earliest_commit.sha)

    # get build for recent commit
    contents = r.get_contents(PATH, ref=latest_commit.sha)
    print("getting build at " + latest_commit.commit.author.date.strftime('%d/%m/%Y')  + " from " + latest_commit.html_url)
    populate(contents, r, PATH, latest_commit.sha)


def main():
    load_dotenv()

    atk = os.getenv('ACCESS_TOKEN')
    download_commits(atk, 'samples/hello_world', 2)

if __name__ == "__main__":
    main()

# get old and new versions of sample
# use west to generate firmware.elf for sample
# run bsdiff on old and new .elf files
# output patch size on .csv
# output change in lines of code