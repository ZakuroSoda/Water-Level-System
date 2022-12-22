import serial.tools.list_ports
import serial
import socket

alarmed = False

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

# Identify if there is an Arduino plugged into the laptop
for info in serial.tools.list_ports.comports():
    if "ino" in info[1]:
        port = info[0]
        print(f"hACker People Device on Serial Port {info[0]}.")
        break
else:
    print("There is no Arduino device conneected to your device. \nTry closing the Arduino IDE, etc.")
    exit(0)

try:
    import pyi_splash
    pyi_splash.close()
except:
    pass

sensor = serial.serial_for_url(port)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', 27179))
serverSocket.listen(1)
print("Waiting for a connection on port 27179...")
clientSocket = Socket()
(clientSocket.sock, (ip, tcpport)) = serverSocket.accept()
print(f"We have a connection with ({ip}, {tcpport})")

while True:
    try:
        command = clientSocket.receive()
        if command == "0" or command == "1" or command == "2" or command == "3" or command == "4" or command == "5":
            sensor.write((command + "*").encode('utf-8'))
            sensor.flush()
            clientSocket.send(sensor.read_until(b"/").decode('utf-8')[:-1])
            sensor.reset_input_buffer()
        if command == "5":
            exit(0)
    except ConnectionResetError:
        print("Your connection was aborted. Please attempt to reconnect. ")

        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind(('', 27179))
        serverSocket.listen(1)
        print("Waiting for a connection on port 27179...")
        clientSocket = Socket()
        (clientSocket.sock, (ip, tcpport)) = serverSocket.accept()
        print(f"We have a connection with ({ip}, {tcpport})")