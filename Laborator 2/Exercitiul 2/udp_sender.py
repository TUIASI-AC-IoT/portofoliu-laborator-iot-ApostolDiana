import socket
import time

# Completati cu adresa IP a platformei ESP32
PEER_IP = "192.168.89.27"
PEER_PORT = 10001


MESSAGE_GPIO1 = b"GPIO4=1"
MESSAGE_GPIO0 = b"GPIO4=0"
i = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while 1:
    try:
        #TO_SEND = MESSAGE + bytes(str(i%2),"ascii")
        #sock.sendto(TO_SEND, (PEER_IP, PEER_PORT))      
        #print("Am trimis mesajul: ", TO_SEND)
        #i = i + 1

        sock.sendto(MESSAGE_GPIO0,  (PEER_IP, PEER_PORT))
        print("Am trimis mesajul: ", MESSAGE_GPIO0)
        time.sleep(2)

        sock.sendto(MESSAGE_GPIO1,  (PEER_IP, PEER_PORT))
        print("Am trimis mesajul: ", MESSAGE_GPIO1)
        time.sleep(2)

       
    except KeyboardInterrupt:
        break