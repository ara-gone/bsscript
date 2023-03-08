import os
import time
import urllib
import shutil

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

def count(contents, repo, sha):
    lines = 0
    if contents:
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents += repo.get_contents(file_content.path, ref=sha)
            else:
                print("assessing... " + file_content.path)
                if os.path.isfile(file_content.path):
                    lines += file_content.decoded_content.decode("utf-8", errors='replace').count('\n')
    return lines

def analysis(path, commit, lines):
    print("writing stats for... " + path)

    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    
    stats_file = open(path + '/stats.txt', 'w')
    stats_file.write('date:{:s}\n'.format(commit.commit.author.date.strftime('%d/%m/%Y')))
    stats_file.write('lines:{:d}\n'.format(lines))
    stats_file.write('additions:{:d}\n'.format(commit.stats.additions))
    stats_file.write('deletions:{:d}\n'.format(commit.stats.deletions))
    stats_file.write('changes:{:d}\n'.format(commit.stats.total))
    stats_file.write('url:{:s}\n'.format(commit.url))
    stats_file.write('html_url:{:s}\n'.format(commit.html_url))
                
def init(version):

    # create directory to place .elf builds. if exists delete the old dirs
    src = R"/mnt/c/Users/dmara/bsscript/"
    if (os.path.exists(src+'zephyr') and os.path.exists(src+'.west')):
        print("Deleting old build system...")
        shutil.rmtree(src+'zephyr')
        shutil.rmtree(src+'.west')

    # download west build system for version
    # os.system('pip uninstall west')
    # os.system('pip install west=={}'.format(version))
    os.system('west init -m https://github.com/zephyrproject-rtos/zephyr --mr {}'.format(version))

def update():
    os.system('west update')

def build(device, sample, label):

    # build that sample!
    os.system('west -v build -p -b {} samples/{} -D CONF_FILE=prj.conf'.format(device, sample))

    # copy the .elf files into folder with subdirs for each [new] sample separated by year
    src = R"/mnt/c/Users/dmara/bsscript/build/zephyr/"
    dest = R"/mnt/c/Users/dmara/bsscript/builds/"
    for file in os.listdir(src):
        src_path = src + file
        dst_path = dest + '{}/{}/'.format(label, sample)

        if not (os.path.exists(dst_path)):
            os.makedirs(dst_path)

        if os.path.isfile(src_path) and file.endswith('.elf'):
            shutil.copy(src_path, dst_path)
        if os.path.isfile(src_path) and file.endswith('.bin'):
            shutil.copy(src_path, dst_path)
        if os.path.isfile(src_path) and file.endswith('.hex'):
            shutil.copy(src_path, dst_path)

def download_commits(atk, PATH, LOOK_BACK):

    g = Github(atk)
    r = g.get_user().get_repo('zephyr')

    until = datetime.today()
    since = until.replace(year=until.year-LOOK_BACK)
    commits = r.get_commits(path=PATH, since=since, until=until)

    if (LOOK_BACK == 0):
        since = until.replace(year=until.year-1)
        commits = r.get_commits(path=PATH, since=since, until=until)
        earliest_commit = commits[0]
        latest_commit = commits[0]
    else:
        earliest_commit = commits[commits.totalCount-1]
        latest_commit = commits[0]
        if (earliest_commit.sha == latest_commit.sha):
            print("No commits within the specified timeframe")

    # get build for commit LOOK_BACK years ago
    contents = r.get_contents(PATH, ref=earliest_commit.sha)

    print("getting commit at " + earliest_commit.commit.author.date.strftime('%d/%m/%Y') + " from " + earliest_commit.html_url)

    copy = contents[:]
    analysis(PATH, earliest_commit, count(copy, r, earliest_commit.sha))
    populate(contents, r, PATH, earliest_commit.sha)

