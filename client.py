from genericpath import exists
import sqlite3
import socket
from telnetlib import EL
import threading
import pickle
import time
from getpass import getpass
import stdiomask
import sys
import os
#from bcrypt import gensalt, hashpw,checkpw

def CreateServerAddr(): 
    try:
        if(not os.path.exists(".ServerAddress.txt")):
            f = open(".ServerAddress.txt", "w")
            f.write("localhost:9999")
            f.close()
    except Exception as E:
        print("Error Create Server Addr: " + str(E))
    
def editServerAddress(): 
    print("Hi Admin")
    try:        
        addrHandle = open(".ServerAddress.txt","r")
        IP = addrHandle.readline().split(":")
        print(f"Current Adress \nIP: {IP[0]} \nPORT: {IP[1]} ")
        ch = input("Do you want to change Server IP and port? [y/n] ")
        addrHandle.close()
        if(ch[0].lower() == "y"):
            IPAddr = input("Enter new IP Address: ")
            PortNumber = input("Enter new port number: ")
            addrHandle = open(".ServerAddress.txt","w")
            addrHandle.write(IPAddr + ":" + PortNumber)
            print("IP Changed successfully\n")
    except Exception as E:
        if "[Errno 2] No such file or directory" in str(E):
            print("File doesnt exists")
            CreateServerAddr()

        print("Error Occured: " + str(E))
        sys.exit()


c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

setChoice = input("WELCOME\nPress enter to continue... ")
CreateServerAddr()
if(setChoice == "_settings"):
    editServerAddress()

print("Trying to connect with server...")
try:
    addrHandle = open(".ServerAddress.txt","r")
    IP = addrHandle.readline().split(":")
    #print(IP)
    c.connect_ex((IP[0], int(IP[1])))
    print("Connection Established")
    c.send(f"Host Device Name: {socket.gethostname()}, Host IP Address: {socket.gethostbyname(socket.gethostname())}".encode('utf-8'))
except:
    print("Something went wrong\nDisconnecting...")
    sys.exit()

print("\n\t\tWelcome!\t\t")
h = input("Login[L] or Signup[S]: ")

def login():
    name = username
    pwd = password
    ld = pickle.dumps([username, password])
    c.send("login".encode('utf-8'))
    c.send(ld)
    ack = c.recv(1024).decode('utf-8')
    if ack == "allok":
        print("\nLogin Successfull")
        print(f"NOTE: \nTo quit: {name.lower()}exitchat\n")
        thrd()
    elif ack == "null":
        print("Invalid Username or Password!")
        sys.exit()
    elif ack == "loggedin":
        print(f"{name} already Logged in!")
        time.sleep(1)
        print("Do not try to login into somebody else's profile!")
        sys.exit()
    else:
        print("Something went wrong at Log In! Rerun the system")
        sys.exit()

def shutdown():
    print("Admin ran server shutdown")
    print("Server will shutdown in 10secs")
    time.sleep(7)
    print("Exiting...")
    c.close()
    os._exit(0)



def signup():
    ld = pickle.dumps([username, password])
    c.send("signup".encode('utf-8'))
    c.send(ld)
    ack = c.recv(1024).decode('utf-8')
    if ack == "allok":
        print("Signup Successfull")
    elif ack == "exist":
        print("Username already taken!")
    else:
        print("Something went wrong at Sign up! Rerun the system")
        sys.exit()


def kickout():
    print("Admin kicked you out! Bye..")
    time.sleep(4)
    os._exit(0)

def recieve():
    while True:
        try:
            message = c.recv(1024).decode('utf-8')
            if message == "ssd":
                shutdown()
            elif f"[admin]: kick {username}" == message:
                kickout()
            elif f"[admin]: kick" == message[0:13]:
                t = message.split(" ")[-1]
                print(f"Admin Kicked out {t}")
            elif f"{username} joined the chat" in message:
                print(f"{username} joined the chat")
            elif message[-5:-1] != "allok":
                print(f"{message}")
        except:
            print("An error occurred")
            c.close()
            break


def write():
    while True:
        message = f"[{username}]: {input('')}"
        if f"[{username}]: {username.lower()}exitchat" == message:
            #c.send(f"{username}: Exiting... Bye!".encode('utf-8'))
            print("Please wait! Exiting...")
            time.sleep(1)
            os._exit(0)

        c.send(message.encode('utf-8'))


def thrd():
    tr = threading.Thread(target=recieve)
    tr.start()

    tw = threading.Thread(target=write)
    tw.start()


if h == 'L' or h == 'l' or h == " " or h == "":
    print("LOGIN")
    username = input("Enter your username: ")
    try:
        #print(2/0)  #stdiomask doesnt work in pycham so put this exception purposely! If executing in cmd remove/comment this exception!
        password = stdiomask.getpass(prompt='Enter your password: ', mask='*')
    except:
        password = input("Enter your password: ")
    login()
elif h == "S" or h == "s" or h == "  ":
    print("SIGNUP")
    username = input("Enter a username: ")
    try:
        #print(2/0)
        password = stdiomask.getpass(prompt='Enter Password: ', mask='*')
        p1 = stdiomask.getpass(prompt='Re-enter Password: ', mask='*')
    except:
        password = input("Enter a Password: ")
        if len(password) < 4:
            print("Password too small!")
            sys.exit()
        p1 = input("Re-enter a Password: ")

    if password == p1:
        signup()
    else:
        print("Enter password correctly! ")
        sys.exit()
else:
    print("Invalid Input")
