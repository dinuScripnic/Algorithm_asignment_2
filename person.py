import copy
from messaging import Key, Message, Priority


class Person:
    def __init__(self, person_id: str, encoding_key: Key) -> None:
        """
        Default initializer. Add explicit setters/getters if you need to initialize attributes.
        :param person_id: the unique id of this person
        :param encoding_key: the "trained" key used for encoding and decoding the messages
        """
        self._id = person_id
        self._key = encoding_key
        self.network = None

    def get_person_id(self) -> str:
        return self._id  # return the id of the person

    def get_serialized_key(self)  -> str:
        """
        The encoding/decoding key can be stored inside the Registry ONLY if serialized to a stream of bytes, values, etc...
        :return:
        """
        return Key.serialize(self._key)  # serialize the key to a string with the following format: char:occurrence,char:occurrence,etc...
    
    def join_network(self, network) -> None:
        """
        Join the network
        :param network: the network to join
        :return: None
        """
        self.network = network  # set the network
    
    def leave_network(self) -> None:
        """
        Leave the network
        :return: None
        """
        if not self.network:  # if not connected to the network, do nothing
            return  # leave the network
        self.network = None  # leave the network

    def send_message_to(self, to_person_id: str, plain_content: str) -> None:
        """
        Send a message with LOW priority to another person.
        :param to_person_id: the id of the receiver person
        :param plain_content: the content of the message that must be encoded before
        :return:
        """
        if not self.network:  # if not connected to the network, do nothing
            return
        plain_content = self._key.encode(plain_content)
        message = Message(self._id, plain_content, Priority.LOW, to_person_id)
        self.network.send(message)  # send the message to the message.receiver

    def send_urgent_message_to(self, to_person_id: str, plain_content: str) -> None:
        """
        Send a message with MEDIUM priority to another person.
        :param to_person_id: the id of the receiver person
        :param plain_content: the content of the message that must be encoded before
        :return:
        """
        if not self.network:
            return
        plain_content = self._key.encode(plain_content)
        message = Message(self._id, plain_content, Priority.MEDIUM, to_person_id)
        self.network.send(message)  # send the message to the receiver


    def send_very_urgent_message_to(self, to_person_id: str, plain_content: str) -> None:
        """
        Send a message with HIGH priority to another person.
        :param to_person_id: the id of the receiver person
        :param plain_content: the content of the message that must be encoded before
        :return:
        """
        if not self.network:  # if not connected to the network, do nothing
            return
        plain_content = self._key.encode(plain_content)
        message = Message(self._id, plain_content, Priority.HIGH, to_person_id)  # create the message
        self.network.send(message)  # send the message


    def send_message_to_everyone(self, plain_content: str) -> None:
        """
        Send a LOW priority broadcast message
        :param plain_content: the content of the message that must be encoded before
        :return:
        """
        if not self.network:  # if not connected to the network, do nothing
            return
        plain_content = self._key.encode(plain_content)
        message = Message(self._id, plain_content, Priority.LOW)  # create the broadcast message
        message.already_seen = [self.get_person_id()]  # so the sender will not receive the message
        self.network.broadcast(message)  # send the message to everyone


    def send_urgent_message_to_everyone(self, plain_content: str) -> None:
        """
        Send a MEDIUM priority broadcast message
        :param plain_content: the content of the message that must be encoded before
        :return:
        """
        if not self.network:  # if not connected to the network, do nothing
            return
        plain_content = self._key.encode(plain_content)  # encode the message
        message = Message(self._id, plain_content, Priority.MEDIUM)  # create the broadcast message
        message.already_seen = [self.get_person_id()]  # so the sender will not receive the message
        self.network.broadcast(message)  # send the broadcast message to all the people in the network

    def send_very_urgent_message_to_everyone(self, plain_content: str) -> None:
        """
        Send a HIGH priority broadcast message
        :param plain_content: the content of the message that must be encoded before
        :return:
        """
        if not self.network:
            return
        plain_content = self._key.encode(plain_content)  # encode the message
        message = Message(self._id, plain_content, Priority.HIGH)  # create the broadcast message
        message.already_seen = [self.get_person_id()]  # so the sender will not receive the message
        self.network.broadcast(message)  # send the broadcast message

    def get_all_messages(self) -> list[Message]:
        """
        Retrieve all the messages waiting to be read. If there are no messages, return an empty list
        :return: the ORDERED list of message or an empty list. The order is defined by priority and the time at which
            messages were received
        """
        if not self.network:  # if not connected to the network, return an empty list
            return []
        messages = self.network.get_all_messages(self)  # get all the messages for this person
        messages = copy.deepcopy(messages)  # copy the list of messages
        for message in messages:
            sender = message.sender
            sender_key = self.network._registry.get_serialized_key(sender)  # get the key of the sender
            sender_key = Key.deserialize(sender_key)  # deserialize the key
            message.content = sender_key.decode(sender_key,message.content)  # decode the message
        return messages  # return the messages