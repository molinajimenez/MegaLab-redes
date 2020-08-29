
# Import socket module 
import socket 
import argparse


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

while True: 

    message = input("Write message: ")
    # message sent to server 
    s.send(message.encode('ascii')) 

    # messaga received from server 
    data = s.recv(1024) 

    # print the received message 
    # here it would be a reverse of sent message 
    print('Received from the server :',str(data.decode('ascii'))) 

    # ask the client whether he wants to continue 
    ans = input('\nDo you want to continue(y/n) :') 
    if ans == 'y': 
        continue
    else: 
        break
# close the connection 
s.close() 
  