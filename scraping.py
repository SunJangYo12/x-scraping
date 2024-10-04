import requests
from bs4 import BeautifulSoup
import re
import json
import os


def xshorten_shrinkme(xx, zz):
    out = {
        "status": "error",
    }
    return out

def shorten_shrinkme(api_key, destination_url):
    # URL API Shrinkme.io
    url = f"https://shrinkme.io/api?api={api_key}&url={destination_url}"
    
    # Mengirim permintaan GET ke API
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if data['status'] == 'success':

            output = {
                "status": "success",
                "data": data['shortenedUrl']
            }
            return output
        else:
            output = {
                "status": "error",
                "data": data
            }
            return output
    else:
        output = {
            "status": "error",
            "data": response.status_code
        }
        return output


def shorten_ouo(api_key, destination_url):
    url = f"https://ouo.io/qs/{api_key}?s={destination_url}"
    
    return url


def proses(url, count, total):
    print("[+] Proses: [{}/{}] {}".format(count, total, url))

    response = requests.get("http://localhost:1212/{}".format(url))

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        body_content = soup.body
        judul = soup.title.get_text().split("|")

        if body_content:

            bitlytoken = "c65be156906e90b427bc071c3b1554c5be27a46c" # go bitly > setting > tab developer> api > now generete
            shrinkmetoken = "bac6d34f524df82a661d3448704893712474e274"
            ouotoken = "kkIsLD9s"

            destination = 'out/{}'.format(url)
            os.makedirs(destination)
            filecontent = destination+"/"+judul[0]+".html"
            filetag = destination+"/Tagser.txt"



            ####################################
            thumb_raw = body_content.find_all('div', "post-thumb")
            for thumb in thumb_raw:
                with open(filecontent, "a") as file:
                    file.write(thumb.prettify())


            ####################################
            kategoz_raw = body_content.find_all('div', "kategoz")
            for kategoz in kategoz_raw:
                with open(filecontent, "a") as file:
                    file.write(kategoz.prettify())



            ####################################
            for lexot in body_content.find_all('div', "lexot"):
                print("|__ Link to sort")

                for listdown in lexot.find_all('div', "smokeurlrh"):

                    qualt = listdown.find('strong').get_text()
                    print("   |__ {}".format(qualt))

                    for a in listdown.find_all("a"):
                        longlink = a['href']

                        print("      |___ "+a.get_text())
                        print("          |___ "+longlink)

                        ouolink = shorten_ouo(ouotoken, longlink)
                        shorlink = shorten_shrinkme(shrinkmetoken, ouolink)

                        if shorlink['status'] == "error":
                            shorlink = shorten_ouo(ouotoken, longlink)
                            print("          |___ LIMIT using "+shorlink)
                            a['href'] = shorlink

                        else:
                            print("          |___ "+shorlink['data'])
                            a['href'] = shorlink['data']

                    print("\n")



                for deleted in lexot.find_all(id="wrapfabtest"):
                    deleted.decompose()

                for deleted in lexot.find_all(id="dl-notif"):
                    deleted.decompose()

                with open(filecontent, "a") as file:
                    file.write(lexot.prettify())

           
            ####################################
            for tagser in body_content.find_all('div', "tagser"):
                tags = tagser.get_text().split(",")

                with open(filetag, "a") as file:
                    for tag in tags:
                        file.write(tag+"\n")

    else:
        print(f'Error: {response.status_code}')


di = 'original'
total_proc = len(os.listdir(di))
count = 0

files = [f for f in os.listdir(di) if os.path.isfile(os.path.join(di, f))]
files.sort()

for index, file in enumerate(files, start=1):

    try:
        proses(file, count, total_proc)
        os.system("mv {}/{} finish".format(di, file))

    except Exception as e:
        print("ERROR PROC: {}".format(e))
        os.system("mv {}/{} fail".format(di, file))

    count += 1

