import shlex
import subprocess
import os
import sys

_working_dir = os.getcwd()
_raw_filenames = [filename for filename in os.listdir('inputs/') if filename.endswith('.mjava')]
_raw_filenames.sort(key=lambda name: ('zz' if '10' in name else 'z' + name) if 'ex' in name else name)
_input_filenames = [os.path.join(_working_dir, 'inputs', name) for name in _raw_filenames]


class OutputInfo:
    def __init__(self, *, program_name: str, output: str, decode_error: bool):
        self.program_name = program_name
        self.output = output
        self.decode_error = decode_error


def run_sample_program(executable_filename: str):
    if '/' not in executable_filename:
        raise RuntimeError('Filename must contain </>')

    for input_filename in _input_filenames:
        program_name = input_filename.split('/')[-1][:-6]
        read_process = subprocess.Popen(shlex.split(f'cat "{input_filename}"'), stdout=subprocess.PIPE)
        work_process = subprocess.Popen(shlex.split(f'"{executable_filename}"'),
                                        stdin=read_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = work_process.communicate()
        return_code = work_process.poll()
        try:
            out = out.decode(sys.stdin.encoding)
            err = err.decode(sys.stdin.encoding)
            decode_error = False
        except UnicodeDecodeError:
            out = out.decode(sys.stdin.encoding, errors='ignore')
            err = err.decode(sys.stdin.encoding, errors='ignore')
            decode_error = True
        if return_code != 0:
            raise RuntimeError(f'Invalid sample program return code: {return_code}')
        if len(err) > 0:
            raise RuntimeError(f'Sample program has error output:\n{err}')
        yield OutputInfo(program_name=program_name, output=out, decode_error=decode_error)
