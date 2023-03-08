from __future__ import annotations

from typing import Generic
from protocols import ID, MorseStr
from enum import IntEnum

class Priority(IntEnum):
    LOW: int
    MEDIUM: int
    HIGH: int

class InvalidContentException(Exception): ...

class TreeNode:
    def __init__(self, data: tuple) -> None: ...
    def __eq__(self, __o: object) -> bool: ...


class Key:
    def __init__(self, training_text: str): ...
    @classmethod
    def serialize(cls, the_key: Key) -> str: ...
    @classmethod
    def deserialize(cls, the_serialized_key: str) -> Key: ...
    def encode(self, plain_content: str) -> MorseStr: ...
    def decode(self, encoded_content: MorseStr) -> str: ...

class Message(Generic[ID]):
    sender: ID
    content: str
    priority: Priority
    receiver: ID | None
    already_seen: list[ID] | None
    def __init__(
        self,
        from_person_id: ID,
        content: str,
        priority: Priority,
        to_person_id: ID | None = None,
    ): ...
