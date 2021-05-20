import re
from typing import Optional
from internal.model import Node


class IllegalSyntaxTreePrintoutError(RuntimeError):
    pass


def parse_tree(syntax_tree_printout: str) -> (Node, list[str]):
    lines = syntax_tree_printout.splitlines()
    root_row = None
    in_syntax_tree = False
    invalid_lines: list[str] = []
    for row in range(len(lines)):
        line = lines[row]
        if len(line) == 0:
            continue
        if 'SYNTAX TREE PRINTOUT' in line:
            in_syntax_tree = True
            continue
        if not in_syntax_tree:
            if not _check_valid_line(line):
                invalid_lines.append(line)
        else:
            _assert_valid_line(line)
        if 'R-[' in line:
            root_row = row
    if root_row is None:
        raise IllegalSyntaxTreePrintoutError('Cannot find root row')

    tree = _parse_tree(lines, root_row, None)
    return tree, invalid_lines


def _parse_tree(matrix: list[str], row: int, parent: Optional[Node]) -> Node:
    line = matrix[row]
    items = line[line.index('[') + 1: line.index(']')].split(',')
    _assert_valid_line_items(line, items)
    type_name = items[0]
    index = int(items[1]) if len(items) >= 2 else None
    literal = items[2][1:-1] if len(items) >= 3 else None
    node = Node(type_name=type_name, index=index, literal=literal, parent=parent)

    column = line.index('[')
    left_child_row = _find_child_row(matrix, row, column, True)
    right_child_row = _find_child_row(matrix, row, column, False)
    if left_child_row is not None:
        node.left_child = _parse_tree(matrix, left_child_row, node)
    if right_child_row is not None:
        node.right_child = _parse_tree(matrix, right_child_row, node)
    return node


def _check_valid_line(line: str):
    return re.search(r'[+R]-\[.+]', line) is not None


def _assert_valid_line(line: str):
    if _check_valid_line(line) is False:
        raise IllegalSyntaxTreePrintoutError(f'Illegal line <{line}>')


def _assert_valid_line_items(line: str, items: list[str]):
    if len(items) < 1 or len(items) > 3:
        raise IllegalSyntaxTreePrintoutError(f'Illegal line <{line}>')


def _find_child_row(matrix: list[str], row: int, column: int, is_left_child: bool) -> Optional[int]:
    while True:
        row = row + 1 if is_left_child else row - 1
        if row >= len(matrix) or column >= len(matrix[row]):
            return None  # out of bound
        if matrix[row][column] == '|':
            continue
        elif matrix[row][column] == '+':
            return row
        else:
            return None  # unrelated characters
