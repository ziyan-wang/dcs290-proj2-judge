from __future__ import annotations
from typing import Optional
from enum import Enum


class Node:
    def __init__(self, *, type_name: str, index: Optional[int], literal: Optional[str], parent: Node):
        self.type_name: str = type_name
        self.index: Optional[int] = index
        self.literal: Optional[str] = literal
        self.parent: Optional[Node] = parent
        self.left_child: Optional[Node] = None
        self.right_child: Optional[Node] = None


class RuleNode:
    def __init__(self, *, name: str, index: Optional[int], literal: Optional[str]):
        self.name: str = name
        self.index: Optional[int] = index
        self.literal: Optional[str] = literal


class Direction(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2


class Rule:
    def __init__(self, *, id: str):
        self.id = id


class ExistRule(Rule):
    def __init__(self, *, id: str, root: RuleNode):
        super().__init__(id=id)
        self.root = root


class ChildRule(Rule):
    def __init__(self, *, id: str, root: RuleNode, child: RuleNode, direction: Direction):
        super().__init__(id=id)
        self.root = root
        self.child = child
        self.direction = direction


class ParentChildRule(ChildRule):
    pass
