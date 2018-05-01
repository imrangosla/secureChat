import socket
from time import sleep


c1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c1.bind(('', 9000))
c1.listen(5)

c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c2.bind(('', 9001))
c2.listen(5)

print("Waiting For Connection")

while True:
    try:
        conn, address = c1.accept()
        print("Connection from Client : ", address)
        conn, address = c2.accept()
        print("Connection from Client : ", address)
        break
    except:
        print("ERROR CONNECTING")
        sleep(3)