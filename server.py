import socket

s=socket.socket()
host=socket.gethostname()
print(host)
port=12345
s.bind((host,port))
s.listen(5)
while True:
    c,addr=s.accept()
    print('GOT THE CONNECTION THROUGH',addr)
    c.send('Thank you for connecting')
    c.close()
