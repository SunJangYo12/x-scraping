from bs4 import BeautifulSoup
import os
import time
import base64
import requests
import json



def proses(url, count, total, di):
    print("[+] Proses: [{}/{}] {}".format(count, total, url))

    urlku = "{}/{}/{}".format(os.getcwd(), di, url)

    destination = 'out_manual/{}'.format(url)
    os.makedirs(destination)
    filetag = destination+"/tag.txt"
    filecontent = destination+"/x.html"


    for file_name in os.listdir(urlku):

        if file_name.endswith('.txt'):
            with open("{}/{}".format(urlku, file_name), 'r', encoding='utf-8') as file:
                chunk = file.read().split('\n')

                with open(filetag, "a") as file:
                    for tag in chunk:

                        file.write(tag.lstrip()+"\n")


        if file_name.endswith('.html'):
            with open("{}/{}".format(urlku, file_name), 'r', encoding='utf-8') as file:
                html_content = file.read()

                soup = BeautifulSoup(html_content, 'html.parser')


                for ti in soup.find_all('div', "post-thumb"):
                    for hh in ti.find_all('h1', 'jdlz'):
                        title = hh.get_text()

                        with open(destination+'/title', "w") as xfile:
                            xfile.write(title.lstrip())


                ################# MODIF LINK ###################
                for lexot in soup.find_all('div', "lexot"):
                    print("|__ Link to base64")

                    for listdown in lexot.find_all('div', "smokeurlrh"):
                        
                        for a in listdown.find_all("a"):

                            href_value = a.get('href')
                            href_value = href_value.encode('utf-8') # ubah ke bytes
                            href_value = base64.b64encode(href_value) # ubah ke base64
                            href_value = href_value.decode('utf-8') # ubaah ke string

                            a['onclick'] = f"jin('{href_value}')"
                            del a['href']
                            del a['target']

                with open(filecontent, "a") as file:
                    file.write(str(soup))

                




    

di = 'out_1'
total_proc = len(os.listdir(di))
count = 0

files = [f for f in os.listdir(di) if os.path.isdir(os.path.join(di, f))]
files.sort()

for index, file in enumerate(files, start=1):
    try:
        proses(file, count, total_proc, di)

    except Exception as e:
        print("ERROR PROC: {}".format(e))


    count += 1

