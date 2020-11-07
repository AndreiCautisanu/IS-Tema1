import socket
from Crypto.Cipher import AES

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
KM_PORT = 4000
PORT = 4001
MODE = ""
BLOCK_SIZE = 16
PAD_CHR = '`'
IV = str.encode("abcdefghijklmnop")
FILE_PATH = r'C:\Users\andre\Desktop\IS-master\output.txt'


pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PAD_CHR  # add characters at end of string to pad
unpad = lambda s: s[:s.find(PAD_CHR)]

def byte_xor(byte_array1, byte_array2):
    result = bytearray()
    for b1, b2 in zip(byte_array1, byte_array2):
        result.append(b1 ^ b2)
    return bytes(result)

def encrypt(text, key):
    #text = str.encode(text)
    cipher = AES.new(key, AES.MODE_CFB, iv = IV)
    encryptedtext = cipher.encrypt(text)
    return encryptedtext

def decrypt(encryptedtext, key):
    cipher = AES.new(key, AES.MODE_CFB, iv = IV)
    return cipher.decrypt(encryptedtext)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
server.bind((host, PORT))


#GET KEY3
client.connect((host, KM_PORT))
KEY3 = client.recv(16)
print("Received key3: ", end="")
print(KEY3)



# A CONNECTS TO GET GO AHEAD FOR GETTING K1/K2 (making sure B got key3)
server.listen()
client, address = server.accept()
print("connection from " + str(address))
client.send(str.encode("go"))
client.close()



# GET K1/K2 FROM A
server.listen()
client, address = server.accept()
print("connection from " + str(address))

MODE = client.recv(3).decode()

cipher = AES.new(KEY3, AES.MODE_CFB, iv = IV)
ct = client.recv(16)
print(ct)
KEY = cipher.decrypt(ct)

print("KEY IS ")
print(KEY)


# SEND COMMUNICATION START MESSAGE AND START COMMUNICATING
client.send(str.encode('go'))

with open(FILE_PATH, "wb+") as f:

    print("mode is " + MODE)

    if MODE == "CBC":
        encrypted_block = client.recv(BLOCK_SIZE)
        prev_encrypted_block = IV


        while(len(encrypted_block) != 0):
            print("received this : ", end="")
            print(encrypted_block)

            decrypted_block = decrypt(encrypted_block, KEY)
            decrypted_block = byte_xor(prev_encrypted_block, decrypted_block)
            print(decrypted_block)
            f.write(decrypted_block)
            prev_encrypted_block = encrypted_block
            encrypted_block = client.recv(BLOCK_SIZE)


    elif MODE == "OFB":
        block = client.recv(BLOCK_SIZE)
        prev_cipher_block = IV


        while len(block) != 0:
            print("received this : ", end="")
            print(block)

            cipher_block = encrypt(prev_cipher_block, KEY)
            xor_block = byte_xor(cipher_block, block)
            f.write(xor_block)
            prev_cipher_block = cipher_block
            block = client.recv(BLOCK_SIZE)


client.close()