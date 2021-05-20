from internal.model import Node, Rule, ExistRule, ChildRule, Direction, RuleNode, ParentChildRule


def check(tree: Node, rules: list[Rule]) -> list[str]:
    violated: list[str] = []
    for rule in rules:
        if _check(tree, rule) is False:
            violated.append(rule.id)
    return violated


def _check(root: Node, rule: Rule) -> bool:
    if isinstance(rule, ExistRule):
        return _check_exist(root, rule)
    elif isinstance(rule, ParentChildRule):
        return _check_parent_child(root, rule)
    elif isinstance(rule, ChildRule):
        return _check_child(root, rule, False)
    else:
        raise RuntimeError('Unexpected rule type')


def _check_exist(root: Node, rule: ExistRule) -> bool:
    if _check_single(root, rule.root):
        return True
    if root.left_child is not None and _check_exist(root.left_child, rule):
        return True
    if root.right_child is not None and _check_exist(root.right_child, rule):
        return True
    return False


def _check_child(root: Node, rule: ChildRule, root_found: bool) -> bool:
    if root_found is False:
        if _check_single(root, rule.root):
            if ((rule.direction == Direction.NONE or rule.direction == Direction.LEFT) and
                    root.left_child is not None and _check_child(root.left_child, rule, True)):
                return True
            if ((rule.direction == Direction.NONE or rule.direction == Direction.RIGHT) and
                    root.right_child is not None and _check_child(root.right_child, rule, True)):
                return True
        if root.left_child is not None and _check_child(root.left_child, rule, False):
            return True
        if root.right_child is not None and _check_child(root.right_child, rule, False):
            return True
        return False
    else:
        if _check_single(root, rule.child):
            return True
        if root.left_child is not None and _check_child(root.left_child, rule, True):
            return True
        if root.right_child is not None and _check_child(root.right_child, rule, True):
            return True
        return False


def _check_parent_child(root: Node, rule: ParentChildRule) -> bool:
    if _check_single(root, rule.root):
        parent = root.parent
        if parent is not None:
            if root == parent.left_child:
                return _check_child(parent.right_child, rule, True) if parent.right_child is not None else False
            elif root == parent.right_child:
                return _check_child(parent.left_child, rule, True) if parent.left_child is not None else False
            else:
                raise RuntimeError('Unexpected found_root_node')
    if root.left_child is not None and _check_parent_child(root.left_child, rule):
        return True
    if root.right_child is not None and _check_parent_child(root.right_child, rule):
        return True
    return False


def _check_single(root: Node, rule_node: RuleNode) -> bool:
    return (rule_node.name == root.type_name and
            (rule_node.index is None or rule_node.index == root.index) and
            (rule_node.literal is None or rule_node.literal == root.literal))
