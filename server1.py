import socket
import threading
import sys
import time
import datetime


HOST = '124.0.0.1'
PORT = int(input("Enter the port number to bind with: "))
score = [0, 0 ,0]
totalQuestions = int(input("Enter the total number of questions: "))
filename = input("Enter the name of the quiz file:")
t = [0, 0 ,0]
try:
    f = open(filename, 'r')
except Exception as e:
    print("NO SUCH FILE!")
    sys.exit(0)
isDone = False


def askQuestion(connlist, playerNo, ques, ans):
    global score
    global f
    global t
    global isDone
    connlist[playerNo].sendall("Q\n")
    time.sleep(0.1)
    connlist[playerNo].sendall(ques+"\n")          #sendall question
    time.sleep(0.1)
    start_time=time.time()
    data = connlist[playerNo].recv(1024)                    #receive answer
    t[playerNo] = time.time()
    if t[playerNo]-start_time<=10:
        if (not isDone) and (ans == data + '\n'):
            score[playerNo]+=10
            isDone = not isDone
            connlist[playerNo].sendall("Correct Answer\n")
            time.sleep(0.1)
        else:
            if ans == data + '\n':
                connlist[playerNo].sendall("Too late!\n")
                time.sleep(0.1)
            else:
                connlist[playerNo].sendall("Incorrect Answer\n")
                time.sleep(0.1)
                score[playerNo]-=10
    else:
        connlist[playerNo].sendall("TOO LATE !")


def sendallScore(connlist):
    global score
    for i, conn in enumerate(connlist):
        conn.sendall("S\n")
        time.sleep(0.1)
        conn.sendall("Player "+str(i+1)+", your score is: "+str(score[i])+"\n")
        time.sleep(0.1)
        
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(3)
print ("Server bound to ", HOST, ":", PORT, "\nConnect all players before continuing...")
(conn1, addr) = s.accept()
print ("Connected to Player 1 at ", addr)
(conn2, addr) = s.accept()
(conn3,addr)=s.accept()
connlist = [conn1, conn2, conn3]
conn1.sendall("A\n")
time.sleep(0.1)
conn1.sendall("You are Player 1\n")
time.sleep(0.1)
conn2.sendall("A\n")
time.sleep(0.1)
conn2.sendall("You are Player 2\n")
time.sleep(0.1)
print ("Connected to Player 2 at ", addr)
conn2.sendall("A\n")
time.sleep(0.1)
conn2.sendall("You are Player 3\n")
time.sleep(0.1)
print( "Connected to Player 3 at ", addr)
for questionNo in range(totalQuestions):
    # conn1.sendall("A\n")
    # time.sleep(0.1)
    conn1.sendall("Question Number "+str(questionNo+1)+"\n")
    time.sleep(0.1)
    # conn2.sendall("A\n")
    # time.sleep(0.1)
    conn2.sendall("Question Number "+str(questionNo+1)+"\n")
    time.sleep(0.1)
    # conn3.sendall("A\n")
    # time.sleep(0.1)
    conn3.sendall("Question Number "+str(questionNo+1)+"\n")
    time.sleep(0.1)
    
    ques = f.readline()
    ans = f.readline()
    isDone = False

    playerThread1 = threading.Thread(target = askQuestion, name = "Thread1", args = (connlist, 0, ques, ans,))
    playerThread2 = threading.Thread(target = askQuestion, name = "Thread2", args = (connlist, 1, ques, ans,))
    playerThread3 = threading.Thread(target = askQuestion, name = "Thread3", args = (connlist, 2, ques, ans,))

    playerThread1.start()
    playerThread2.start()
    playerThread3.start()

    playerThread1.join()
    playerThread2.join()
    playerThread3.join()

    # TO DO Buzzer Round Implementation using threading, threading not required for current task
    sendallScore(connlist)
    if score[0]>5 or score[1]>=5 or score[2]>=5:
        break
if score[0]>score[1] and score[0]>score[2]:
    print ("Player 1 won, with score: ", score)
    conn1.sendall("X\n")
    time.sleep(0.1)
    conn1.sendall("YOU WON\n")
    time.sleep(0.1)
    conn2.sendall("X\n")
    time.sleep(0.1)
    conn2.sendall("YOU LOST\n")
    time.sleep(0.1)
    conn3.sendall("X\n")
    time.sleep(0.1)
    conn3.sendall("YOU LOST\n")
elif score[0]<score[1] and score[2]<score[1]:
    print ("Player 2 won, with score: ", score)
    conn2.sendall("X\n")
    time.sleep(0.1)
    conn2.sendall("YOU WON\n")
    time.sleep(0.1)
    conn1.sendall("X\n")
    time.sleep(0.1)
    conn1.sendall("YOU LOST\n")
    time.sleep(0.1)
    conn3.sendall("X\n")
    time.sleep(0.1)
    conn3.sendall("YOU LOST\n")
else:
    print ("Player 3 won,with score: ", score)
    conn3.sendall("X\n")
    time.sleep(0.1)
    conn3.sendall("YOU WON\n")
    time.sleep(0.1)
    conn2.sendall("X\n")
    time.sleep(0.1)
    conn2.sendall("YOU LOST\n")
    time.sleep(0.1)
    conn1.sendall("X\n")
    time.sleep(0.1)
    conn1.sendall("YOU LOST\n")

s.close()