import os
import time



def proses(url, count, total, out):
    print("[+] Proses: [{}/{}] {}".format(count, total, url))

    file_path = "{}/{}/{}/Tagser.txt".format(os.getcwd(), out, url)

    # Cek apakah file ada di folder
    if os.path.isfile(file_path):
        print("OK\n")
        return None
    else:
        print("ERROR {}".format(url))
        return url


    

di = 'out_1'
total_proc = len(os.listdir(di))
count = 0

files = [f for f in os.listdir(di) if os.path.isdir(os.path.join(di, f))]
files.sort()

fail = []

for index, file in enumerate(files, start=1):

    proc = proses(file, count, total_proc, di)
    if proc:
        fail.append(proc)

    count += 1

print("\n\nFAIL: {}".format(len(fail)))
for ff in fail:
    print(ff)
    os.system("mv {}/{} x".format(di, ff))
