
import socket, argparse, pickle, json
from algorithms import * 
from _thread import *
from threading import Thread
from time import sleep

BUFFER_LENGTH = 1024
ap = argparse.ArgumentParser()
ap.add_argument("--host", required=False, help="Server IP address.")
ap.add_argument("--port", required=False, help="Port in which the server will be listening.")
args = vars(ap.parse_args())

# la ip y el puerto serán automáticamente asumidos si no se brindan en los argumentos
# si no se brinda ip se asumirá que el cliente y el server están en la misma PC
host = args["host"] if args["host"] != None else socket.gethostname()
port = int(args["port"]) if args["port"] != None else 5000
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
# conectar al server 
s.connect((host,port)) 

route_table = {}
algorithm = ""

def send_message(sender, receiver, message, path = None, heartbeat = False):
    if path == None:
        message_to_send = bytes("||".join(["3", sender, receiver, message, "||"]), encoding="ascii")
    elif heartbeat == False:
        message_to_send = bytes("||".join(["3", sender, receiver, message, ":".join(path),"||"]), encoding="ascii")
    else:
        message_to_send = bytes("||".join(["2", sender, receiver, message, ":".join(path),"||"]), encoding="ascii")
    # si el length del mensaje es menor al buffer_length, para evitar que se reciban multiples
    # mensajes como uno solo, se llenará el buffer con caracteres filler para llegar al buffer_length
    missing_bytes = bytes("." * (BUFFER_LENGTH - len(message_to_send)),encoding="ascii")
    s.send(message_to_send + missing_bytes)

def forward_message(sender, message, path, heartbeat = False):
    next_node = path.pop(0)
    if next_node and not heartbeat: # si el mensaje a mandar es uno plano 
        print("Forwarding message '{}' to node {}".format(message,next_node))
        send_message(get_node().getName(), next_node, message, path)
    elif next_node and heartbeat: # si el mensaje a reenviar es una tabla de ruteo
        print("Sending route table of node {} to {}".format(sender, next_node))
        send_message(get_node().getName(), next_node, message, path, heartbeat)
    elif not next_node and heartbeat: # si el mensaje que se recibio es tabla de ruteo
        state = json.loads(message)
        print("State of node {} received: {} / From sender: {}".format(list(state.keys())[0], state, sender))
    else: # si el mensaje que se recibió es uno plano
        print("Message received: {} / From sender: {}".format(message, sender))

def writing_thread():
    while True:
        global algorithm
        global route_table
        # todo lo siguiente debe hacerse en otro thread, que es el que pide input al usuario y hace algo con eso 
        # ya con multithread se elimina la condición de "getName == A"
        if algorithm =="flood":
            sleep(5)
            package = input("Write message to send: ")
            end = input("Write end node: ")
            hop_limit = int(input("Write depth (hop) limit: "))
            start = get_node().getName()
            flood(route_table, start, end, package, send_message, hop_limit+1)
        elif algorithm == "dvr":
            sleep(5)
            routing_dic = dvrouting(route_table, get_node().getName())
            # enviar mensaje?
            package = input("Write message to send: ")
            end = input("Write end node: ")
            start = get_node().getName()
            path = dvr_find_path(start, end, routing_dic[end][1], routing_dic)
            print("Best path chosen by DVR:", path)
            self_node_name = path.pop(0) # eliminar el primero de la lista, que es el mismo
            forward_message(self_node_name, package, path)
        # tabla de ruteo ya la manda el server nomas se conecta el nodo 
        elif algorithm == "lsr":
            sleep(5)
            package = input("Write message to send: ")
            start = input("Write y to start: ")
            # se asume que todos los nodos de la red la están conectados 
            # se envía el estado del nodo a todos los demás
            paths = {}
            # envio de la tabla va en un tercer thread (o el thread de listening)
            # el heartbeat se puede mandar aunque los clientes estén conectados o no
            self_node_name = get_node().getName()
            for node in route_table.keys():
                if node != self_node_name:
                # obtener el path más corto a los demás nodos 
                    paths[node] = dijkstra(route_table, get_node().getName(), node)
                    print("Shortest path from {} to {} by Dijkstra: {}".format(self_node_name, node, paths[node]))
                    print("Sending route table to", node)
                    paths[node].pop(0) # sacar a el mismo nodo del path
                    forward_message(self_node_name, json.dumps(get_node().getState()), paths[node], True)

def listening_thread():
    while True: 
        """ 
            TODO separar cliente en dos threads, uno que escuche lo que manda el server y 
            otro que pida input al user. 
        """
        #  mensaje recibido del server 
        data = s.recv(BUFFER_LENGTH) 
        message = ""
        global algorithm
        global route_table
        try: 
            message = data.decode("ascii").split("||")
            if message[0] == "1":
                algorithm = message[1]
                route_table = json.loads(message[2])
                print('Received init from server') 
                s.send(bytes("init", encoding="ascii"))
                continue

            elif message[0] == "2": # recibe mensaje del server 
                path = message[3].split(":")
                forward_message(message[1], message[2], path, True)
            elif message[0] == "3": # recibe mensaje del server 
                if len(message) > 3: # el mensaje que recibio es para alguien mas
                    path = message[3].split(":")
                    forward_message(message[1], message[2], path)
                else:
                    print("Message received: {} / From sender: {}".format(message[2], message[1]))
            
        except:
            self_node = pickle.loads(data)
            print("Node name assigned: {} and neighbors {}".format(self_node.getName(), self_node.getNeighbors()))
            init_node(self_node)
            

thread1 = Thread(target=listening_thread, args = ())
thread2 = Thread(target=writing_thread, args = ())
thread1.start()
thread2.start()

thread1.join()
thread2.join()
s.close() 
  