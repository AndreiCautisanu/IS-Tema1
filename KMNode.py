import socket
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Random import get_random_bytes



PORT = 4000
PAD_CHR = '`'
BLOCK_SIZE = 16
KEY1 = get_random_bytes(BLOCK_SIZE)
KEY2 = get_random_bytes(BLOCK_SIZE)
KEY3 = get_random_bytes(BLOCK_SIZE)
IV = str.encode("abcdefghijklmnop")


#pad and unpad functions
pad = lambda s: s.decode() + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PAD_CHR  # add characters at end of string to pad
unpad = lambda s: s[:s.find(PAD_CHR)]


#################################################################################


#set up server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
server.bind((host, PORT))

server.listen()


# initial connections, send both A and B key3
for i in [0, 1]:
    client, address = server.accept()
    print("connection from " + str(address))

    client.send(KEY3)
    print("sent key3: ", end=" ")
    print(KEY3)
    client.close()


# A connects to communicate MODE, send corresponding key
client, address = server.accept()
print("connection from " + str(address))

cmode = client.recv(10)
mode = cmode.decode()
print(mode)

cipher = AES.new(KEY3, AES.MODE_CFB, iv = IV)

if (mode == "CBC"):
    cryptMessage = cipher.encrypt(KEY1)
elif (mode == "OFB"):
    cryptMessage = cipher.encrypt(KEY2)

client.send(cryptMessage)
client.close()
server.close()
