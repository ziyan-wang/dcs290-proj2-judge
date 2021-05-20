import json
import os
from typing import List

from internal.model import Rule, ExistRule, RuleNode, ChildRule, Direction, ParentChildRule

_EXIST_KEY = '$exist'
_CHILD_KEY = '$child'
_LEFT_KEY = '$left'
_RIGHT_KEY = '$right'
_PARENT_LEFT_KEY = '$parentLeft'
_PARENT_RIGHT_KEY = '$parentRight'


class RuleNotFoundError(RuntimeError):
    pass


def parse_rules(filename: str) -> List[Rule]:
    if not os.path.isfile(filename):
        raise RuleNotFoundError

    with open(filename) as f:
        raw_rules = json.load(f)
    rules: list[Rule] = []
    for rule_id, rule_detail in raw_rules.items():
        if _EXIST_KEY in rule_detail:
            rule = ExistRule(id=rule_id, root=_make_rule_node(rule_detail[_EXIST_KEY]))
            rules.append(rule)
        elif (_CHILD_KEY in rule_detail or
              _LEFT_KEY in rule_detail or _RIGHT_KEY in rule_detail or
              _PARENT_LEFT_KEY in rule_detail or _PARENT_RIGHT_KEY in rule_detail):
            if _LEFT_KEY in rule_detail or _PARENT_LEFT_KEY in rule_detail:
                key = _LEFT_KEY if _LEFT_KEY in rule_detail else _PARENT_LEFT_KEY
                direction = Direction.LEFT
            elif _RIGHT_KEY in rule_detail or _PARENT_RIGHT_KEY in rule_detail:
                key = _RIGHT_KEY if _RIGHT_KEY in rule_detail else _PARENT_RIGHT_KEY
                direction = Direction.RIGHT
            else:
                key = _CHILD_KEY
                direction = Direction.NONE
            rule_root = rule_detail[key][0]
            rule_child = rule_detail[key][1]
            if _PARENT_LEFT_KEY in rule_detail or _PARENT_RIGHT_KEY in rule_detail:
                make_rule = ParentChildRule
            else:
                make_rule = ChildRule
            rule = make_rule(id=rule_id, root=_make_rule_node(rule_root),
                             child=_make_rule_node(rule_child), direction=direction)
            rules.append(rule)
        else:
            raise RuntimeError(f'Invalid rule {rule_id}')
    return rules


def _make_rule_node(rule_node_info) -> RuleNode:
    return RuleNode(name=rule_node_info['name'],
                    index=rule_node_info['index'] if 'index' in rule_node_info else None,
                    literal=rule_node_info['literal'] if 'literal' in rule_node_info else None)
