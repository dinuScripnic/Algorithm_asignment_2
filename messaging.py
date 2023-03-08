from enum import IntEnum
import string
import sys


class Priority(IntEnum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    
class InvalidContentException(Exception):
    pass

class TreeNode:
    def __init__(self, data: tuple) -> None:
        self.data = data
        self.left = None
        self.right = None
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, TreeNode):
            return self.data == __o.data and self.left == __o.left and self.right == __o.right      
        return False
    
def insert(data:list) -> TreeNode:  
    elements_to_insert = data  # list of tuples
    node_list = []  # list of nodes
    data_to_insert = elements_to_insert.pop(0)
    root = TreeNode(data_to_insert)  # creates the root node of the binary tree
    node_list.append(root)  # adds the root node to the list of nodes
    
    while len(elements_to_insert) > 0:  # while there are still elements to insert
        data_to_insert = elements_to_insert.pop(0)
        m = node_list.pop(0)
        m.left = TreeNode(data_to_insert)
        node_list.append(m.left)
        
        data_to_insert = elements_to_insert.pop(0)
        m.right = TreeNode(data_to_insert)
        node_list.append(m.right)
    return root

def find(btree: TreeNode, char: str) -> str:
    """
    Find the morse code for a given character
    :param char:
    :return: morse code
    """
    
    if btree.data[0] == char:
        return ""
    if btree.left:
        left = find(btree.left, char)
        if left is not None:
            return "." + left
    if btree.right:
        right = find(btree.right, char)
        if right is not None:
            return "-" + right
    return None


def transverse(btree: TreeNode) -> str:
    """
    Transverse the binary tree in order
    :param btree:
    :return: string of characters
    """
    queue = [btree]
    result = []
    while queue:
        node = queue.pop(0)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
        result.append(node.data)
    return result

class Key:
    """
    The encoding/decoding key to transform a plain text into a sequence of '.' (dot), '-' (line), ' ' (space),
    '/' (word separator).
    """

    def __init__(self, training_text: str) -> None:
        """
        Default initializer. Given the training text build the internal structure of the key
        :param training_text:
        """
        self.training_text = training_text
        dic = {" ": sys.maxsize}
        # create a dictionary with the occurrences of each letter and digit
        for char in string.ascii_lowercase:  
            dic[char] = training_text.count(char)  
        for char in string.digits: 
            dic[char] = training_text.count(char)
        for key, value in dic.items():  # if there are occurrences, add 122 because the ascii code for z is 122
            if value == 0:
                dic[key] = ord(key)  # if there are no occurrences, add the ascii code of the letter and sort by it
            else:
                dic[key] += 122
        # sort the dictionary by value
        occurrences = sorted(dic.items(), key=lambda c: c[1], reverse=True)# sort by value
        self.root = insert(occurrences)  # create a binary tree with the ordered dictionary            

    @classmethod
    def serialize(cls, the_key: 'Key') -> str:
        """
        Serialize the given key into a string to be stored in the registry
        :param the_key: the actual key object
        :return: a string corresponding to the key
        """
        string_representation = ""
        list = transverse(the_key.root)
        for x in list:
            string_representation += f'{x[0]}:{x[1]},' # add the character and the value to the string
        return string_representation[:-1]  # return the string without the last comma
        

    @classmethod
    def deserialize(cls, the_serialized_key: str):
        """
        Rebuild the key from a the input string read from the registry
        :param the_serialized_key: a string corresponding to the key
        :return: the actual key object
        """
        
        list = the_serialized_key.split(',')
        for i in range(len(list)):
            list[i] = list[i].split(':')
            list[i][1] = int(list[i][1])
            list[i] = tuple(list[i])
        cls.root = insert(list)
        return cls
            

    def encode(self, plain_content: str) -> str:
        """
        Encode the content using the key.
        - Fails with an InvalidContentException if the plain content contains unsupported chars
        :param plain_content:
        :return: encoded_content: made only using the symbols: '.', '-', ' ', '/'
        """
        # check if the plain content contains unsupported chars
        # supported chars are: a-z, 0-9, space
        encoded_content = []  # initialize the list of encoded elements
        for char in plain_content:  # iterate through the plain content
            if char not in string.ascii_lowercase and char not in string.digits and char != ' ':  # if the char is not supported, raise an exception
                raise InvalidContentException("The plain content contains unsupported chars")
            elif char == ' ':  # if the char is a space, add a / to the encoded content
                encoded_content.append('/')
            else:  # if the char is supported, find the morse code for it
                encoded_content.append(find(self.root, char))
            encoded_content.append(' ')  # add a space between each encoded element
        return ''.join(encoded_content)  # return the encoded content

    def decode(self, encoded_content: str) -> str:
        """
        Decode the content using the key.
        - Fails with an InvalidContentException if the encoded content contains unsupported chars
        :param encoded_content:
        :return: decoded_content, i.e., plain content
        """
        decoded_content = []  # initialize the list of decoded elements
        for letter in encoded_content.split():  # split the encoded content by spaces
            if letter != '/':  # if the letter / then it is a space
                current = self.root  # start at the root
                for char in letter:  # iterate through chars of the letter
                    if char not in ['.', '-']:  # if the char is not a dot or a dash, raise an exception
                        raise InvalidContentException("The encoded content contains unsupported chars")
                    elif char == '.':  # if the char is a dot, go left
                        current = current.left  
                    elif char == '-':  # if the char is a dash, go right
                        current = current.right
                decoded_content.append(current.data[0])  # append the decoded letter to the list
                current = self.root  # reset the current node to the root
            else:
                decoded_content.append(' ') 
        return ''.join(decoded_content)  # return the decoded content as a string


class Message:
    """
    A data object containing the relevant information for an message
    """

    def __init__(self, from_person_id, content, priority, to_person_id=None):
        """
        :param from_person_id: id of the person
        :param content: content of the message
        :param priority: one of Priority enumeration
        :param to_person_id: id of the receiver. This can be None only for broadcasted messages
        """
        self.sender = from_person_id
        self.content = content
        self.priority = priority
        self.receiver = to_person_id
        self.already_seen = None

    def __str__(self):
        """
        String representation of the message
        :return:
        """
        return f"Message from {self.sender} to {self.receiver} with priority {self.priority} and content {self.content}"
    
Key('hello world')