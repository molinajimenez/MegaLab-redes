
# Import socket module 
import socket, argparse, pickle, json
from algorithms import * 

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

# route_table = json.load(open("route_table.json"))
route_table = {}
algorithm = ""

def send_message(sender, receiver, message, path = None):
    if path == None:
        message_to_send = bytes("||".join(["3", sender, receiver, message, "||"]), encoding="ascii")
    else:
        message_to_send = bytes("||".join(["3", sender, receiver, message, ":".join(path),"||"]), encoding="ascii")
    # si el length del mensaje es menor al buffer_length, para evitar que se reciban multiples
    # mensajes como uno solo, se llenará el buffer con caracteres filler para llegar al buffer_length
    missing_bytes = bytes("." * (BUFFER_LENGTH - len(message_to_send)),encoding="ascii")
    s.send(message_to_send + missing_bytes)

def forward_message(sender, message, path):
    # try:
    next_node = path.pop(0)
    if next_node:
        print("Forwarding message '{}' to node {}".format(message,next_node))
        send_message(get_node().getName(), next_node, message, path)
    else:
        print("Message received: {} / From sender: {}".format(message, sender))
    # except:
    #     print("Received message '{}' from node {}".format(message, sender))

# def send_state(sender, receiver, state):
#     state_str = json.dumps(state)
#     message_to_send = bytes("||".join(["2", sender, receiver, state_str]), encoding="ascii")
#     missing_bytes = bytes("." * (BUFFER_LENGTH - len(message_to_send)),encoding="ascii")
#     s.send(message_to_send + missing_bytes)

# def receive_state(sender, state):
#     # primero se obtiene el estado y se verifica si no esta dentro del route_table (seria un nodo nuevo)
#     nodes = route_table.keys()
#     new_node_name = state.keys()[0]
#     if new_node_name not in nodes:
#         route_table[new_node_name] = state[new_node_name]

# def find_neighbors_rt():
#     not_in_table = []
#     for neighbor in self_node.getNeighbors().keys():
#         if neighbor not in route_table.keys():
#             not_in_table.append(neighbor)
#     return not_in_table

while True: 
    """ 
        TODO separar cliente en dos threads, uno que escuche lo que manda el server y 
        otro que pida input al user. 

        También falta probar rutas inversas de envío de mensajes (osea hemos hecho A -> C pero no C -> A)
    """
    #  mensaje recibido del server 
    data = s.recv(BUFFER_LENGTH) 
    message = ""
    try: 
        message = data.decode("ascii").split("||")
        if message[0] == "1":
            algorithm = message[1]
            route_table = json.loads(message[2])
            print('Received init from server') 
            s.send(bytes("init", encoding="ascii"))
            continue
        elif message[0] == "3": # recibe mensaje de un server 
            if len(message) > 3: # el mensaje que recibio es para alguien mas
                path = message[3].split(":")
                forward_message(message[1], message[2], path)
            else:
                print("Message received: {} / From sender: {}".format(message[2], message[1]))
        
    except:
        self_node = pickle.loads(data)
        print("Node name assigned: {} and neighbors {}".format(self_node.getName(), self_node.getNeighbors()))
        init_node(self_node)
    # implementación de flood (temporal)
    if algorithm =="flood" and self_node.getName() == "A":
        package = input("Write message to send: ")
        end = input("Write end node: ")
        hop_limit = int(input("Write depth (hop) limit: "))
        start = get_node().getName()
        flood(route_table, start, end, package, send_message, hop_limit+1)
    elif algorithm == "dvr" and self_node.getName() == "A":
        routing_dic = dvrouting(route_table, get_node().getName())
        # print("route table", routing_dic)
        # enviar mensaje?
        package = input("Write message to send: ")
        end = input("Write end node: ")
        start = get_node().getName()
        path = dvr_find_path(start, end, routing_dic[end][1], routing_dic)
        print("Best path chosen by DVR:", path)
        self_node_name = path.pop(0) # eliminar el primero de la lista, que es el mismo
        forward_message(self_node_name, package, path)
    # tabla de ruteo ya la manda el server nomas se conecta el nodo 
    # elif algorithm == "lsr" and self_node.getName() == "A":
        # route_table = self_node.getState()
        # neighbor = self_node.getNeighbors().keys()
        # missing_neighbors = find_neighbors_rt()
        # while missing_neighbors: # mientras todavía no tenga el estado de sus vecinos 
        #     for node in missing_neighbors:
        #         # send_state(self_node.getName(), node, self_node.getState())
        #         send_self_node(self_node.getName(), send_state)
        #     missing_neighbors = find_neighbors_rt()
        




# cerrar la conexion
s.close() 
  