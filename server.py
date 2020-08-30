import socket, pickle
from _thread import *
import threading 
import argparse
from server_module import *
import json


# carga de routing table

routing_table = json.load(open('route_table.json'))
node_names = list(routing_table.keys())[::-1] # la lista se pone al revés para asi hacer pop a los primeros nombres de la lista (en lugar de los ultimos)
LIMIT = len(node_names) # cantidad máxima de nodos en la red 
active_nodes = {}
available_nodes = node_names.copy()
# thread_lock = threading.Lock() 

ap = argparse.ArgumentParser()
ap.add_argument("--host", required=False, help="Server IP address.")
ap.add_argument("--port", required=False, help="Port in which the server will be listening.")
ap.add_argument("-a", "--alg", required=False, help="Routing algorithm to be used.")
args = vars(ap.parse_args())

# la ip y el puerto serán automáticamente asumidos si no se brindan en los argumentos
# si no se brinda una IP específica, se asumirá el localhost
host = args["host"] if args["host"] != None else socket.gethostname()
port = int(args["port"]) if args["port"] != None else 5000
alg = args["alg"]


# main loop 
# bind socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((host, port)) 
print("socket binded to port", port) 
# put the socket into listening mode 
s.listen(LIMIT) # cantidad de clientes simultáneos se limita a la cantidad de nodos del grafo 
print("socket is listening") 

# thread function 
def thread_process(c, addr): 
    has_init = True
    while True: 
        # cuando el cliente se conecta, se le envía sus vecinos y los pesos de los links
        if has_init:
            new_node_name = available_nodes.pop()
            new_node = init_node(new_node_name, routing_table[new_node_name], addr[0], addr[1])
            active_nodes[new_node_name] = c
            # envío del nodo correspondiente al cliente 
            c.send(bytes("1||", encoding='ascii'))
            has_init = False

        # data received from client
        data = c.recv(1024) 
        if not data: 
            print('Client from {}:{} exited. Bye!'.format(addr[0], c)) 
            # lock released on exit 
            # thread_lock.release() 
            break

        if data.decode("ascii") == "init":
            print("Sending init node for {}:{}".format(addr[0], addr[1]))
            c.send(pickle.dumps(new_node))
            continue
        message = data.decode("ascii").split("||")
        action = message[0]
        if action == "2": # envio de tabla de ruteo 
            sender = message[1]
            receiver = message[2]
            state = message[3]
            send_route_table(sender, receiver, state, active_nodes)
        elif action == "3": # envio de mensajes 
            print("data received", message)
            sender = message[1]
            receiver = message[2]
            package = message[3]
            success = send_message(sender, receiver, package, active_nodes, routing_table)
            if not success:
                print("Failed to send message. Nodes {} and {} are not connected.".format(sender, receiver))

        # print("Received from client:", message)
        # # reverse the given string from client 
        # msg = "Message '{}' received!".format(message)
        # # send back reversed string to client 
        # c.send(msg.encode("ascii")) 

        # posteriormente, se indica a los nodos cuál es el algoritmo a usar para que actualicen sus tablas de ruteo 

    # connection closed 
    c.close() 

# a forever loop until client wants to exit 
while True: 
    # establish connection with client 
    c, addr = s.accept() 
    # lock acquired by client 
    print("addr",addr)
    # thread_lock.acquire() 
    print('Connected to :', addr[0], ':', addr[1]) 
    # Start a new thread and return its identifier 
    start_new_thread(thread_process, (c,addr,)) 
s.close() 
  