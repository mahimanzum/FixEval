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

def getJsonData(JsonFile):
    with open(JsonFile, encoding="utf8") as f:
        data = json.load(f)
    return data

def check_floating(n1, n2):
    n1 = n1.replace("-", "").replace("+", "")
    n2 = n2.replace("-", "").replace("+", "")
    
    if (not n1.replace('.','',1).replace("E","").isdigit()) or (not n1.replace('.','',1).replace("E","").isdigit()):
        return False
    if abs(float(n1)-float(n2))<1e8:
        return True
    return False
    
def print_error(l1, l2):
    print("###")
    print(l1)
    print("###")
    print(l2)
    print("###")

def compare_files(file1, file2):
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

if __name__ == "__main__":

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
    folders = glob("atcoder_test_cases/*")

    final_keys = []
    for idx in range(len(folders)):
        folders[idx] = folders[idx].replace("atcoder_test_cases/", "")
    #print(folders)
    for key in problems.keys():
        if key in folders:
            if len(problems[key]) == len(glob("atcoder_test_cases/"+key+"/*")):
                final_keys.append(key)
                
        elif key.lower() in folders :
            if len(problems[key]) == len(glob("atcoder_test_cases/"+ key.lower() +"/*")):
                final_keys.append(key)

    problemid_to_tc = {}
    for key in problems:
        if(key in final_keys):
            for idx, prob_id in enumerate(problems[key]):
                folder_list = glob("atcoder_test_cases/"+key+"/*")
                if(len(folder_list)==0):
                    folder_list = glob("atcoder_test_cases/"+key.lower()+"/*")
                problemid_to_tc[prob_id] = folder_list[idx]
    
    print("len(problemid_to_tc) = ", len(problemid_to_tc))

    data = getJsonData("../data/java/processed/test.jsonl")
    root_folder = "../third_party"
    jprocessor = JavaProcessor(root_folder=root_folder)
    uniq = set()
    #code_tokens_java = jprocessor.tokenize_code(code)
    cnt = 0
    done = False
    for dt in tqdm(data[14975:]): #12480+721
        if dt['id'].split("_")[0] in problemid_to_tc.keys():
            #if(dt['tgt_id'].split("_")[1] != "s473235135"):
            #    continue
            cnt+=1
            #print("comes")
            #print(dt['id'])
            #pprint(dt)
            #print(dt['src'])
            code = jprocessor.detokenize_code(dt['tgt'])
            if dt['tgt_id'] in uniq:
                continue
            uniq.add(dt['tgt_id'])

            p3 = subprocess.run(["rm","Main.java"])
            p4 = subprocess.run(["rm","*.class"])

            with open('Main.java', 'w', encoding='utf8') as fw:
                fw.write(code)
            test_case_folder = problemid_to_tc[dt['id'].split("_")[0]]
            in_files = glob(test_case_folder+"/in/*")
            p1 = subprocess.run(["javac","Main.java"],stderr=PIPE)
            return_code = p1.returncode
            if(return_code):
                print("######## doesnt compile  ############")
                print(dt['tgt_id'])
                continue

            for in_file in in_files:
                #subprocess.run(["java","Main" ,"<",in_files[0], ">", "cmd_out.txt"], shell=True)
                cmd = "java Main < {} > cmd_out.txt".format(in_file)
                p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
                p.wait()
                #output = p.stdout
                #print(output)
                out = in_file.split("/")
                out[3] = "out"
                out_file ="/".join(out)
                out_file = out_file.replace(".in", ".out")

                p2 = subprocess.Popen(["cp",out_file, "cmd_out_match.txt"])
                p2.wait()
                if not compare_files('cmd_out.txt', 'cmd_out_match.txt'):
                    print(dt['tgt_id'])
                    print(in_file)
            