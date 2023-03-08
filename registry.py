class RegistryException(Exception):
    """
    A generic exception for problems in the registry
    """

    pass


class node:
	def __init__(self,value: str, node_id: int, serialized_key: str) -> None:
		self.value=value
		self.node_id = node_id
		self.serialized_key = serialized_key
		self.left_child=None
		self.right_child=None
		self.parent=None
		self.height=1 


class AVLTree:
	def __init__(self) -> None:
		self.root=None

	def insert(self, person: str, node_id: int, serialized_key: str) -> None:
		if self.root==None:
			self.root=node(person, node_id, serialized_key)
		else:
			self._insert(person, node_id, serialized_key,self.root)

	def _insert(self, value:str, node_id:int, serialized_key:str,cur_node:node) -> None:
		if value<cur_node.value:
			if cur_node.left_child==None:
				cur_node.left_child=node(value, node_id, serialized_key)
				cur_node.left_child.parent=cur_node # set parent
				self._inspect_insertion(cur_node.left_child)
			else:
				self._insert(value, node_id, serialized_key,cur_node.left_child)
		elif value>cur_node.value:
			if cur_node.right_child==None:
				cur_node.right_child=node(value, node_id, serialized_key)
				cur_node.right_child.parent=cur_node # set parent
				self._inspect_insertion(cur_node.right_child)
			else:
				self._insert(value, node_id, serialized_key,cur_node.right_child)
		else:
			if cur_node.value == value and cur_node.node_id==node_id and (cur_node.serialized_key==serialized_key or cur_node.serialized_key!=serialized_key):
				raise RegistryException("Duplicate entry")
			if cur_node.value == value and  not cur_node.node_id:
				cur_node.node_id = node_id
				cur_node.serialized_key = serialized_key
				return

	def height(self):
		if self.root!=None:
			return self._height(self.root,0)
		else:
			return 0

	def _height(self,cur_node,cur_height):
		if cur_node==None: return cur_height
		left_height=self._height(cur_node.left_child,cur_height+1)
		right_height=self._height(cur_node.right_child,cur_height+1)
		return max(left_height,right_height)

	def find(self,value):
		if self.root!=None:
			return self._find(value,self.root)
		else:
			return None

	def _find(self,value,cur_node):
		if value==cur_node.value:
			return cur_node
		elif value<cur_node.value and cur_node.left_child!=None:
			return self._find(value,cur_node.left_child)
		elif value>cur_node.value and cur_node.right_child!=None:
			return self._find(value,cur_node.right_child)

	def delete_value(self,value):
		return self.delete_node(self.find(value))
    
	def delete_node(self,node):

		if node==None or self.find(node.value)==None:
			return None

		def min_value_node(n):
			current=n
			while current.left_child!=None:
				current=current.left_child
			return current

		# returns the number of children for the specified node
		def num_children(n):
			num_children=0
			if n.left_child!=None: num_children+=1
			if n.right_child!=None: num_children+=1
			return num_children

		# get the parent of the node to be deleted
		node_parent=node.parent

		# get the number of children of the node to be deleted
		node_children=num_children(node)

		# break operation into different cases based on the
		# structure of the tree & node to be deleted

		# CASE 1 (node has no children)
		if node_children==0:

			if node_parent!=None:
				# remove reference to the node from the parent
				if node_parent.left_child==node:
					node_parent.left_child=None
				else:
					node_parent.right_child=None
			else:
				self.root=None

		# CASE 2 (node has a single child)
		if node_children==1:

			# get the single child node
			if node.left_child!=None:
				child=node.left_child
			else:
				child=node.right_child

			if node_parent!=None:
				# replace the node to be deleted with its child
				if node_parent.left_child==node:
					node_parent.left_child=child
				else:
					node_parent.right_child=child
			else:
				self.root=child

			# correct the parent pointer in node
			child.parent=node_parent

		# CASE 3 (node has two children)
		if node_children==2:

			# get the inorder successor of the deleted node
			successor=min_value_node(node.right_child)

			# copy the inorder successor's value to the node formerly
			# holding the value we wished to delete
			node.value=successor.value

			# delete the inorder successor now that it's value was
			# copied into the other node
			self.delete_node(successor)

			# exit function so we don't call the _inspect_deletion twice
			return

		if node_parent!=None:
			# fix the height of the parent of current node
			node_parent.height=1+max(self.get_height(node_parent.left_child),self.get_height(node_parent.right_child))

			# begin to traverse back up the tree checking if there are
			# any sections which now invalidate the AVL balance rules
			self._inspect_deletion(node_parent)


	def _inspect_insertion(self,cur_node,path=[]):
		if cur_node.parent==None: return
		path=[cur_node]+path

		left_height =self.get_height(cur_node.parent.left_child)
		right_height=self.get_height(cur_node.parent.right_child)

		if abs(left_height-right_height)>1:
			path=[cur_node.parent]+path
			self._rebalance_node(path[0],path[1],path[2])
			return

		new_height=1+cur_node.height
		if new_height>cur_node.parent.height:
			cur_node.parent.height=new_height

		self._inspect_insertion(cur_node.parent,path)

	def _inspect_deletion(self,cur_node):
		if cur_node==None: return

		left_height =self.get_height(cur_node.left_child)
		right_height=self.get_height(cur_node.right_child)

		if abs(left_height-right_height)>1:
			y=self.taller_child(cur_node)
			x=self.taller_child(y)
			self._rebalance_node(cur_node,y,x)

		self._inspect_deletion(cur_node.parent)

	def _rebalance_node(self,z,y,x):
		if y==z.left_child and x==y.left_child:
			self._right_rotate(z)
		elif y==z.left_child and x==y.right_child:
			self._left_rotate(y)
			self._right_rotate(z)
		elif y==z.right_child and x==y.right_child:
			self._left_rotate(z)
		elif y==z.right_child and x==y.left_child:
			self._right_rotate(y)
			self._left_rotate(z)
		else:
			raise RegistryException("Tree is in an invalid state.")

	def _right_rotate(self,z):
		sub_root=z.parent
		y=z.left_child
		t3=y.right_child
		y.right_child=z
		z.parent=y
		z.left_child=t3
		if t3!=None: t3.parent=z
		y.parent=sub_root
		if y.parent==None:
				self.root=y
		else:
			if y.parent.left_child==z:
				y.parent.left_child=y
			else:
				y.parent.right_child=y
		z.height=1+max(self.get_height(z.left_child),
			self.get_height(z.right_child))
		y.height=1+max(self.get_height(y.left_child),
			self.get_height(y.right_child))

	def _left_rotate(self,z):
		sub_root=z.parent
		y=z.right_child
		t2=y.left_child
		y.left_child=z
		z.parent=y
		z.right_child=t2
		if t2!=None: t2.parent=z
		y.parent=sub_root
		if y.parent==None:
			self.root=y
		else:
			if y.parent.left_child==z:
				y.parent.left_child=y
			else:
				y.parent.right_child=y
		z.height=1+max(self.get_height(z.left_child),
			self.get_height(z.right_child))
		y.height=1+max(self.get_height(y.left_child),
			self.get_height(y.right_child))

	def get_height(self,cur_node):
		if cur_node==None: return 0
		return cur_node.height

	def taller_child(self,cur_node):
		left=self.get_height(cur_node.left_child)
		right=self.get_height(cur_node.right_child)
		return cur_node.left_child if left>=right else cur_node.right_child

	def inorder(self) -> list:
		"""Returns a list of the tree's elements in inorder."""
		output = []
		if self.root:
			self._inorder(self.root, output)
		return output
	def _inorder(self, cur_node, output):
		if cur_node:
			self._inorder(cur_node.left_child, output)
			output.append(cur_node)
			self._inorder(cur_node.right_child, output)
        
        
        
