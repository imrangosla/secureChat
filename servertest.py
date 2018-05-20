'''
Server Side code
1 - chat
2 - online
3 - offline
'''


from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import subprocess, ssl
from tkinter import messagebox


global selected_users
users = [('admin', 'pass'), ('user', 'pass1'), ('shree', 'shree'), ('jon', 'jon')]
online_users = [
selected_users = []


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        connectstream, client_address = SERVER.accept()

        client = ssl.wrap_socket(connectstream, server_side=True, certfile="server.crt", keyfile="server.key")
        
        print("%s:%s has connected." % client_address)
        #client.send(bytes("Greetings from the cave! Now type your name and press enter!"))
        logincreds = client.recv(BUFSIZ).decode("utf-8")
        try:
            username, password = logincreds.split()
            login = (username, password)
            if login not in users:
                #messagebox.showerror("Invalid Credentials", "Incorrect Username or Password!!!!!!!!")
                client.close()
            else:
                clients[client] = username
                online_users.append(username)
                Thread(target=handle_client, args=(client,)).start()
        except:
            client.close()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    global selected_users

    name = clients[client]
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(welcome.encode())
    broadcastStatus(','.join(online_users))


    while True:
        msg = client.recv(BUFSIZ)

        if msg[0] == '/':
            selected_users = msg.split(',')
            #print(selected_users)
            del selected_users[selected_users.index('/')]    
            #print(selected_users)   
        
        elif msg != "{quit}".encode():
            #print("elif not quit")
            broadcast(msg, name)
        
        else:
            client.send("{quit}".encode())
            client.close()
            del online_users[online_users.index(name)]
            #print("before" , clients)
            del clients[client]
            #print("after", clients)
            broadcast("has left the chat.".encode(), name)
            broadcastStatus(','.join(online_users))
            break


def broadcastStatus(name):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(("2" + name).encode())

def broadcast(msg, prefix=""):  # prefix is for name identification.
    global selected_users
    """Broadcasts a message to all the clients."""
    #print("into broadcast")
    for sock in clients:
        #print("into the for loop")
        #print(clients.get(sock))
        #print(selected_users)
        if clients.get(sock) in selected_users and prefix in selected_users:
            #print("SENDING")
            sock.send((prefix + ": " + msg.decode("utf-8")).encode())
        
clients = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
while True:
    try:
        SERVER.bind(ADDR)
        break
    except:
        subprocess.call(' sudo lsof -t -i tcp:33000 | xargs kill -9', shell = True)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
SERVER.close()