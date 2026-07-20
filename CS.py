import socket as s
import glob
from itertools import islice
import sys

def Find():
    Pattern = 'C:/**/*.txt'
    return list(islice(glob.iglob(Pattern, recursive=True), 2))

def SendFile(sock, filepath):
    f = open(filepath, 'rb')
    datas = f.read(1024)

    while datas:
        sock.send(datas)
        datas = f.read(1024)

def GetFilename(Msg):
    new = Msg.split('/')
    return new[-1]

def CreateDown(Socket, Filename):
    print("file--- " + Filename)
    f = open(Filename, 'wb+')

    while True:
        datas = Socket.recv(1024)
        while datas:
            f.write(datas)
            datas = Socket.recv(1024)
        f.close()
        break
    print("Downloaded...")


def Receiver():
    Socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    Socket.bind(("", 9050))

    Socket.listen(3)

    ClientSocket, Info = Socket.accept()
    print("acc")
    print(Info)

    msg = ""
    while msg != "EOF":
        msg = ClientSocket.recv(256).decode() # filename
        CreateDown(ClientSocket, msg)
        ClientSocket.send('1'.encode())



def Sender():
    Socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    Socket.connect(("127.0.0.1", 9050))
    list = Find()
    ll = len(list)
    for i in range(0, ll):
        name = GetFilename(list[i])
        Socket.send(name.encode())
        SendFile(Socket, list[i])
        Socket.send("EOF".encode())
        print("done")
        Socket.recv(16)

    
    


if __name__ == "__main__":

    cs = int(sys.argv[1])

    print(cs)

    if cs==1:
        Sender()

    else:
        Receiver()