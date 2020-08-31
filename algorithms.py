from Node import *
import time 
import json


# grafo se importara desde server y se parseara a objetos Node linkeados 

# def init_graph(limit):
#     mydic = {}
#     Node('a',['b','c'],'no_message')
#graph2 = {}    

graph = {'a': {'b': 10, 'c': 3}, 'b': {'c': 1, 'd': 2}, 'c': {
    'b': 4, 'd': 8, 'e': 2}, 'd': {'e': 7}, 'e': {'d': 9}}

self_node = None
UPDATE_INTERVAL = 1
ROUTE_UPDATE_INTERVAL = 30

def init_node(node_obj):
    global self_node 
    self_node = node_obj
    # print(self_node)
    return self_node

def get_node_state():
    global self_node 
    return self_node.getState()

def get_node():
    return self_node

def dijkstra(graph, start, goal):
    shortest_distance = {}
    predecessor = {}
    unseenNodes = graph
    infinity = float("inf")
    path = []
    # todos los nodos inician con peso infinito, esto nos ayuda para que veamos si se puede llegar o no.
    for node in unseenNodes:
        shortest_distance[node] = infinity
    shortest_distance[start] = 0
    # mientras no hayamos recorrido todo..
    while unseenNodes:
        minNode = None
        for node in unseenNodes:
            if minNode is None:
                # asumimos al inicio que es el minimo.
                minNode = node
                # bubble sort del minimo
            elif shortest_distance[node] < shortest_distance[minNode]:
                minNode = node
        # obtenemos el peso de cada item y sumamos eso mas la distancia del minimo, si es menor a el childnoe (infinito) o un valor no optimo
        for childNode, weight in graph[minNode].items():
            if weight + shortest_distance[minNode] < shortest_distance[childNode]:
                # asignamos la suma (deja de ser infinito)
                shortest_distance[childNode] = weight + \
                    shortest_distance[minNode]
                # si es menor, agregamos al camino a recorrer
                predecessor[childNode] = minNode
        # pop para romper el loop
        unseenNodes.pop(minNode)
    # donde estamos
    currentNode = goal
    # mientras no estemos en el final
    while currentNode != start:
        # intentamos, no sabemos si esta realmente conectado
        try:
            # insertamos el actual, con previo 0
            path.insert(0, currentNode)
            # designamos el actual como el predecesor del camino.
            currentNode = predecessor[currentNode]
        except KeyError:
            print('Inalcanzable chavo.')
            break

    path.insert(0, start)
    # si se puede llegar::
    if shortest_distance[goal] != infinity:
        print('Shortest distance is ' + str(shortest_distance[goal]))
        return path

def encodeMessage(nodeentity_id, neighbours):
    messageDict = dict()
    messageDict['nodeId'] = nodeentity_id    
    messageDict['nodeFrom'] = nodeentity_id
    messageDict['nodeNeighbour'] = neighbours
    return json.dumps(messageDict).encode()

def send_self_node(node_key, send_message):
    neighbors = Node.getNeighbors(node_key)
    data = encodeMessage(node_key, neighbors)
    sendLinkStatePacket(neighbors, data, node_key, send_message) 


def sendLinkStatePacket(receivers, message, sender, send_message):
    for target in receivers:
        if sender != target:
            send_message(sender, target, message)
    return


#ni idea de si esto funciona o no
def findRoute(graph, start, end):
    count = 0
    while count < ROUTE_UPDATE_INTERVAL:
        time.sleep(1)
        count += 1
    if count == ROUTE_UPDATE_INTERVAL:
        if len(graph) > 1:
            for node in graph.keys():
                if node == start:
                    continue
                dijkstra(graph, start, end)

        else:
            print("only one node in network")
    return


def flood(graph, start, end, message, send_message, limit=-1):
    #si no se asigna una cantidad de hops se toma todo el largo de la subnet 
    hops = 0
    if limit > -1:
        hops = limit
    else:
        hops = len(graph)
    
    #variable que detecta si llegamos
    current = start
    #fin de la recursividad. si el limite de replicacion es de n hops, el mensaje hara esos hops a lo largo de la red.
    
    #chequeamos los items que tiene cada nodo (los vecinos)
    for x in graph[start].items():
        # neighbors del current node, le bajamos 1, por hacer un hop
        if hops > 0:
            if current != end:
                send_message(start, x[0], message)
                flood(graph, x[0], end, message, send_message, limit=hops-1)
            else:
                print("reached end. at ", current)
                return
    print("out of loop")


# Utilizando Bellman-Ford
def dvrouting(graph, src):
    nodes = list(graph.keys())
    print("nodes", nodes)
    # Conseguir no. de nodos/vertices
    num_nodes = len(graph.keys())
    # Primero se inicializa la DV table con:
    #   Distancia hacia los demas vertices como INF
    dist = {}
    #   Distancia a si mismo 0
    dist[src] = 0

    graphVector = []
    for item in graph.items():
        if item[0] != src:
            dist[item[0]] = float("Inf")
        
        for n in item[1].items():
            temp = []
            temp.append(item[0])
            temp.append(n[0])
            temp.append(n[1])
            graphVector.append(temp)

    # Cambiar u, v (vertices que forman una arista) y w (peso) por como lo vayamos a manejar.
    # u y v: nodos que conforman un edge
    # w es el peso 
    # Contraer todas las aristas V-1 veces. 
    for _ in range(num_nodes - 1):
        for u, v, w in graphVector:  
                if dist[u] != float("Inf") and dist[u] + w < dist[v]:  
                        dist[v] = [dist[u] + w, u]
                        # dist[v].predecesor = u
     
    for u, v, w in graphVector:  
        if dist[u] != float('inf') and dist[u] + w < dist[v]:  
            print("Graph contains negative weight cycle") 
            return 
    return dist


def dvr_find_path(cost, start, end, graph, current_path = [], suma = 0):
    # print("dvr params", cost, start, end, graph)
    for child in graph[start].items():
        suma += child[1]
        if child[0] == end:
            current_path.append(child[0])
            print("current path", current_path, "child", child)
            return current_path
        if suma > cost:
            print("suma", suma, "cost", cost, "child", child)
            suma -= child[1]
            continue
        current_path.append(child[0])
        dvr_find_path(cost, child[0], end, graph, current_path, suma)
    return
        
# def dvr_find_path(cost, start, end, graph):



# dist = dvrouting(graph, 'b')
# print(dist)
# flood(graph, 'a', 'b', 3)
