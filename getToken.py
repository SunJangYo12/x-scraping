from requests_oauthlib import OAuth2Session
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import requests
import time


client_id = '<>'
client_secret = '<>'


redirect_uri = 'http://localhost:8080/oauth2callback'
authorization_base_url = 'https://accounts.google.com/o/oauth2/auth'
token_url = 'https://oauth2.googleapis.com/token'
scope = ['https://www.googleapis.com/auth/blogger']


oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
authorization_url, state = oauth.authorization_url(authorization_base_url)

print(f'Kunjungi URL berikut untuk otorisasi:\n\n{authorization_url}\n\n')


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/oauth2callback'):
            query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            code = query_components.get('code')
            self.send_response(200)
            self.end_headers()


            print(code[0])


            self.wfile.write(f'Authorization code received: {code}\n'.encode())
            self.wfile.write(f'Wait 10s...\n'.encode())

            time.sleep(10)

            # get token
            token_url = 'https://oauth2.googleapis.com/token'
            payload = {
                'code': code[0],
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code',
            }
            response = requests.post(token_url, data=payload)

            if response.status_code == 200:
                token_info = response.json()
                print("\nAccess Token:", token_info['access_token'])

                self.wfile.write(f'\nSuccessfully: \n{token_info["access_token"]}'.encode())
            else:
                self.wfile.write(f'Failed: {response.text}'.encode())
                print("\nFailed to retrieve token:", response.status_code, response.text)



        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
