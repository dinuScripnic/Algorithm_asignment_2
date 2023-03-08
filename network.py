import sys
import string

from messaging import Key, Message
from person import Person
# from messaging import Message
from registry import Registry


class InvalidNetworkException(Exception):
    """
    A generic exception for problems in the network
    """

    pass

class Priorityqueue:
    
    def __init__(self) -> None:
        self.low = []
        self.medium = []
        self.high = []        
      
    def add(self, message: Message) -> None:
        message_priority = message.priority
        if message_priority == 0:
            self.low.append(message)
        elif message_priority == 1:
            self.medium.append(message)
        elif message_priority == 2:
            self.high.append(message)
    
    def remove_for_person(self, person: str) -> None:
        self.messages = self.high+self.medium+self.low
        for message in self.messages:
            if message.receiver == person:
                self.remove_message(message)
    
    def remove_message(self, message: Message) -> None:
        if message.priority == 0:
            self.low.remove(message)
        elif message.priority == 1:
            self.medium.remove(message)
        elif message.priority == 2:
            self.high.remove(message)
    
    def return_all_messages_of_a_person(self, person: str) -> list[Message]:
        output = []
        self.messages = self.high+self.medium+self.low
        for message in self.messages:
            if message.receiver == person:
                output.append(message)
                self.remove_message(message)
            elif message.receiver == None:
                if person in message.already_seen:
                    pass
                else:
                    message.already_seen.append(person)
                    output.append(message)
        return output
    
    def __len__(self) -> int:
        return len(self.high)+len(self.medium)+len(self.low)


class Node:
    def __init__(self, node_id: int) -> None:
        """
        Default constructor. If you need to set attributed, use explicit setters/getters. Do not add parameters here
        :param node_id:
        """
        self.node_id = node_id
        self.next = None
        self.queue = None

    def receive(self, message: Message) -> None:
        """
        Receive a message
        :param message: an object with sender, priority, content, and recipient fields
        :return:
        """
        if not self.queue:
            self.queue = Priorityqueue()
        self.queue.add(message)
            

    def get_all_messages(self, person: str) -> list[Message]:
        """
        Retrieve all the messages waiting to be read. If there are no messages, return an empty list
        :param person: who received the messages (both direct and broadcast)
        :return: the list of messages ordered by arrival time and priority
        """
        if self.queue:
            return self.queue.return_all_messages_of_a_person(person)
        else:
            return []
    
    def delete_messages(self, person: str) -> None:
        """
        delete all the messages for the given person
        :param person: the person that received the messages
        :return:
        """
        if self.queue:
            self.queue.remove_for_person(person)
        else:
            pass 
    
    def delete_for_forwarding(self, message: Message) -> None:
        try:
            self.queue.remove_message(message)
        except:
            pass
    
    def delete_all_messages(self) -> None:
        self.queue = None
    

class LinkedList:
    
    def __init__(self) -> None:
        self.head = None
    
    def insert(self, node: Node) -> None:
        if self.head is None:
            self.head = node
        else:
            node.next = self.head
            self.head = node
    
    def search(self, node_id: int) -> Node:
        current = self.head
        while current:
            if current.node_id == node_id:
                return current
            current = current.next
        return None

    def delete(self, node_id: int) -> None:
        if self.head is None:
            raise InvalidNetworkException("Cannot delete from empty list")
        if self.head.node_id == node_id:
            self.head = self.head.next
            return
        else:
            current = self.head
            while current.next:
                if current.next.node_id == node_id:
                    if current.next.next is None:
                        current.next = None
                        return
                    else:
                        current.next = current.next.next
                        return
                current = current.next
        
    
    def exists(self, node_id: int) -> bool:
        current = self.head
        while current:
            if current.node_id == node_id:
                return True
            current = current.next
        return False

    def get(self, index: int) -> Node:
        if index == 0:
            return self.head
        if index > len(self):
            return None
        if index < 0:
            index = len(self) + index
        current = self.head
        for i in range(index):
            current = current.next
        return current
    
    def __iter__(self) -> Node:
        current = self.head
        while current:
            yield current
            current = current.next
    
    def __len__(self) -> int:
        count = 0
        self.current = self.head
        while self.current:
            count += 1
            self.current = self.current.next
        return count


class Edge:

    def __init__(self, to_node:int, cost: int) -> None:
        self.to_node = to_node
        self.cost = cost


