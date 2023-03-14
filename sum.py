import os
import csv
import bsdiff4

            # for w in ws:
            #     if w.endswith('.obj') or w.endswith('.obj\n'):
            #         # to remove newline characters
            #         wl = ''
            #         if w.endswith('.c\n'):
            #             wl = w.replace('\n', '')
            #         else:
            #             wl = w
            #         wl = wl.replace('/mnt/c/Users/dmara/bsscript/', '').replace('/mnt/c/users/dmara/bsscript/', '')
            #         wname = wl.split('/')
            #         print(wname[len(wname)-1])

def main():
    total = 0

    with open('build_obj.txt') as f:
        ls = f.readlines()

        # get every file path ending with .obj
        for l in ls:
            ln = l.replace('\n', '')
            
            if (os.path.exists(ln)):
                os.system('strip --strip-debug --strip-unneeded {} -o strip.obj'.format(ln))
                bytes_ = os.stat('strip.obj').st_size
                print(ln + " when stripped: " + convert_bytes(bytes_))

                # if (bytes_ > 1024)
                total += bytes_
            else:
                print("could not find " + ln)
            
    print("total = " + convert_bytes(total))
    print(total)
    print("compared to zephyr.bin: " + convert_bytes(155680))

def convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

if __name__ == "__main__":
    main()