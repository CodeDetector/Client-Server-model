import socket
import sys
import time 

def question(s):
    ques=s.recv(1024)
    print(ques)
    ans=input("Answer : ")
    while ans not in ['A','B','C','D']:
        print("Enter a valid choice")
        ans=input("Answer : " )
    s.sendall(ans)
    response=s.recv(1024)
    print( response )   

def scores(s):
    prompt=s.recv(1024)
    print(prompt)

def final(s):
    prompt=s.recv(1024)
    print(prompt)

HOST='124.0.0.1'  
PORT=int(input("Enter the port number"))
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))

while True:
    start_time=time.time()
    choice=s.recv(1024)
    if choice[0]=="Q":
        question(s)
    elif choice[0]=="S":
        scores(s)
    elif choice[0]=="X" :
        final(s)
        break
    elif choice[0]=="A":
        final(s)
    else:
        print("invalid ")             
