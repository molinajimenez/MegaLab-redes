#import Node
# Grafo dirigido, si A->B no significa que exista B->A a menos que este explicitamente descrito, numero es peso.
graph = {'a': {'b': 10, 'c': 3}, 'b': {'c': 1, 'd': 2}, 'c': {
    'b': 4, 'd': 8, 'e': 2}, 'd': {'e': 7}, 'e': {'d': 9}}
#grafo hecho en objetos nodo.

def init_graph(limit):
    mydic = {}
    Node('a',['b','c'],'no_message')
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

def flood(graph, start, end, limit):
    # iniciamos chequeando los hijos de start
    print("limit is", limit)
    #variable que detecta si llegamos
    current = start
    if current != end:
        #fin de la recursividad. si el limite de replicacion es de n hops, el mensaje hara esos hops a lo largo de la red.
        if limit > 0:
            #chequeamos los items que tiene cada nodo (los vecinos)
            for x in graph[start].items():
                # neighbors del current node, le bajamos 1, por hacer un hop
                flood(graph, x[0], end, limit-1)
                print("currently at: ", x[0])
    else:
        print("reached end. at ", current)
        return None

flood(graph, 'a', 'b',3)
