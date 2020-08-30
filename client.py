
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

def send_message(sender, receiver, message):
    print("IN SEND MESSAGE")
    message_to_send = bytes("||".join(["3", sender, receiver, message, "||"]), encoding="ascii")
    # si el length del mensaje es menor al buffer_length, para evitar que se reciban multiples
    # mensajes como uno solo, se llenará el buffer con caracteres filler para llegar al buffer_length
    missing_bytes = bytes("." * (BUFFER_LENGTH - len(message_to_send)),encoding="ascii")
    s.send(message_to_send + missing_bytes)

while True: 
    #  mensaje recibido del server 
    data = s.recv(BUFFER_LENGTH) 
    message = ""
    try: 
        if data.decode("ascii") == "1||":
            print('Received init from server') 
            s.send(bytes("init", encoding="ascii"))
            continue
        message = data.decode("ascii").split("||")
        if message[0] == "3": # recibe mensaje de un server 
            # print("data decoded", data.decode("ascii"))
            print("Message received: {} / From sender: {}".format(message[2], message[1]))

        
    except:
        self_node = pickle.loads(data)
        print("Node name assigned: {} and neighbors {}".format(self_node.getName(), self_node.getNeighbors()))
        init_node(self_node)
    # implementación de flood (temporal)
    if self_node.getName() == "A":
        package = input("Write message to send: ")
        end = input("Write end node: ")
        hop_limit = int(input("Write depth (hop) limit: "))
        start = get_node().getName()
        flood(route_table, start, end, package, send_message, hop_limit+1)

# cerrar la conexion
s.close() 
  