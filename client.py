
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

route_table = json.load(open("route_table.json"))
algorithm = ""

def send_message(sender, receiver, message, path = None):
    if path == None:
        message_to_send = bytes("||".join(["3", sender, receiver, message]), encoding="ascii")
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




while True: 
    #  mensaje recibido del server 
    data = s.recv(BUFFER_LENGTH) 
    message = ""
    try: 
        message = data.decode("ascii").split("||")
        if message[0] == "1":
            algorithm = message[1]
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
        print("path", path)
        self_node_name = path.pop(0) # eliminar el primero de la lista, que es el mismo
        forward_message(self_node_name, package, path)



# cerrar la conexion
s.close() 
  