def main():
    load_dotenv()

    atk = os.getenv('ACCESS_TOKEN')
    
    # init('v3.2.0')
    # update()
    # download_commits(atk, 'samples/basic/blinky', 0)
    # download_commits(atk, 'samples/hello_world', 0)
    # download_commits(atk, 'samples/synchronization', 0)
    # download_commits(atk, 'samples/philosophers', 0)
    # download_commits(atk, 'samples/bluetooth/beacon', 0)
    # download_commits(atk, 'samples/bluetooth/mesh_demo', 0)
    # download_commits(atk, 'samples/bluetooth/handsfree', 0)
    # download_commits(atk, 'samples/bluetooth/central_hr', 0)
    # download_commits(atk, 'samples/bluetooth/peripheral', 0)
    # download_commits(atk, 'samples/sensor/ccs811', 0)
    # download_commits(atk, 'samples/sensor/lis2dh', 0)
    # download_commits(atk, 'samples/sensor/stm32_temp_sensor', 0)

    # build('qemu_x86', 'hello_world', 'v3.2.0')
    # build('qemu_x86', 'basic/blinky', 'v3.2.0')
    # build('stm32f746g_disco', 'basic/blinky', 'v3.2.0')
    # build('qemu_x86', 'synchronization', 'v3.2.0')
    # build('qemu_x86', 'philosophers', 'v3.2.0')
    # build('qemu_x86', 'bluetooth/beacon', 'v3.2.0')
    # build('qemu_x86', 'bluetooth/mesh_demo', 'v3.2.0')
    # build('qemu_x86', 'bluetooth/handsfree', 'v3.2.0')
    # build('qemu_x86', 'bluetooth/central_hr', 'v3.2.0')
    # build('qemu_x86', 'bluetooth/peripheral', 'v3.2.0')
    # build('actinius_icarus', 'sensor/stm32_temp_sensor', 'v3.2.0')

    # init('v3.1.0')

    # update()

    # download_commits(atk, 'samples/bluetooth/handsfree', 0)
    # build('qemu_x86', 'hello_world', 'v3.1.0')
    # build('qemu_x86', 'bluetooth/central_hr', 'v3.1.0')
    build('qemu_x86', 'synchronization', 'v3.1.0')
    # build('qemu_x86', 'philosophers', 'v3.1.0')
    # build('qemu_x86', 'bluetooth/mesh_demo', 'v3.1.0')
    # build('qemu_x86', 'bluetooth/handsfree', 'v3.1.0')
    # build('qemu_x86', 'bluetooth/beacon', 'v3.1.0')

    # init('v2.7.2')
    # update()
    # download_commits(atk, 'samples/hello_world', 2)
    # download_commits(atk, 'samples/basic/blinky', 2)
    download_commits(atk, 'samples/synchronization', 2)
    # download_commits(atk, 'samples/philosophers', 2)
    # download_commits(atk, 'samples/bluetooth/beacon', 2)
    # download_commits(atk, 'samples/bluetooth/central_hr', 2)
    # download_commits(atk, 'samples/bluetooth/handsfree', 2)
    # download_commits(atk, 'samples/sensor/stm32_temp_sensor', 2)
    
    # build('qemu_x86', 'hello_world', 'v2.7.2')
    # build('stm32f746g_disco', 'basic/blinky', 'v2.7.2')
    build('qemu_x86', 'synchronization', 'v2.7.2')
    # build('qemu_x86', 'philosophers', 'v2.7.2')
    # build('qemu_x86', 'bluetooth/beacon', 'v2.7.2')
    # build('qemu_x86', 'bluetooth/central_hr', 'v2.7.2')
    # build('qemu_x86', 'bluetooth/handsfree', 'v2.7.2')
    # build('actinius_icarus', 'sensor/stm32_temp_sensor', 'v2.7.2')

    # init('v2.6.0')
    # build('qemu_x86', 'hello_world', 'v2.6.0')
    # build('qemu_x86', 'basic/blinky', 'v2.6.0')
    # build('qemu_x86', 'synchronization', 'v2.6.0')
    # build('qemu_x86', 'philosophers', 'v2.6.0')
    # build('qemu_x86', 'bluetooth/beacon', 'v2.6.0')
    # build('qemu_x86', 'bluetooth/central_hr', 'v2.6.0')
    # build('qemu_x86', 'bluetooth/handsfree', 'v2.6.0')
    # build('actinius_icarus', 'sensor/stm32_temp_sensor', 'v2.6.0')

    # init('v2.4.0') # Sep 27 2020
    # download_commits(atk, 'samples/hello_world', 3)
    # download_commits(atk, 'samples/synchronization', 3)
    # download_commits(atk, 'samples/philosophers', 3)
    # download_commits(atk, 'samples/bluetooth/handsfree', 3)
    # download_commits(atk, 'samples/sensor/stm32_temp_sensor', 3)

    # build('qemu_x86', 'hello_world', 'v2.4.0')
    # build('qemu_x86', 'synchronization', 'v2.4.0')
    # build('qemu_x86', 'philosophers', 'v2.4.0')
    # build('qemu_x86', 'bluetooth/handsfree', 'v2.4.0')
    # build('actinius_icarus', 'sensor/stm32_temp_sensor', 'v2.4.0')

    # init('v2.0.0') # Sep 6 2019
    # download_commits(atk, 'samples/hello_world', 4)
    # download_commits(atk, 'samples/synchronization', 4)
    # download_commits(atk, 'samples/philosophers', 4)
    # download_commits(atk, 'samples/bluetooth/handsfree', 4)
    # download_commits(atk, 'samples/sensor/stm32_temp_sensor', 4)

    # build('qemu_x86', 'hello_world', 'v2.0.0')
    # build('qemu_x86', 'synchronization', 'v2.0.0')
    # build('qemu_x86', 'philosophers', 'v2.0.0')
    # build('qemu_x86', 'bluetooth/handsfree', 'v2.0.0')
    # build('actinius_icarus', 'sensor/stm32_temp_sensor', 'v2.0.0')

    # init('v1.13.0') # Sep 11 2018

if __name__ == "__main__":
    main()

# get old and new versions of sample
# use west to generate firmware.elf for sample
# run bsdiff on old and new .elf files
# output patch size on .csv
# output change in lines of code