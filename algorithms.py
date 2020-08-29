#import Node
# grafo se importara desde server y se parseara a objetos Node linkeados 

# def init_graph(limit):
#     mydic = {}
#     Node('a',['b','c'],'no_message')
#graph2 = {}    

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
        print('The path is ' + str(path))


#dijkstra(graph, 'a', 'b')

def flood(graph, start, end, limit=-1):

    #si no se asigna una cantidad de hops se toma todo el largo de la subnet 
    hops = 0
    if limit > -1:
        hops = limit
    else:
        hops = len(graph)
        
  
    print("limit is", hops)
    #variable que detecta si llegamos
    current = start
    #fin de la recursividad. si el limite de replicacion es de n hops, el mensaje hara esos hops a lo largo de la red.
    
    innerhops = hops
    #chequeamos los items que tiene cada nodo (los vecinos)
    for x in graph[start].items():
        # neighbors del current node, le bajamos 1, por hacer un hop
        if hops > 0:
            if current != end:
                if hops == innerhops:
                    hops -= 1
                    flood(graph, x[0], end, hops)
                    print("currently at: ", x[0])
                else:
                    flood(graph, x[0], end, hops-1)
                    print("currently at: ", x[0])

            else:
                print("reached end. at ", current)
                break 
    print("out of loop")

# Utilizando Bellman-Ford
def dvrouting(graph, src):
    # Conseguir no. de nodos/vertices
    nodes = len(graph)
    # Primero se inicializa la DV table con:
    #   Distancia hacia los demas vertices como INF
    dist = [float('inf')] * nodes
    #   Distancia a si mismo 0
    dist[src] = 0

    """ TODO (ZEA) """
    # Cambiar u, v (vertices que forman una arista) y w (peso) por como lo vayamos a manejar.

    # Contraer todas las aristas V-1 veces. 
    for _ in range(nodes - 1):
        """ ESTO ES DE MIENTRAS EN LO QUE VEMOS LO DE NODE.PY """
        for u, v, w in graph:  
                if dist[u] != float('inf') and dist[u] + w < dist[v]:  
                        dist[v] = dist[u] + w  

    # Revisar si hay pesos negativos
    """ ESTO ES DE MIENTRAS EN LO QUE VEMOS LO DE NODE.PY """
    for u, v, w in graph:  
        if dist[u] != float('inf') and dist[u] + w < dist[v]:  
            print("Graph contains negative weight cycle") 
            return



# flood(graph, 'a', 'b', 3)
