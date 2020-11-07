import socket
from Crypto.Cipher import AES


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
KM_PORT = 4000
B_PORT = 4001
MODE = "OFB"
BLOCK_SIZE = 16
PAD_CHR = '`'
IV = str.encode("abcdefghijklmnop")
FILE_PATH = r'C:\Users\andre\Desktop\IS-master\input.txt'


pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PAD_CHR  # add characters at end of string to pad
unpad = lambda s: s[:s.find(PAD_CHR)]


def byte_xor(byte_array1, byte_array2):
    result = bytearray()
    for b1, b2 in zip(byte_array1, byte_array2):
        result.append(b1 ^ b2)
    return bytes(result)

def encrypt(text, key):
    cipher = AES.new(key, AES.MODE_CFB, iv = IV)
    encrypted_text = cipher.encrypt(text)
    return encrypted_text

def decrypt(encrypted_text, key):
    cipher = AES.new(key, AES.MODE_CFB, iv = IV)
    return cipher.decrypt(encrypted_text)




# GET KEY3
client.connect((host, KM_PORT))
KEY3 = client.recv(16)
print("Received key3: ", end="")
print(KEY3)
client.close()




# GET OK FROM B THAT IT RECEIVED KEY3
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, B_PORT))
msg = client.recv(2)
client.close()



# KM - SEND MODE GET KEY
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, KM_PORT))
client.send(str.encode(MODE))
try:
    cipher = AES.new(KEY3, AES.MODE_CFB, iv = IV)
    ct = client.recv(16)
    KEY = cipher.decrypt(ct)
except ValueError:
    print("Not good")



print("KEY IS ", end="")
print(KEY)
client.close()


#SEND KEY TO B
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, B_PORT))
client.send(str.encode(MODE))
client.send(ct)



#GET COMMUNICATION START MESSAGE AND START COMMUNICATING
go_message = client.recv(2).decode()
if (go_message == 'go'):
    with open(FILE_PATH, "rt+") as f:
        if MODE == "CBC":
            block = f.read(BLOCK_SIZE)
            prev_encrypted_block = IV
            while len(block) != 0:
                block = pad(block)
                xor_block = byte_xor(prev_encrypted_block, str.encode(block))
                encrypted_block = encrypt(xor_block, KEY)
                client.send(encrypted_block)
                print("sent this: ", end=" ")
                print(encrypted_block)
                prev_encrypted_block = encrypted_block
                block = f.read(BLOCK_SIZE)
        
        elif MODE == "OFB":
            block = f.read(BLOCK_SIZE)
            prev_cipher_block = IV
            while len(block) != 0:
                block = pad(block)
                cipher_block = encrypt(prev_cipher_block, KEY)
                xor_block = byte_xor(str.encode(block), cipher_block)
                client.send(xor_block)
                print("sent this: ", end=" ")
                print(xor_block)
                prev_cipher_block = cipher_block
                block = f.read(BLOCK_SIZE)

client.close()