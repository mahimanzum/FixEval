from glob import glob
import pandas as pd
import matplotlib.pyplot as plt
import json
from joblib import Parallel, delayed, parallel_backend
from multiprocessing import Process, Lock
from tqdm import tqdm
import json
from collections import defaultdict
from codegen.preprocessing.lang_processors.java_processor import JavaProcessor
from codegen.preprocessing.lang_processors.python_processor import PythonProcessor
import subprocess
import filecmp
from subprocess import Popen, PIPE, STDOUT
import sys
import argparse

def getJsonData(JsonFile):
    with open(JsonFile, encoding="utf8") as f:
        data = json.load(f)
    return data

def only_digits(num):
    return num.replace("-", "").replace("+", "").replace('.','',1).replace("E","").isdigit()

def check_floating(n1, n2):
    if (not only_digits(n1)) or (not only_digits(n2)):
        return False
    #print(float(n1), float(n2))
    if abs(float(n1)-float(n2))<1e-6:
        return True
    return False

def print_error(l1, l2):
    print("###")
    print(l1)
    print("###")
    print(l2)
    print("###")

def compare_files(file1, file2):
    try:
        with open(file1) as f1, open(file2) as f2: 
            content1 = f1.read().split()
            content2 = f2.read().split()
            for l1, l2 in zip(content1, content2):
                if l1.strip() != l2.strip(): 
                    num1s = l1.strip().split(" ")
                    num2s = l2.strip().split(" ")
                    if(len(num1s) == len(num2s)):
                        for idx in range(len(num1s)):
                            if not check_floating(num1s[idx],num2s[idx]):
                                print_error(l1, l2)
                                return False
                    else:
                        print_error(l1, l2)
                        return False
            return True
    except Exception as e:
        print("exception = ", e)
        return False
def run_python(code, test_case_folder):
    with open('garbage/Main.py', 'w', encoding='utf8') as fw:
        fw.write(code)
    in_files = glob(test_case_folder+"/in/*")
    p1 = subprocess.run(["python","-m", "py_compile", "garbage/Main.py"], stderr=PIPE)
    return_code = p1.returncode
    python2 = False
    if (return_code):
        p1 = subprocess.run(["python2","-m", "py_compile", "garbage/Main.py"], stderr=PIPE)
        return_code = p1.returncode
        python2=True

    if(return_code):
        print("doesnt compile", return_code)
        print(code)
        
        sys.exit(0)
        return False, 0, len(in_files)

    did_not_match = 0
    for in_file in in_files:
        stripped_TC = open(in_file).read().strip()
        with open('garbage/stripped_TC.txt', 'w') as f:
            f.write(stripped_TC)
        cmd = "python garbage/Main.py < {} > garbage/cmd_out.txt".format('garbage/stripped_TC.txt')
        if (python2):
            cmd = cmd.replace("python", "python2")
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=subprocess.DEVNULL, close_fds=True)
        p.wait()
        out = in_file.split("/")
        out[5] = "out"
        out_file ="/".join(out)
        out_file = out_file.replace(".in", ".out")

        p2 = subprocess.Popen(["cp",out_file, "garbage/cmd_out_match.txt"])
        p2.wait()
        if not compare_files('garbage/cmd_out.txt', 'garbage/cmd_out_match.txt'):
            did_not_match+=1
            print(in_file)
    return True, len(in_files)-did_not_match,len(in_files)

def run_java(code, test_case_folder):

    with open('garbage/Main.java', 'w', encoding='utf8') as fw:
        fw.write(code)
    in_files = glob(test_case_folder+"/in/*")
    p1 = subprocess.run(["javac","garbage/Main.java"], stderr=PIPE)
    return_code = p1.returncode
    if(return_code):
        return False, 0, len(in_files)

    did_not_match = 0
    for in_file in in_files:
        cmd = "java garbage/Main < {} > garbage/cmd_out.txt".format(in_file)
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=subprocess.DEVNULL, close_fds=True)
        p.wait()
        out = in_file.split("/")
        out[5] = "out"
        out_file ="/".join(out)
        out_file = out_file.replace(".in", ".out")

        p2 = subprocess.Popen(["cp",out_file, "garbage/cmd_out_match.txt"])
        p2.wait()
        if not compare_files('garbage/cmd_out.txt', 'garbage/cmd_out_match.txt'):

            did_not_match+=1
    return True, len(in_files)-did_not_match,len(in_files)

