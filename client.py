
# Import socket module 
import socket, argparse, pickle, json
from algorithms import * 

ap = argparse.ArgumentParser()
ap.add_argument("--host", required=False, help="Server IP address.")
ap.add_argument("--port", required=False, help="Port in which the server will be listening.")
args = vars(ap.parse_args())

# la ip y el puerto serán automáticamente asumidos si no se brindan en los argumentos
# si no se brinda ip se asumirá que el cliente y el server están en la misma PC
host = args["host"] if args["host"] != None else socket.gethostname()
port = int(args["port"]) if args["port"] != None else 5000
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
# connect to server on local computer 
s.connect((host,port)) 

route_table = json.load(open("route_table.json"))
def send_message(sender, receiver, message):
    print("IN SEND MESSAGE")
    s.send(bytes("||".join(["3", sender, receiver, message]), encoding="ascii"))

while True: 
    # message received from server 
    data = s.recv(1024) 
    message = ""
    try: 
        if data.decode("ascii") == "1||":
            print('Received init from server') 
            s.send(bytes("init", encoding="ascii"))
            continue
        message = data.decode("ascii").split("||")
        # print the received message 
        # print('Received from the server :',str(data.decode('ascii'))) 
        # aqui se implementan los algoritmos 
        # en el caso de flood, devuelve una lista de pares de vertices
        # for hop in path:
        #     s.send(bytes("||".join(["3", hop[0], hop[1], package]), encoding="ascii"))
        if message[0] == "3": # recibe mensaje de un server 
            print("data decoded", data.decode("ascii"))
            print("Message received:", message[1])

        
    except:
        self_node = pickle.loads(data)
        print("Node name assigned: {} and neighbors {}".format(self_node.getName(), self_node.getNeighbors()))
        init_node(self_node)
    
    if self_node.getName() == "A":
        package = input("Write message to send: ")
        end = input("Write end node: ")
        hop_limit = int(input("Write depth (hop) limit: "))
        start = get_node().getName()
        flood(route_table, start, end, package, send_message, hop_limit+1)

    # # ask the client whether he wants to continue 
    # ans = input('\nDo you want to continue(y/n) :') 
    # if ans == 'y': 
    #     message = input("Write message: ")
    #     # message sent to server 
    #     s.send(message.encode('utf-8')) 
    #     continue
    # else: 
    #     break
# close the connection 
s.close() 
  