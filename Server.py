import socket
import os
import glob
import time

HEADER = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

filepath = os.getcwd() + "/Files"
# for filename in os.listdir(filepath):
#     print(os.path.join(filepath, filename))

SERVER = "192.168.43.32"
# SERVER1 = socket.gethostbyname(socket.gethostname())
# print(SERVER1)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, 5500))

#SERVER LISTENING
server.listen(10)
print(f"Server Listening on {SERVER}")

#SERVER CONNECTED TO CLIENT
conn, addr = server.accept()
print(f"{addr} connected.")

# SEND TOTAL NO OF FILES
filetotal = len(os.listdir(filepath))
filetotal1024 = str(filetotal).encode(FORMAT) + b" " * (HEADER - filetotal)
conn.send(filetotal1024) 
print(f"SEND 1: Sent Encoded filetotal, {filetotal}")

#SENDING DATA
for filename in os.listdir(filepath):
    fileaddr = os.path.join(filepath, filename)
    with open(fileaddr, 'rb') as f:
        # print(f"[SENDING FILE]: {filename}")

        # SEND SIZE OF NAME
        # namesize = os.path.getsize(fileaddr)
        namesize = len(filename)
        namesize = str(namesize).encode(FORMAT)
        namesize += b" " * (HEADER - len(namesize))
        print(f"SEND 2: Encoded Namesize: {int(namesize.decode(FORMAT))}")
        time.sleep(0.5)
        conn.send(namesize)

        # SEND NAME
        print(f"SEND 3: Encoded Filename: {filename}")
        conn.send(filename.encode(FORMAT))

        # SEND DATA
        print(f"SEND 4: Data")
        datas = f.read(1024)
        while datas:
            conn.send(datas)
            datas = f.read(1024)
        f.close()
        conn.send(DISCONNECT_MESSAGE.encode(FORMAT))
        
        print("[DONE SENDING]")
        time.sleep(0.5)
        
print("DONE")
