import socket as s
import glob
from itertools import islice
import sys
import time

def Find():
    #Pattern = 'C:/**/*.txt'
    Pattern = '*.jpg'
    return list(islice(glob.iglob(Pattern, recursive=True), 4))

def SendFile(sock, filepath):
    f = open(filepath, 'rb')
    datas = 1
    while datas:
        datas = f.read(1024)
        sock.send(datas)

def GetFilename(Msg):
    new = Msg.split('/')
    return new[-1]

def TryToDecode(msg):
    try:
        out = msg.decode()
        return out
    except:
        return -1

def CreateDownl(Socket, Filename):
    print("file--- " + Filename)
    print('aa')
    f = open(Filename, 'wb+')
    while True:
        datas = 1
        while datas:
            print('w for recv')
            datas = Socket.recv(2048)
            eof = "---EOF---EOF---FCSFLAG---"
            out = TryToDecode(datas)
            if out != -1:
                print(datas)
                if eof in TryToDecode(datas):
                    print("rasdadsfdsfsdgjsdfk;gj\n\n")
                    break

            f.write(datas)
            print("sec while recv got")
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
    while True:
        msg = ClientSocket.recv(256).decode() # filename
        if msg == '':
            break
        CreateDownl(ClientSocket, msg)
        print("before 1")
        ClientSocket.send('1'.encode())


def Sender():
    Socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    Socket.connect(("127.0.0.1", 9050))
    list = Find()
    ll = len(list)-1
    print(ll)
    while ll != -1:
        print(list)
        name = GetFilename(list[ll])
        Socket.send(name.encode())
        SendFile(Socket, list[ll])
        time.sleep(2)
        Socket.send("---EOF---EOF---FCSFLAG---".encode())
        list.remove(name)
        print(list)
        print("file done")
        Socket.recv(16)
        print("\n\n"+str(ll))
        ll-=1

    
    


if __name__ == "__main__":

    cs = int(sys.argv[1])

    print(cs)

    if cs==1:
        Sender()

    else:
        Receiver()
