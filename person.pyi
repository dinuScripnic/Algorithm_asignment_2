from __future__ import annotations

from typing import MutableSequence, Generic
from protocols import ID
from messaging import Key, Message
from network import CommunicationNetwork

class Person(Generic[ID]):
    _id: ID
    _key: Key
    network: CommunicationNetwork
    def __init__(self, person_id: ID, encoding_key: Key): ...
    def get_person_id(self) -> ID: ...
    def get_serialized_key(self) -> str: ...
    def join_network(self, network: CommunicationNetwork) -> None: ...
    def leave_netowrk(self) -> None: ...
    def send_message_to(self, to_person_id: ID, plain_content: str) -> None: ...
    def send_urgent_message_to(self, to_person_id: ID, plain_content: str) -> None: ...
    def send_very_urgent_message_to(
        self, to_person_id: ID, plain_content: str
    ) -> None: ...
    def send_message_to_everyone(self, plain_content: str) -> None: ...
    def send_urgent_message_to_everyone(self, plain_content: str) -> None: ...
    def send_very_urgent_message_to_everyone(self, plain_content: str) -> None: ...
    def get_all_messages(self) -> MutableSequence[Message]: ...
