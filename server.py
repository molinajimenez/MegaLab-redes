import socket
from _thread import *
import threading 
import argparse

# nodes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
node_names = ["A", "B", "C", "D"]
LIMIT = len(node_names) # cantidad máxima de nodos en la red 
active_nodes = []
thread_lock = threading.Lock() 

ap = argparse.ArgumentParser()
ap.add_argument("--host", required=False, help="Server IP address.")
ap.add_argument("--port", required=False, help="Port in which the server will be listening.")
args = vars(ap.parse_args())

# la ip y el puerto serán automáticamente asumidos si no se brindan en los argumentos
# si no se brinda una IP específica, se asumirá el localhost
host = args["host"] if args["host"] != None else socket.gethostname()
port = int(args["port"]) if args["port"] != None else 5000

# thread function 
def thread_process(c,addr): 
    while True: 
        # data received from client 
        data = c.recv(1024) 
        if not data: 
            print('Client from {}:{} exited. Bye!'.format(addr[0], addr[1])) 
            # lock released on exit 
            thread_lock.release() 
            break
        message = data.decode("ascii")
        print("Received from client:", message)
        # reverse the given string from client 
        msg = "Message '{}' received!".format(message)
        # send back reversed string to client 
        c.send(msg.encode("ascii")) 
        # cuando el cliente se conecta, se le envía sus vecinos y los pesos de los links
    # connection closed 
    c.close() 

# main loop 
# bind socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((host, port)) 
print("socket binded to port", port) 
# put the socket into listening mode 
s.listen(LIMIT) # cantidad de clientes simultáneos se limita a la cantidad de nodos del grafo 
print("socket is listening") 

# a forever loop until client wants to exit 
while True: 
    # establish connection with client 
    c, addr = s.accept() 
    # lock acquired by client 
    print("addr",addr)
    thread_lock.acquire() 
    print('Connected to :', addr[0], ':', addr[1]) 
    # Start a new thread and return its identifier 
    start_new_thread(thread_process, (c,addr,)) 
s.close() 
  