class CommunicationNetwork:
    def __init__(self) -> None:  # tested
        """
        Default initializer. The network contains nodes, links and the registry
        """
        self._registry = Registry()  # {person_id: {node: node_id, key: serialized_key}...}
        self._nodes = LinkedList()  # (Node_1, Node_1.next->Node_2, Node_2.next->Node_3, ...)
        self._edges = {}  # {node_1: {to_node_2: Edge(to_node_2, cost), to_node_3: Edge(to_note_3, cost), ...}, ...}

    def add(self, node: Node) -> None:  # tested
        """
        Add a new node to the network. Fail with an InvalidNetworkException if a node with the same node_id exists.
        :param node:
        :return:
        """
        if not isinstance(node, Node):
            raise InvalidNetworkException("Node is not an instance of Node")
        if node in self._nodes:
            raise InvalidNetworkException("A node with the same node_id exists.")
        self._nodes.insert(node)
    
    def add_multiple(self, nodes: list[Node]) -> None:  # tested
        # created it for testing purposes, because i was tired of adding nodes one by one
        """
        Add all the nodes in the list to the network
        :param nodes:
        :return:
        """
        for node in nodes:
            self.add(node)

    def remove(self, node: Node)->None:  # tested
        """
        Remove the node with the given node_id from the network. Do nothing if the node does not exist.
        Disconnect all the persons that are attached to this node and discard any "unread" message.
        Fail with an InvalidNetworkException if the network becomes invalid after removing the node.
        :param node:
        :return:
        """
        if node not in self._nodes:  # tested
            return
        else:  # tested
            node.delete_all_messages()
            if node.node_id in self._edges:
                neighbours = [neighbour for neighbour in self._edges[node.node_id].keys()]
                for neighbour in neighbours:
                    self.unlink(node, self._nodes.search(neighbour))
                self._edges.pop(node.node_id)
            self._nodes.delete(node.node_id)
            self._registry.remove_node(node.node_id)
            if not self.is_valid():  # tested
                raise InvalidNetworkException("The network is invalid after removing the node.")

    def link(self, node_1: Node, node_2: Node, cost: int) -> None:  # tested
        """
        Connect the two nodes using an undirected/bi-directional link with a given cost.
        - Fail with an InvalidNetworkException if the nodes are the same (no self-loop)
        - Fail with an InvalidNetworkException if any of the nodes does not exist
        - Fail with an InvalidNetworkException if the nodes are already linked
        - Fail with an InvalidNetworkException if the cost is not positive
        :param node_1: the first node
        :param node_2: the second node
        :param cost: non-zero, positive value, distance between the two nodes
        :return:
        """
        if node_1 == node_2:  #tested
            raise InvalidNetworkException("No self-loop")
        elif not self._nodes.exists(node_1.node_id) or not self._nodes.exists(node_2.node_id):  #tested
            raise InvalidNetworkException("One of the nodes does not exist")
        elif cost <= 0:  #tested
            raise InvalidNetworkException("Cost must be positive")
        else:  #tested
            edge_to_node_1 = Edge(node_1, cost)
            edge_to_node_2 = Edge(node_2, cost)
            # get the neighbors of node_1
            if node_1.node_id in self._edges:
               node_1_edges = self._edges[node_1.node_id]
            else:  # if no neighbors, create new
                self._edges[node_1.node_id] = {}
                node_1_edges = self._edges[node_1.node_id]
            # get the neighbors of node_2
            if node_2.node_id in self._edges:
                node_2_edges = self._edges[node_2.node_id]
            else: # if no neighbors, create new
                self._edges[node_2.node_id] = {}
                node_2_edges = self._edges[node_2.node_id]
            if node_2.node_id not in node_1_edges or node_1.node_id not in node_2_edges:  # check if node_1 is already linked to node_2
                node_1_edges[node_2.node_id] = edge_to_node_2
                node_2_edges[node_1.node_id] = edge_to_node_1
            else:
                raise InvalidNetworkException("Nodes are already linked")
                
    def unlink(self, node_1: Node, node_2: Node)->None:  # tested
        """
        Disconnect the two nodes. Do nothing if the nodes do not exist or are not connected
        :param node_1: the first node
        :param node_2:  the second node
        :return:  None
        """
        # first check if any persons are connected to the nodes
        # tested
        if self._registry.node_in_use(node_1.node_id) and self._registry.node_in_use(node_2.node_id):
            raise InvalidNetworkException("One of the nodes is in use")
        else:
            try:  # tested
                self._edges[node_1.node_id].pop(node_2.node_id)  # remove the edge from node_1's neighbors
                self._edges[node_2.node_id].pop(node_1.node_id)  # remove the edge from node_2's neighbors
            except KeyError:  # if nodes are not connected
                pass  # tested
    
    def is_valid(self) -> bool:  # tested
        """
        Validate the network
        :return: True if the network is connected, i.e., each node is reachable from any other node (except itself)
        """
        if len(self._nodes) == 0:  # if no nodes, return True
            return True
        if len(self._nodes) == 1:  # if only one node, the network is theoretically connected
            return True
        if len(self._edges) == 0:  # this one was added in case we remove the node from the network, before the network was connected
            return True
        else:
            visited = set()
            self._dfs(self._nodes.get(0).node_id, visited)
            return len(visited) == len(self._nodes)
    
    def _dfs(self, node: int, visited: set[Node]) -> None: # tested
        """
        Helper function for is_valid
        :param node: the node to start the search
        :param visited: a set of visited nodes
        :return: None
        """
        if node not in visited:
            visited.add(node)
            if node in self._edges:
                for neighbor in self._edges[node]:
                    self._dfs(neighbor, visited)

    def join_network(self, person: Person, node_id: int) -> None:  # tested
        """
        Register the person in the network, including adding all the information to the Registry
        :param person: the person object that must be registered in the network at the given node
        :param node_id: the id of the node which will become the gateway for the person
        :return:
        """
        self._registry.insert(person.get_person_id(), node_id, person.get_serialized_key())  # insert the person into the registry
        person.join_network(self)  # add the person to the network

    def leave_network(self, person: Person) -> None:
        """
        Remove this person and all the unread messages from the network and delete all the infos from the Registry
        :param person:
        :return:
        """
        if not self._registry.is_connected(person.get_person_id()):  # if not connected, do nothing
            return
        person.leave_network()  # remove the person from the network
        person_id = person.get_person_id()  # get the person's id
        node = self._nodes.search(self._registry.get_node_id(person_id))  # get the node that the person is connected to
        self._registry.delete(person_id)  # delete the person from the registry
        node.delete_messages(person_id)  # delete the person's messages from the node              

    
    def minimum_distance(self, distance: dict, node_list: list) -> Node:  # tested
        """
        Returns the node with the minimum distance from the source node
        : param distance: a dictionary of distances from the source node
        : param node_list: a list of nodes
        : return: the node with the minimum distance
        """
        min = None 
        for node in node_list:  # iterate through the nodes
            if min == None:  # if min is not set
                min = node  # set min to the first node
            elif distance[node] < distance[min]:  # if the distance of the current node is less than the distance of the min node
                min = node  # set min to the current node
        return min  # return the node with the minimum distance
    
    def dijkastra(self, start_node: int) -> tuple[dict, dict]:  # tested
        """
        Find the shortest path from start_node to end_node using Dijkstra's algorithm.
        :param start_node:  the node to start the search
        :return: a tuple of two dictionaries. The first dictionary contains the shortest distance from start_node to each node.
        """
        node_list = [node.node_id for node in self._nodes]  # initialize node_list to all nodes
        distance = dict.fromkeys(node_list, sys.maxsize)  # initialize distance to all nodes to infinity
        previous = dict.fromkeys(node_list, sys.maxsize)  # initialize previous to all nodes to None
        distance[start_node] = 0  # distance from start_node to start_node is 0
        
        while node_list:  # while there are still nodes to visit
            u = self.minimum_distance(distance, node_list)  # get the node with the minimum distance from start_node
            node_list.remove(u)  # remove the node from the list of nodes to visit
            if u in self._edges:  # if u has neighbors
                for key, value in self._edges[u].items():  # for each neighbor
                    alt = distance[u] + value.cost  # calculate the distance from start_node to the neighbor
                    if alt < distance[value.to_node.node_id]:  # if the distance is less than the current distance
                        distance[value.to_node.node_id] = alt  # update the distance
                        previous[value.to_node.node_id] = u  # update the previous node
                        
        return distance, previous

    def path(self, end_node: int, prev: dict) -> list[int]:  # tested
        """
        prints the path from start_node to end_node, with step-by-step instructions
        :param end_node: the id of the end node
        :prev: the dictionary of previous nodes
        :return: a list of nodes representing the shortest path from start_node to end_node
        """
        previous_node = prev[end_node]  # get the previous node
        route = [end_node]  # initialize the route to the end node
        while previous_node != sys.maxsize: 
            route.append(previous_node)  # add the previous node to the route
            previous_node = prev[previous_node]  # get the previous node of the previous node
            
        route.reverse()  # reverse the route
        return route  # return the route

    def send(self, message: Message) -> None:
        """
        Send the message from the sender to the recipient specified inside the message (i.e., message.receiver)
        - Fail if message.receiver is not registered
        - Fail if message.sender is not registered in the network
        :param message: an object with sender, priority, content, and recipient fields
        :return:
        """
        receiver = message.receiver
        sender = message.sender
        connected_persons = self._registry.get_persons()  # get the list of connected persons
        if receiver not in connected_persons:  # if the receiver is not registered
            raise InvalidNetworkException("Receiver is not registered in the network")
        elif sender not in connected_persons: # this one is a bit irelevant, connection to network is checked in the person class when sending a message
            raise InvalidNetworkException("Sender is not registered in the network")
        else:  # tested
            receiver_node = self._registry.get_node_id(receiver)
            sender_node = self._registry.get_node_id(sender)
            if receiver_node == sender_node:  # if the sender and receiver are connected to the same node
                self.forward(message, self._nodes.search(receiver_node))  # forward the message to the node
                return
            if not sender_node:
                raise InvalidNetworkException("Sender does not have a node")
            previous = self.dijkastra(sender_node)[1]
            path = self.path(receiver_node, previous)
            # if len(path) == 1:
            #     self.forward(message, self._nodes.search(path[0]))
            #     return
            for step in path:
                previous_node = self._nodes.search(path[path.index(step) - 1])
                for node in self._nodes:
                    if node.node_id == step:
                        if node.node_id == sender_node:
                            continue
                        else:
                            self.forward(message, node)
                            if previous_node:
                                previous_node.delete_for_forwarding(message)
                            break

    def broadcast(self, message: Message) -> None:
        """
        Send the message from the sender to all connected recipients (but not the sender). Note: message.receiver must be None.
        - Fail if message.receiver is not None
        - Fail if message.sender is not registered in the network
        :param message: an object with sender, priority, content, and without reciver because its brodcast.
        :return:
        """
        if message.receiver is not None:
            raise InvalidNetworkException("Message is not a broadcast message")
        elif message.sender not in self._registry.get_persons(): # this one is a bit irelevant, connection to network is checked in the person class when sending a message
            raise InvalidNetworkException("Sender is not registered in the network")
        else:  # tested
            for node in self._nodes:  # send the message to all nodes
                receiver_node = node.node_id  # get the receiver node id
                sender_node = self._registry.get_node_id(message.sender)  # get the sender node id
                if receiver_node == sender_node:  # if the sender and receiver are the same node
                    self.forward(message, self._nodes.search(receiver_node))
                if not sender_node:
                    raise InvalidNetworkException("Sender does not have a node")
                previous = self.dijkastra(sender_node)[1]  
                path = self.path(receiver_node, previous)  # get the path from sender to receiver
                # if len(path) == 1:  # if the recipient is on the same node as the sender, a easier way to send the message
                #     self.forward(message, self._nodes.search(path[0]))
                for step in path:  
                    previous_node = self._nodes.search(path[path.index(step) - 1])  # get the previous node
                    for node in self._nodes:
                        if node.node_id == step:
                            self.forward(message, node)  # forward the message to the next node
                            if previous_node != None:
                                previous_node.delete_for_forwarding(message)  # delete the message from the previous node
                            break

    def forward(self, message: Message, node: Node) -> None:  # tested
        """
        Simulate the forward of the message to an (intermediate) node.
        :param message: the message to be forwarded
        :param node: node which the message is forwarded to
        :return:
        """
        node.receive(message)
        
    def get_all_messages(self, person: Person) -> list[Message]:  # tested
        """
        Retrieve all the messages waiting to be read. If there are no messages, return an empty list
        :param person: who received the messages (both direct and broadcast)
        :return: the list of messages ordered by arrival time and priority
        """
        person_id = person.get_person_id()  # get the person's id
        if person_id not in self._registry.get_persons():  # if the person is not registered
            return []
        node = self._nodes.search(self._registry.get_node_id(person_id))  # get the node that the person is connected to
        return node.get_all_messages(person_id)  # get the person's messages from the node