import socket

SERVER = "192.168.43.32"
FORMAT = "utf-8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, 5500))
print(f"[CONNECTED] to {SERVER}")
print(f"[RECEIVING DATA]")

#RECEIVE TOTAL NO OF FILES

totalfiles = client.recv(1024).decode(FORMAT)
totalfiles = int(totalfiles)
print(f"Received Total files: {totalfiles}")

for fileno in range(totalfiles):
    #RECEIVE FILE SIZE
    while True:
        filenamesize = client.recv(1024).decode(FORMAT)
        if filenamesize:
            filenamesize = int(filenamesize)
            break
    print(f"Filenamesize: {filenamesize}")

    #RECEIVE FILE NAME
    filename = client.recv(filenamesize).decode(FORMAT)
    print(f"Filename: {filename}")

    #RECEIVE DATA
    f = open(filename, "wb")
    while True:
        datas = client.recv(1024)
        while datas:
            f.write(datas)
            datas = client.recv(1024)
            if datas == "!DISCONNECT".encode():
                print(f"Transfer Success for file {filename}")
                break
        f.close()
        break
    print(f"[FILE RECEIVED]: {filename}")
    continue
print("[DONE RECEIVING]")