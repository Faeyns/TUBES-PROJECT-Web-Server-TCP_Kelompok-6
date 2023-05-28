# Mengimport semua simbol dari modul socket
from socket import *
# Mengimport modul sys
import sys 

# Membuat objek serverHost menggunakan fungsi socket()
# dengan AF_INET: Menggunakan protokol IPv4 dan SOCK_STREAM: Menggunakan TCP sebagai protokol transport
serverHost = socket(AF_INET, SOCK_STREAM)
# Menentukan nomor port untuk server
serverPort = 3275

# Melakukan binding serverHost ke alamat IP yang tersedia dan nomor port yang ditentukan
serverHost.bind(('', serverPort))
# Mendengarkan koneksi masuk dari client
# Parameter 1 menentukan jumlah koneksi yang dapat ditangani secara simultan
serverHost.listen(1)

while True:
    # Memberikan pesan server sudah ready
    print('Server is Ready')
    
    # Menerima koneksi dari client dan mengembalikan objek socket koneksi (connectionSocket) dan alamat client (addr)
    connectionSocket, addr = serverHost.accept()
    try:
        # Mengambil nama file yang diminta dan mencari file di sistem file
        name = connectionSocket.recv(1024)
        # Membagi data yang diterima menjadi sebuah list kata menggunakan spasi sebagai pemisah
        filename = name.split()[1]
        # Mencetak nama file yang diminta
        print(filename)
        # Mengecek jika terdapat nama file yang diminta dengan mengecek input '/'
        if filename == b'/':
            raise Exception
        # Membuka file yang diminta dalam mode baca biner dengan menggunakan statement 'with'
        # dan menghasilkan file objek yang disimpan dalam variabel 'f'
        with open(filename[1:], "rb") as f:
            # Membaca semua isi file dan menyimpannya dalam variabel 'outputdata'
            outputdata = f.read()

        # Mengirim satu baris header HTTP dengan status 200 OK ke socket
        header = b'HTTP/1.1 200 OK\r\n\r\n'
        # Mengirimkan data yang terdiri dari header HTTP dan outputdata ke socket client
        connectionSocket.send(header + outputdata)
        # Mencetak pesan bahwa respon telah selesai dan menunggu server
        print('Response done, waiting for server...\n')

        # Menutup socket client
        connectionSocket.close()
    
    except IOError:
        # Mengirimkan respon untuk halaman 404 tidak ditemukan
        filename = b'/NotFoundPage.html'
        # Membuka file yang diminta dalam mode baca biner dengan menggunakan statement 'with'
        # dan menghasilkan file objek yang disimpan dalam variabel 'f'
        with open(filename[1:], "rb") as f:
            # Membaca isi file yang diminta dan menyimpannya dalam variabel 'outputdata'
            outputdata = f.read()

        # Mengirim satu baris header HTTP dengan status 404 Not Found ke socket
        header = b'HTTP/1.1 404 Not Found\r\n\r\n'
        # Mengirimkan data yang terdiri dari header HTTP dan outputdata ke socket client
        connectionSocket.send(header + outputdata)
        # Mencetak pesan bahwa respon telah selesai dan menunggu server
        print('Response done, waiting for server...\n')

        # Menutup socket client
        connectionSocket.close()
    
    except Exception:
        # Mengirimkan respon untuk halaman landing
        filename = b'/WelcomePage.html'
        # Membuka file yang diminta dalam mode baca biner dengan menggunakan statement 'with'
        # dan menghasilkan file objek yang disimpan dalam variabel 'f'
        with open(filename[1:], "rb") as f:
            # Membaca isi file yang diminta dan menyimpannya dalam variabel 'outputdata'
            outputdata = f.read()

        # Mengirim satu baris header HTTP dengan status 200 OK ke socket
        header = b'HTTP/1.1 200 OK\r\n\r\n'
        # Mengirimkan data yang terdiri dari header HTTP dan outputdata ke socket client
        connectionSocket.send(header + outputdata)
        # Mencetak pesan bahwa respon telah selesai dan menunggu server
        print('Response done, waiting for server...\n')

        # Menutup socket client
        connectionSocket.close()

# Menutup socket server
serverHost.close()
# Mengakhiri Program
sys.exit()