def main(args):

    data = getJsonData(args.input)

    root_folder = "../third_party"
    jprocessor = JavaProcessor(root_folder=root_folder)
    pyprocessor = PythonProcessor(root_folder=root_folder)
    
    processor = jprocessor if args.lang == 'java' else pyprocessor
    #print(processor)
    problemlist=pd.read_csv("../Project_CodeNet/metadata/problem_list.csv")
    problems = defaultdict(list)
    for index, row in tqdm(problemlist.iterrows()):
        if(row['dataset']=='AtCoder'):
            if("AtCoder Regular Contest" in row['name']):
                number = row['name'].split(" ")[3]
                problems["ARC"+number].append(row['id'])
            if("AtCoder Beginner Contest" in row['name']):
                number = row['name'].split(" ")[3]
                problems["ABC"+number].append(row['id'])
            if("AtCoder Grand Contest" in row['name']):
                number = row['name'].split(" ")[3]
                problems["AGC"+number].append(row['id'])
    folders = glob(f"{args.test_cases}/*")

    final_keys = []
    for idx in range(len(folders)):
        folders[idx] = folders[idx].replace(f"{args.test_cases}/", "")
    #print(folders)
    for key in problems.keys():
        if key in folders:
            if len(problems[key]) == len(glob(f"{args.test_cases}/"+key+"/*")):
                final_keys.append(key)
                
        elif key.lower() in folders :
            if len(problems[key]) == len(glob(f"{args.test_cases}/"+ key.lower() +"/*")):
                final_keys.append(key)

    problemid_to_tc = {}
    for key in problems:
        if(key in final_keys):
            for idx, prob_id in enumerate(problems[key]):
                folder_list = glob(f"{args.test_cases}/"+key+"/*")
                if(len(folder_list)==0):
                    folder_list = glob(f"{args.test_cases}/"+key.lower()+"/*")
                problemid_to_tc[prob_id] = folder_list[idx]
    
    print("len(problemid_to_tc) = ", len(problemid_to_tc))
    
    ran, total= 0, 0
    uniq = set()
    invalid_problems = ['p02833','p02764','p03619','p03429', 'p03334','p03110', 'p03836', 'p03394', 'p02678', 'p03046', 'p04035', 'p02669', 'p02977', 'p02997', 'p03938', 'p02692', 'p03267', 'p02975', 'p02825', 'p03952', 'p02731', 'p02936', 'p02902', 'p03263', 'p02972', 'p02690', 'p04007', 'p03257', 'p03095', 'p03746', 'p02903', 'p03097', 'p02963', 'p03245', 'p02976', 'p02694', 'p02697', 'p03044', 'p02861', 'p02850']
    for dt in tqdm(data[629:]): #9630
        if dt['tgt_id'].split("_")[0] in problemid_to_tc.keys():
            if dt['tgt_id'].split("_")[0] in invalid_problems:
                print(" an invalid problem is in test which should not happen")
                return
                continue
            
            code = processor.detokenize_code(dt['tgt'])
            if dt['tgt_id'] in uniq:
                continue
            uniq.add(dt['tgt_id'])
            
            test_case_folder = problemid_to_tc[dt['tgt_id'].split("_")[0]]
            if args.lang=='java':
                compiles, correctTC, totalTC = run_java(code,test_case_folder)
                if(correctTC != totalTC):
                    print("missed a test case", dt['tgt_id'])
                ran+=correctTC
                total+=totalTC
            if args.lang=='py':
                compiles, correctTC, totalTC = run_python(code,test_case_folder)
                if(correctTC != totalTC):
                    print(correctTC, totalTC)
                    print("missed a test case", dt['tgt_id'])
                ran+=correctTC
                total+=totalTC
            
        else:
            print(dt['src_id'])
            print("a problem found for which we have no test case which should not happen")
            return
    
    print("ran, total = ", ran, total)
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Path to sources")
    parser.add_argument("--lang", type=str, required=True, help="Name of language")
    parser.add_argument("--test_cases", type=str, required=True, help="Name of language")
    
    #../src/atcoder_test_cases
    params = parser.parse_args()
    main(params)        