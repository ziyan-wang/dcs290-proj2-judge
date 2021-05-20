import sys
from internal.checker import check
from internal.executor import run_sample_program
from internal.rule_parser import parse_rules, RuleNotFoundError
from internal.tree_parser import parse_tree, IllegalSyntaxTreePrintoutError


def main():
    if len(sys.argv) != 2:
        sys.stderr.write('usage: python src/judge.py <tested_program_path>\n')
        sys.exit(1)

    tested_program_filename = sys.argv[1]
    print(f'Testing {tested_program_filename}')
    for output_info in run_sample_program(tested_program_filename):
        sys.stdout.write(f'{output_info.program_name}.mjava: '.ljust(15))
        if output_info.decode_error:
            sys.stdout.write('Decode error; ')
        try:
            tree, invalid_lines = parse_tree(output_info.output)
        except IllegalSyntaxTreePrintoutError as error:
            sys.stdout.write(f'{repr(error)}\n')
            continue
        if len(invalid_lines) > 0:
            sys.stdout.write(f'Found {len(invalid_lines)} invalid lines; ')
        try:
            rules = parse_rules(f'rules/{output_info.program_name}.json')
        except RuleNotFoundError:
            sys.stdout.write('Pass (no rule)\n')
            continue
        violated_rules = check(tree, rules)
        if len(violated_rules) > 0:
            sys.stdout.write(f'{len(violated_rules)} Error(s): {", ".join(violated_rules)}\n')
        else:
            sys.stdout.write('Pass\n')


def test():
    with open('sample_output/hello.out') as f:
        syntax_tree_printout = f.read()
    tree = parse_tree(syntax_tree_printout)
    rules = parse_rules('rules/hello.json')
    violated_rules = check(tree, rules)
    if len(violated_rules) > 0:
        print('ERROR! violated rules: ')
        print(', '.join(violated_rules))
    else:
        print('OK')


if __name__ == '__main__':
    main()
