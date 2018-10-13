import socket
client = socket.socket()

client.connect(('localhost', 10000))

while True:
    cmd = input('>>> ').strip()
    if len(cmd) == 0 :
        continue
    client.send(bytes(cmd,encoding='utf8'))
    data = client.recv(1024)
    print(data.decode())

client.close()