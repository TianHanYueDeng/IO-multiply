
import select
import socket
import queue

server = socket.socket()
server.bind(('localhost',10000))
server.listen(10)
server.setblocking(False)
message_queues = {}
inputs = [server]
outputs = []

while True:
    readable, writeable, exceptional = select.select(inputs, outputs, inputs)
    for r in readable:
        if r is server:
            conn,addr=r.accept()
            print("new connection:",addr)
            inputs.append(conn)
            message_queues[conn] = queue.Queue()
        else:
            try :
                data = r.recv(1024)
                print("%s says: \n %s"%(addr,data.decode()))
                resp=input(">>")
                message_queues[r].put(resp)
                outputs.append(r)
            except ConnectionResetError as e:
                print("connection fails",r)
                if r in outputs:
                   outputs.remove(r)
                inputs.remove(r)
                r.close()
                del message_queues[r]


    for w in writeable:
        next_message = message_queues[w].get(0)
        w.send(bytes(next_message,encoding='utf8'))
        outputs.remove(w)

    for e in exceptional:
        if e in outputs:
            outputs.remove(e)
        inputs.remove(e)
        del message_queues[e]



