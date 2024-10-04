from bs4 import BeautifulSoup
import os
import time
import base64
import requests
import json

access_token = 'ya29.a0AcM612zUxZsYbaZTleKJ7m4veqRT_ICD90f3h5CQMa5-dL_mwre4oAj2h19QBVFOOIFnvfBnFpZClBPu8Z_RhawmyFXxV586UfOFb2wIyVn8_qSHqb8-TNj-fFN2fPHvkqEIq6hd49WmX1xQ_3LXfisJVk5k0NfBhFCbOWORaCgYKAZQSARISFQHGX2MirEobvqPlbqpX6PF2rDB9rg0175'
blog_id = '6338466928954570545' #sunjangyo177@gmail.com (animefanshare17)


blog_url = f'https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/'

def proses(url, count, total, di):
    print("[+] Proses: [{}/{}] {}".format(count, total, url))

    urlku = "{}/{}/{}".format(os.getcwd(), di, url)

    tagser = []

    for file_name in os.listdir(urlku):

        if file_name.endswith('.txt'):
            itag = 0
            with open("{}/{}".format(urlku, file_name), 'r', encoding='utf-8') as file:
                chunk = file.read().split('\n')
                for tag in chunk:
                    if tag != "" and itag < 3:
                        itag += 1
                        tag = tag.lstrip()
                        tag = tag.rstrip()
                        tagser.append(tag)


        if file_name.endswith('.html'):

            with open("{}/{}".format(urlku, file_name), 'r', encoding='utf-8') as file:
                html_content = file.read()

                soup = BeautifulSoup(html_content, 'html.parser')


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


                title = "x"
                for ti in soup.find_all('div', "post-thumb"):
                    for hh in ti.find_all('h1', 'jdlz'):
                        title = hh.get_text()

                data = {
                    "kind": "blogger#post",
                    "blog": {
                        "id": blog_id
                    },
                    "title": title,
                    "labels": tagser,
                    "content": str(soup)
                }
                headers = {
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                }
                

                response = requests.post(blog_url, headers=headers, data=json.dumps(data))

                if response.status_code == 200:
                    print("Posting berhasil dibuat!\n\n")
                    return response.status_code
                    #print(response.json())
                else:
                    print(f"Gagal membuat posting. Status kode: {response.status_code}\n")
                    print(response.text)
                    return 0




    

di = 'out_1'
total_proc = len(os.listdir(di))
count = 0

files = [f for f in os.listdir(di) if os.path.isdir(os.path.join(di, f))]
files.sort()

for index, file in enumerate(files, start=1):
    try:
        proc = proses(file, count, total_proc, di)
        if proc == 200:
            os.system("mv {}/{} finish_post".format(di, file))

    except Exception as e:
        print("ERROR PROC: {}".format(e))


    time.sleep(5)



    count += 1

