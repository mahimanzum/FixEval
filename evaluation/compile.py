import os
import sys
import shutil
sys.path.append("..")

import argparse
from tqdm import tqdm
from src.codegen.preprocessing.lang_processors.java_processor import JavaProcessor
from src.codegen.preprocessing.lang_processors.python_processor import PythonProcessor
from subprocess import run, check_output, CalledProcessError, STDOUT, PIPE

root_folder = "../third_party"
jprocessor = JavaProcessor(root_folder=root_folder)
pyprocessor = PythonProcessor(root_folder=root_folder)


def check_python(args):
    programs = []
    with open(args.input_file, encoding='utf8') as f:
        for line in f:
            programs.append(line.strip())

    success, error, num_syntax_error, num_indent_error = 0, 0, 0, 0
    for program in tqdm(programs, total=len(programs)):
        # find public class name
        public_class_name = 'main'
        if "public class" in program:
            public_class_name = program.split("public class", 1)[1].split()[0]

        program = pyprocessor.detokenize_code(program)
        filename = '{}.py'.format(public_class_name)
        with open(filename, 'w', encoding='utf8')as fw:
            fw.write(program)

        command = ["python", "-m", "py_compile", filename]
        p = run(command, stderr=PIPE)
        error_msg = p.stderr.decode("utf-8")
        if len(error_msg) == 0:
            success += 1
        else:
            error += 1
            if "SyntaxError: " in error_msg:
                num_syntax_error += 1
            elif "IndentationError: " in error_msg:
                num_indent_error += 1

        if os.path.isfile(filename):
            os.remove(filename)

    print('Success - {}, Errors - {} [Syntax - {}, Indent - {}]'.format(
        success, error, num_syntax_error, num_indent_error)
    )


def check_java(args):
    programs = []
    with open(args.input_file, encoding='utf8') as f:
        for line in f:
            programs.append(line.strip())

    success, error, num_errors = 0, 0, 0
    for program in tqdm(programs, total=len(programs)):
        # find public class name
        #print(program)
        #rint("#####")
        #program=program.replace("import .", "import java .")
        public_class_name = 'main'
        if "public class" in program:
            tokens = program.split("public class", 1)
            if len(tokens) == 2 and len(tokens[1]) > 0:
                public_class_name = tokens[1].split()[0]

        program = jprocessor.detokenize_code(program)
        filename = 'garbage/{}.java'.format(public_class_name)
        class_filename = 'garbage/{}.class'.format(public_class_name)
        #program.replace("import . util . * ;", "import java . util . * ;")
        with open(filename, 'w', encoding='utf8')as fw:
            fw.write(program)

        #print(program)
        #print("####")
        command = ["javac", filename, "-d", "garbage/"]
        try:
            check_output(command, stderr=STDOUT)
            success += 1
        except CalledProcessError as e:
            error += 1
            error_count = e.output.decode().split()[-2]
            num_errors += int(error_count)
            #print(success,error)
            #print("Error Message: ", e.output.decode())
            #print("#####  ")
            #print(program)
            #print("###########################")
        
        dir = 'garbage'
        for filename in os.listdir(dir):
            file_path = os.path.join(dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        #if os.path.isfile(filename):
        #    os.remove(filename)
        #if os.path.isfile(class_filename):
        #    os.remove(class_filename)
        #os.system("rm *.class > /dev/null")
    print('Success - {}, Errors - {} [Total - {}]'.format(success, error, num_errors))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, help='Source input file')
    parser.add_argument("--language", type=str, help='Language name')
    args = parser.parse_args()
    if args.language == 'java':
        check_java(args)
    if args.language == 'python':
        check_python(args)
