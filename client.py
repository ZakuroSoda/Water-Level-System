import socket
import ctypes
import time
import os
import requests
from requests.structures import CaseInsensitiveDict
try:
    import pyi_splash
except:
    pass
from colorama import init, Fore
init()

mode = True
alarm = False

class Socket:
    """A class that makes a socket to communicate data over TCP/IP. 
       Thanks to the tutorial at https://docs.python.org/3/howto/sockets.html
       for majority of the code. 
       
       Every message must be concluded by an asterisk, to signal that the message is over. 
       """

    def __init__(self, existing=None):
        if existing == None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = existing

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg):
        totalsent = 0
        msg_delimited = str(msg + "*").encode('utf-8')
        while totalsent < len(msg_delimited):
            sent = self.sock.send(msg_delimited[totalsent:])
            if sent == 0:
                raise ConnectionResetError
            totalsent = totalsent + sent

    def receive(self):
        chunks = []
        while True:
            chunk = self.sock.recv(4096)
            if chunk == b'':
                raise ConnectionResetError
            chunks.append(chunk)
            if b"*" in b''.join(chunks):
                break
        return str(b''.join(chunks))[2:-2]

clientSocket = Socket()
try:
    pyi_splash.close()
except:
    pass
while True:
    try:
        clientSocket.connect(input(Fore.RESET + "IP Address of Server: "), 27179)
        break
    except:
        print(Fore.RED + "We could not connect to port 27179 on the given IP address. Please try again... ")

print(Fore.GREEN + "Connected!")
time.sleep(0.5)
os.system('cls')

while True:
    try:
        if mode == True:
            clientSocket.send("0")
            cm = clientSocket.receive()
            if int(cm) >= 4:
                print(Fore.RED + f"Water Level: {cm}cm")
            else:
                print(Fore.GREEN + f"Water Level: {cm}cm")
            time.sleep(0.5)
        else:
            command = input(Fore.RESET + "What would you like to do? ")
            if command == "0" or command.lower() == "rawcm":
                clientSocket.send("0")
                cm = clientSocket.receive()
                if int(cm) >= 4:
                    print(Fore.RED + f"Water Level: {cm}cm")
                else:
                    print(Fore.GREEN + f"Water Level: {cm}cm")
            elif command == "1" or command.lower() == "rawin":
                clientSocket.send("1")
                inches = clientSocket.receive()
                if int(inches) >= 1.57:
                    print(Fore.RED + f"Water Level: {inches}in")
                else:
                    print(Fore.GREEN + f"Water Level: {inches}in")
            elif command == "2" or command.lower() == "alarm":
                clientSocket.send("2")
                ret = clientSocket.receive()
                print(Fore.GREEN + f"Success! ")
            elif command == "3" or command.lower() == "light":
                clientSocket.send("3")
                ret = clientSocket.receive()
                print(Fore.GREEN + f"Success! ")
            elif command == "4" or command.lower() == "pause":
                clientSocket.send("4")
                ret = clientSocket.receive()
                print(Fore.GREEN + f"Success! ")
            elif command == "5" or command.lower() == "sleep":
                clientSocket.send("5")
                ret = clientSocket.receive()
                print(Fore.GREEN + f"Success! ")
                exit(0)
            elif command.lower() == "e":
                raise KeyboardInterrupt
            
        clientSocket.send("0")
        cm = clientSocket.receive()
        if int(cm) >= 4 and alarm == False:
            alarm = True
            ctypes.windll.user32.MessageBoxW(0, "Hello user, your hACker People Water Sensor has detected a high water level. The alarms are sounding. To disable these, enter the shell and use command PAUSE. ", "High water level!", 0)
            headers = CaseInsensitiveDict()
            headers["Content-Type"] = "application/json"
            requests.post("https://prod-10.southeastasia.logic.azure.com:443/workflows/d2ab2be06a9643d6beb9180b5b7b2e0d/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=beOJt0r0sRmbWTr5_AzgcmqacvlUv4D88L1X-OFzjq8", headers=headers, data={})
        elif int(cm) < 4 and alarm == True:
            alarm = False
            ctypes.windll.user32.MessageBoxW(0, "Hello user, your hACker People water sensor has detected that your water level is safe now. For more information, please enter the shell. ", "Normal Water Level.", 0)
    except KeyboardInterrupt:
        mode = mode != True
        print(Fore.BLUE + "Keyboard Interrupt")
        time.sleep(3)
        os.system('cls')
        if mode == False:
            print(Fore.RESET + "Interactive hACker People Shell:\nYou are communicating with the hACker People Water Sensor\nHere's a list of appropriate commands\n    1. 0|RAWCM - Sends the raw data over serial in centimeters\n    2. 1|RAWIN - Sends the raw data over serial in inches\n    3. 2|ALARM - Sound the alarm for 5s, for debugging\n    4. 3|LIGHT - Blink all the LEDs at 2Hz for 5s, for debugging\n    5. 4|PAUSE - Acknowledge high water level and pause alarm\n    6. 5|SLEEP - Sleep the device, stop the sensors and output\n    7. E|^C    - Exit shell and go back to report mode\n")
    except ConnectionResetError:
        print(Fore.RED + "Your connection was aborted. Please attempt to reconnect. ")
        clientSocket = Socket()
        while True:
            try:
                clientSocket.connect(input(Fore.RESET + "IP Address of Server: "), 27179)
                break
            except:
                print(Fore.RED + "We could not connect to port 27179 on the given IP address. Please try again... ")

        print(Fore.GREEN + "Connected!")