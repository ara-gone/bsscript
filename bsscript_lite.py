#!/bin/env python

import os
import bsdiff4
import csv
import sys
import filecmp

# take command line arguments for folders

def main():
    output = open('analysis_lite.csv', 'w')

    writer = csv.writer(output)
    header = ['sample', 'file', 'oldfile_version', 'newfile_version', 'patch_size']
    writer.writerow(header)

    bsscript('zephyr_v2.7.2', 'zephyr_v3.2.0', output)
    # bsscript('zephyr_v3.1.0', 'zephyr_v3.2.0', output)

def bsscript(src, dst, output):
    writer = csv.writer(output)

    s_src = R"/mnt/c/Users/dmara/bsscript/objects/"
    
    dir_src = s_src + src + '/'
    dir_dst = s_src + dst + '/'

    # get object folder
    for f1 in os.listdir(dir_src):

        # iterate over files in sample
        sample_dir = dir_src + f1
        check_dir = dir_dst + f1

        build_total = 0

        print('going through sample {} ...'.format(check_src))

        if os.path.isdir(sample_dir):
            for f2 in os.listdir(sample_dir):
                # find similar file in dir_dst

                file_src = sample_dir + '/' + f2
                file_dst = check_dir + '/' + f2

                # print(file_src)
                # print(file_dst)
                
                # if os.path.exists(file_src) and os.path.exists(file_dst) and not os.path.isdir(file_src):
                if file_src.endswith('.obj') and os.path.exists(file_src) and os.path.exists(file_dst) and not os.path.isdir(file_src):
                    with open(file_src, 'rb') as fx:
                        with open(file_dst, 'rb') as fy:
                            if not filecmp.cmp(file_src, file_dst, True): # if the two files are NOT identical...
                                # bytes_ = bsdiff4.diff(fx.read(), fy.read())

                                os.system('./bsdiff {} {} aPatch'.format(file_src, file_dst))
                                # print('diffing {} and {} results in patch size={}'.format(file_src, file_dst, len(bytes_)))

                                file_stats = os.stat('aPatch')
                                data = [f1, f2, src, dst, file_stats.st_size]
                                # data = [f1, f2, src, dst, len(bytes_)]
                                writer.writerow(data)

                                # build_total += len(bytes_)
                                build_total += file_stats.st_size
            print('for sample {} the sum of all the object file diffs is = {} bytes from {}'.format(f1, build_total, src))
            

if __name__ == "__main__":
    main()
