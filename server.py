import sqlite3
import socket
import threading
import pickle
import aess
import time
import os
#Password is AES encrypted! Username is used as key for encryption
host = 'localhost'
port = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen()
clients = []
nicknames = []
print("Waiting for a connection... ")


def broadcast(message):
    if message != "allok":
        for client in clients:
            try:
                client.send(message)
            except Exception as E:
                print("Broadcast Error: ",E,"for client ",client)

def shutdown():
    print("Server about to shutdown")
    message = "ssd"
    broadcast(message.encode('utf-8'))
    time.sleep(15)
    os._exit(0)


def kickout(m):
    nm = m.split(" ")[-1]
    k = "[admin]: kick " + nm
    print(f"Admin kicked out {nm}")
    broadcast(k.encode('utf-8'))


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if message.decode('utf-8') == "[admin]: cmd server shutdown":
                shutdown()
            if "[admin]: cmd kick" == message.decode('utf-8')[0:17]:
                kickout(message.decode('utf-8'))
            else:
                broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} has left the chat".encode('utf-8'))
            print(f"{nickname} has left the chat!")
            nicknames.remove(nickname)
            break


def receive():
    while True:
        c, a = s.accept()
        print("Client Connected:  ", str(a))
        try:
            m1 = c.recv(1024).decode('utf-8')
        except:
            print("Some error occurred at receive block.")
            continue
        if m1 == "login":
            m2 = c.recv(1024)
            ack = login(m2)
            c.send(ack.encode('utf-8'))
            m2 = pickle.loads(m2)
            if ack == "allok":
                nickname = m2[0]
                nicknames.append(nickname)
                clients.append(c)
                broadcast(f"{nickname} joined the chat ".encode('utf-8'))
                thread = threading.Thread(target=handle, args=(c,))
                thread.start()

            elif ack == "null":
                print("Something Went Wrong")

        elif m1 == "signup":
            m2 = c.recv(1024)
            ack = signup(m2)
        else:
            ack = "invalid"

        c.send(ack.encode('utf-8'))



def signup(m2):
    conn = sqlite3.connect('user.db')
    m2 = pickle.loads(m2)
    username = m2[0]
    pwd = m2[1]
    password = aess.encrypt(pwd, username)
    cc = conn.cursor()
    try:
        cc.execute("CREATE TABLE IF NOT EXISTS userdetails (username text NOT NULL UNIQUE,password text NOT NULL)")
        cc.execute('INSERT INTO userdetails (username, password) VALUES (?,?)', (username, password,))
    except Exception as E:
        if str(E) == "UNIQUE constraint failed: userdetails.username":
            print("Username already exists")
            conn.close()
            return "exist"

        print("Inserting Data Error: ", E)
        conn.close()
        return "null"


    conn.commit()
    print(f"{username} Signed Up successfully!")
    conn.close()
    x = "allok"
    return x


def login(m2):
    conn = sqlite3.connect('user.db')
    m2 = pickle.loads(m2)
    username = m2[0]
    pwd = m2[1]
    password = aess.encrypt(pwd, username)
    cc = conn.cursor()
    if username not in nicknames:
        try:
            cc.execute("""SELECT username,password FROM userdetails WHERE username=? AND password=?""", (username, password))

            if cc.fetchone() == None:
                x = "null"
                print(f"Login Failed. Username: {username}")
            else:
                x = "allok"
                print(f"{username} Logged in ")

        except:
            print("Error While Checking for Username And Password in Database")

    else:
        x = "loggedin"
        print(f"Somebody tried to login using {username}'s credentials!")

    conn.commit()
    conn.close()

    return x

receive()
