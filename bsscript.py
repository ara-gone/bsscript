#!/bin/env python

import os
import bsdiff4
import csv
import sys

# take command line arguments for folders

def main():
    output = open('analysis.csv', 'w')

    writer = csv.writer(output)
    header = ['sample', 'oldfile_version', 'oldfile_date', 
        'newfile_version', 'newfile_date', 'patch_size', 'line_difference', 'oldfile_size', 'newfile_size']
    # header2 = ['oldfile_size, newfile_size', 'size_difference', 'line_difference', 'commits_since']
    writer.writerow(header)

    bsscript('v3.1.0', 'v3.2.0', output)
    bsscript('v2.7.2', 'v3.2.0', output)
    # bsscript('v3.2.0', 'v2.7.2', output)
    
    bsscript('v2.6.0', 'v3.2.0', output)
    # bsscript('v2.6.0', 'v2.7.2', output)

    # bsscript('v2.4.0', 'v2.7.2', output)
    # bsscript('v2.4.0', 'v2.6.0', output)
    bsscript('v2.4.0', 'v3.2.0', output)

def bsscript(src, dst, output):
    writer = csv.writer(output)

    # src = ''
    # dst = ''
    # if (len(args) != 2):
    #     raise Exception("Need to provide args(src, dst)")
    # for i, arg in enumerate(args):
    #     if (i == 0):
    #         src = args[i]
    #     if (i == 1):
    #         dst = args[i]

    s_src = R"/mnt/c/Users/dmara/bsscript/builds/"
    
    dir_src = s_src + src + '/'
    dir_dst = s_src + dst + '/'

    # get sample folder
    for f1 in os.listdir(dir_src):

        # iterate over files in sample
        sample_dir = dir_src + f1
        check_dir = dir_dst + f1
        if os.path.isdir(sample_dir):
            for f2 in os.listdir(sample_dir):
                # find similar file in dir_dst
                file_src = sample_dir + '/' + f2
                file_dst = check_dir + '/' + f2
                
                fname = f1
                if os.path.isdir(file_src):
                    file_src += '/zephyr.hex'
                    file_dst += '/zephyr.hex'
                    fname = f1 + '/' + f2   
                    stat_src = sample_dir + '/' + f2 + '/stats.txt'
                    stat_dst = check_dir + '/' + f2 + '/stats.txt'
                else:
                    stat_src = sample_dir + '/stats.txt'
                    stat_dst = check_dir + '/stats.txt'

                if os.path.exists(file_src) and os.path.exists(file_dst) and not os.path.isdir(file_src):
                    # run diff algorithm
                    # print(file_src)
                    # print(file_dst)                               
                    with open(file_src, 'rb') as fx:
                        with open(file_dst, 'rb') as fy:

                            if file_src.endswith('/zephyr.hex'):
                                bytes_ = bsdiff4.diff(fx.read(), fy.read())
                                print('diffing {} and {} results in patch size={}'.format(file_src, file_dst, len(bytes_)))

                                # read stats.txt(s) if they exist
                                date1 = ''
                                date2 = ''
                                ldif = 0                           
                                if os.path.exists(stat_src) and os.path.exists(stat_dst):
                                    # print(stat_src)
                                    # print(stat_dst)    
                                    fs1 = open(stat_src, 'r')
                                    fs2 = open(stat_dst, 'r')

                                    content1 = fs1.readlines()
                                    content2 = fs2.readlines()

                                    for i, line in enumerate(content1):
                                        if line.startswith('date'):
                                            date1 = (content1[i][5:-1])
                                            date2 = (content2[i][5:-1])
                                        elif line.startswith('lines'):
                                            ldif = int(content2[i][6:]) - int(content1[i][6:])
                                
                                    # probably could rewrite this with all data in stats.txt
                                    data = [file_src, src, date1, dst, date2, len(bytes_), ldif, os.path.getsize(file_src), os.path.getsize(file_dst)]
                                    writer.writerow(data)

                    # out = open('./{}-{}+{}'.format(f1,src,dst), "w")
                    # bsdiff4.file_patch(file_src, file_dst, f_path)

if __name__ == "__main__":
    main()

# get old and new versions of sample
# use west to generate firmware.elf for sample
# run bsdiff on old and new .elf files
# output patch size on .csv
# output change in lines of code