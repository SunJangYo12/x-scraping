# Get original content from url ex. kusonime.com
$ bash getori.sh 

# Link or change original link to shortlink with my payment
$ cd original
$ php -S localhost:1212
new tab
$ python3 scraping.py

Note: pastikan folder out kosong saat pertama menjalankan. shortlink saat ini
menggunakan shrink.me dan ouo.io


# Verifikasi
verifikasi apakah semua sudah di link atau belum.
$ ganti variable di = "out_1"
$ python3 verify.py


# Khusus untuk bloger
dapatkan token api oauth2.0 untuk membuat postingan. pertama edit api_secret dll
$ python3 getToken.py

copy link dan buka di chrome tunggu mendapatkan token
pastekan token di variable access_token.
$ python3 post.py