class Registry:
    """
    This class implements a simple (in-memory) database that stores information about the Persons that have
    joined the network
    """

    def __init__(self) -> None:
        """
        Default constructor. Use explicit setters/getters to add more attributes
        """
        self.connected = AVLTree()

    def get_serialized_key(self, person_id: str) -> str:
        """
        Retrieve encoding/decoding key
        :param person_id:
        :return: the serialized key associated to the give person_id if exists otherwise return None
        """
        if self.connected:
            person = self.connected.find(person_id)
            if person:
                return person.serialized_key
        return None         
    
    def node_in_use(self, node_id: int) -> bool:  # tested
        """
        Check whether the given node is in use
        :param node_id: the id of the node
        :return: True if the node is in use, False otherwise
        """
        if self.connected.root:
            connected = self.connected.inorder()
            for p in connected:
                if p.node_id == node_id:
                    return True
        return False
            

    def get_node_id(self, person_id: str) -> int:  # tested
        """
        Returns the node_id associated to the give person_id if exists otherwise return None
        :param person_id:  the id of the person
        :return: node_id or None
        """
        person = self.connected.find(person_id)
        if person:
            return person.node_id
        else:
            return None
    
    def get_persons(self) -> list[str]:  # tested
        """
        Retrieve the list of all the persons that have joined the network
        :return: the list of person ids
        """
        output = []
        if self.connected.root:
            connected = self.connected.inorder()
            for p in connected:
                output.append(p.value)
        return output
            
    
    def get_persons_at_node(self, node_id: int) -> list[str]:  # tested
        if self.connected:
            output = []
            persons = self.connected.inorder()
            for p in persons:
                if p.node_id == node_id:
                    output.append(p.value)
            return output
        return []
            
    def is_connected(self, person_id: str) -> bool:  # tested
        """
        Check whether the person with the given id is connected to the network
        :param person_id:
        :return: True if the person is connected, False otherwise
        """
        if self.connected.root:
            if self.connected.find(person_id):
                return True
            else:
                return False
        else:
            return False
        
    def delete(self, person_id: str) -> None:  # tested
        """
        Delete all the information associated to the person if the person exists. Do nothing otherwise
        :param person_id:
        :return:
        """
        self.connected.delete_value(person_id)
    
    def remove_node(self, node_id: int) -> None:  # tested
        """
        Remove all the information associated to the given node
        :param node_id:
        :return:
        """
        if self.connected:
            persons = self.connected.inorder()
            for p in persons:
                if p.node_id == node_id:
                    p.node_id = None

            

    def insert(self, person_id: str, node_id: int, serialized_key: str) -> None:  # tested
        """
        Insert the information of a person joining the network
        - Fails with a RegistryException if a person with same id is already registered

        Note: The registry cannot store structured data, i.e., objects, so we need to provide only plain strings
        so they can be copied by value

        :param person_id: the id of the person
        :param node_id: the id of the node
        :param serialized_key: the serialized encoding/decoding key (this is a string!)
        :return:
        """
        self.connected.insert(person_id, node_id, serialized_key)