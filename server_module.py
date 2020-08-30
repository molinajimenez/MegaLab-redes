import Node
import json

def init_node(name, neighbors, ip, socket):
    # new_node = Node.Node(name, neighbors, ip, socket)
    # print("new_node", new_node)
    return Node.Node(name, neighbors, ip, socket)


def send_route_table(receiver, state, active_nodes):
    # msg = bytes("||".join([receiver, ]))
    for key in active_nodes.keys():
        if key == receiver:
            receiver_connection = active_nodes[key]
            receiver_connection.send(bytes(json.dumps(state), encoding="ascii"))

def send_message(sender, receiver, message, active_nodes, route_table):
    print("IN server SEND MESSAGE")
    print("sender", sender, "receiver", receiver)
    if receiver in route_table[sender].keys():
        for key in active_nodes.keys():
            if key == receiver:
                receiver_connection = active_nodes[key]
                print("rec conn", receiver_connection)
                receiver_connection.send(bytes("||".join(["3", sender, message, ""]), encoding="ascii"))
                return True
    else:
        return False
    