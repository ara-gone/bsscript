import os
import csv
import bsdiff4

def main():
    files = [
        # 'helloworld3_1_0.txt', 
        # 'centralhr3_1_0.txt', 
        # 'beacon3_1_0.txt', 
        'synchronization2_7_2.txt'  
        ]

    compare_to = [
        # 'helloworld3_2_0.txt',
        # 'centralhr3_2_0.txt',
        # 'beacon3_2_0.txt', 
        'synchronization3_2_0.txt' 
        ]

    csv_names = [
        # 'helloworld_3mo',
        # 'centralhr_3mo',
        # 'beacon_3mo', 
        'synchronization' 
        ]

    for i, txt_file in enumerate(files):
        output = open('new_line_change_csvs/{}.csv'.format(csv_names[i]), 'w')
        writer = csv.writer(output)
        
        with open('build_outputs/{}'.format(txt_file)) as f1:
            with open('build_outputs/{}'.format(compare_to[i])) as f2:

                print('comparing... ' + txt_file + ' ...to '  + compare_to[i])

                writer.writerow([txt_file])
                header = ['file_name', 'lines in 3.1.0', 'lines in 3.2.0', 'line_difference', 'diff (bytes)']
                writer.writerow(header)

                ls1 = f1.readlines()
                ls2 = f2.readlines()

                list_all(ls1, txt_file)
                list_all(ls2, compare_to[i])

                # parse every individual line in the build outputs
                for l in ls1:
                    # separate into array of strings 'ws'
                    ws = l.split(" ")
                    for w in ws:
                        if w.endswith('.c') or w.endswith('.c\n'):
                            # to remove newline characters
                            wl = ''
                            if w.endswith('.c\n'):
                                wl = w.replace('\n', '')
                            else:
                                wl = w
                            wl = wl.replace('/mnt/c/Users/dmara/bsscript/', '').replace('/mnt/c/users/dmara/bsscript/', '')
                            
                            wname = wl.split('/')
                            # print(wname[len(wname)-1])
                                                
                            wl2 = parse(wl,ls2)   
                            # check path
                            if wl2 == '' or wl2 == None:
                                print('could not find ' + wl + ' in 3.2.0')

                            elif os.path.exists('zephyr2_7_2/' + wl.replace('zephyr/', '')) and os.path.exists('zephyr3_2_0/' + wl2.replace('zephyr/', '')):
                                updated_wl = 'zephyr3_1_0/' + wl.replace('zephyr/', '')
                                updated_wl2 = 'zephyr3_2_0/' + wl2.replace('zephyr/', '') 

                                src_f = open(updated_wl,'r')
                                dst_f = open(updated_wl2,'r')
              
                                x = len(src_f.readlines())
                                y = len(dst_f.readlines())

                                src_f = open(updated_wl,'r')
                                dst_f = open(updated_wl2,'r')
                                bytes_ = bsdiff4.diff(src_f.read(), dst_f.read())

                                writer.writerow([wl,x,y,x-y,len(bytes_)])
                                

def parse(path, ls):
    # parse every individual line in the build outputs
    for l in ls:
        # separate into array of strings 'ws'
        ws = l.split(" ")
        for w in ws:
            if w.endswith('.c') or w.endswith('.c\n'):
                # to remove newline characters
                wl = ''
                if w.endswith('.c\n'):
                    wl = w.replace('\n', '') 
                else:
                    wl = w
                wl = wl.replace('/mnt/c/Users/dmara/bsscript/', '').replace('/mnt/c/users/dmara/bsscript/', '')
                # print(wl)
                if wl == path:
                    print('matched... ' + path + ' to ' + wl )
                    return wl

def list_all(ls, name):

    # parse every individual line in the build outputs 
    with open('file_lists/list_{}'.format(name), 'w') as f:
        f.write(name + '\n')
        for l in ls:
            # separate into array of strings 'ws'
            ws = l.split(" ")
            for w in ws:
                if w.endswith('.c') or w.endswith('.c\n'):
                    # to remove newline characters
                    wl = ''
                    if w.endswith('.c\n'):
                        wl = w.replace('\n', '') 
                    else:
                        wl = w
                    wl = wl.replace('/mnt/c/Users/dmara/bsscript/', '').replace('/mnt/c/users/dmara/bsscript/', '')
                    f.write(wl + '\n')

if __name__ == "__main__":
    main()