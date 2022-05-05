from glob import glob
import pandas as pd
import matplotlib.pyplot as plt
import json
from joblib import Parallel, delayed, parallel_backend
from multiprocessing import Process, Lock
from tqdm import tqdm
import json
from collections import defaultdict
import subprocess
from subprocess import Popen, PIPE, STDOUT
import sys
import argparse
import os
from joblib import Parallel, delayed
from subprocess import TimeoutExpired
import threading
import psutil
import resource

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
            content1 = f1.read().strip().split()
            content2 = f2.read().strip().split()
            #print(content1)
            #print("########")
            #print(content2)
            if(len(content1) != len(content2)):
                #print("length not same")
                #print(content1)
                #print("#####")
                #print(content2)
                return False
            for l1, l2 in zip(content1, content2):
                if l1.strip() != l2.strip(): 
                    num1s = l1.strip().split(" ")
                    num2s = l2.strip().split(" ")
                    if(len(num1s) == len(num2s)):
                        for idx in range(len(num1s)):
                            if not check_floating(num1s[idx],num2s[idx]):
                                #print_error(l1, l2)
                                return False
                    else:
                        #print_error(l1, l2)
                        return False
            
            return True
    except Exception as e:
        print("exception = ", e)
        return False

def kill(proc_pid):
    if psutil.pid_exists(proc_pid):
        process = psutil.Process(proc_pid)
        for proc in process.children(recursive=True):
            if psutil.pid_exists(proc.pid):
                proc.kill()
        process.kill()


MAX_VIRTUAL_MEMORY =4* 1024 * 1024 * 1024 # 4*1024 MB
def limit_virtual_memory():
    resource.setrlimit(resource.RLIMIT_AS, (MAX_VIRTUAL_MEMORY, resource.RLIM_INFINITY))

def run_python(code, test_case_folder, idx):
    root_path = f'garbage_py/{idx}'
    isExist = os.path.exists(root_path)
    if not isExist:
        os.makedirs(root_path)

    with open(f'{root_path}/Main.py', 'w+', encoding='utf8') as fw:
        fw.write(code)
    in_files = glob(test_case_folder+"/in/*")
    p1 = subprocess.run(["python","-m", "py_compile", f"{root_path}/Main.py"], stderr=PIPE)
    return_code = p1.returncode
    python2 = False
    if (return_code):
        p1 = subprocess.run(["python2","-m", "py_compile", f"{root_path}/Main.py"], stderr=PIPE)
        return_code = p1.returncode
        python2=True

    if(return_code):
        print("doesnt compile", return_code)
        return False, 0, len(in_files)

    did_not_match = 0
    for in_file in in_files:
        stripped_TC = open(in_file).read().strip()
        with open(f'{root_path}/stripped_TC.txt', 'w+') as f:
            f.write(stripped_TC)
        cmd = f"python {root_path}/Main.py < {root_path}/stripped_TC.txt > {root_path}/cmd_out.txt"
        if (python2):
            cmd = cmd.replace("python", "python2")
        p = Popen(cmd, preexec_fn=limit_virtual_memory, shell=True, stdin=PIPE, stdout=PIPE, stderr=subprocess.DEVNULL, close_fds=True)

        # for Time limit exceeded cases
        try:
            outs, errs = p.communicate(timeout=15)
        except TimeoutExpired:
            kill(p.pid)
            did_not_match+=1
            continue
        
        out_file = in_file.replace("in", "out", 1).replace(".in", ".out", 1)

        p2 = subprocess.Popen(["cp",out_file, f"{root_path}/cmd_out_match.txt"])
        p2.wait()
        if not compare_files(f'{root_path}/cmd_out.txt', f'{root_path}/cmd_out_match.txt'):
            did_not_match+=1
            #print(in_file)
    
    subprocess.run(["rm","-rf",f"{root_path}"])
    return True, len(in_files)-did_not_match,len(in_files)

def run_java(code, test_case_folder, idx):
       
    root_path = f'garbage/{idx}'
    isExist = os.path.exists(root_path)
    if not isExist:
        os.makedirs(root_path)

    with open(f'{root_path}/Main.java', 'w+', encoding='utf8') as fw:
        fw.write(code)
    in_files = glob(test_case_folder+"/in/*")
    p1 = subprocess.run(["javac","-d",f"{root_path}/", f"{root_path}/Main.java"],stderr=PIPE)#, stderr=PIPE
    return_code = p1.returncode
    
    if(return_code):
        return False, 0, len(in_files)

    did_not_match = 0
    
    for in_file in in_files:
        #with open('output.txt', 'a') as f:
        #    f.write(in_file+'\n')
        cmd = f"java -Xmx2000m -cp {root_path}/ Main < {in_file} > {root_path}/cmd_out.txt"
        p = Popen(cmd, shell=True, stdin=PIPE,stderr=subprocess.DEVNULL,stdout=PIPE, close_fds=True)# stderr=subprocess.DEVNULL
        #p.wait()
        # for time Limit exceeded cases
        try:
            outs, errs = p.communicate(timeout=10)
        except TimeoutExpired:
            #print("TLE heppened")
            kill(p.pid)
            did_not_match+=1
            continue            
        #print(open(f"{root_path}/cmd_out.txt", 'r').read())        
        p.wait()
        
        out_file = in_file.replace("in", "out", 1).replace(".in", ".out", 1)
        p2 = subprocess.Popen(["cp",out_file, f"{root_path}/cmd_out_match.txt"])
        p2.wait()
        #print(in_file)
        #print(out_file)
       
        #print(open(f"{root_path}/cmd_out_match.txt", 'r').read())
        if not compare_files(f'{root_path}/cmd_out.txt', f'{root_path}/cmd_out_match.txt'): 
            did_not_match+=1
            #print("comes")

    subprocess.run(["rm","-rf",f"{root_path}"])
    return True, len(in_files)-did_not_match,len(in_files)
FINAL_RESULT = []
def main(args):

    data = getJsonData(args.references)
    
    problemlist=pd.read_csv(args.problem_list)
    problems = defaultdict(list)
    for index, row in problemlist.iterrows():
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
    #print(problems["ABC157"])
    print(len(folders))
    
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
    #print(problems['ABC157'])
    problemid_to_tc = {}
    for key in problems:
        if(key in final_keys):
            #print(key)
            for idx, prob_id in enumerate(problems[key]):
                folder_list = sorted(glob(f"{args.test_cases}/"+key+"/*"))
                if(len(folder_list)==0):
                    folder_list = sorted(glob(f"{args.test_cases}/"+key.lower()+"/*"))
                #if key =="ABC157":
                #    print(folder_list)
                problemid_to_tc[prob_id] = folder_list[idx]
    #print(problemid_to_tc['p02759'])
    print("len(problemid_to_tc) = ", len(problemid_to_tc))
    
    ran_prev, ran_now, total, data_count = 0, 0, 0, 0
    
    invalid_problems = ['p02833','p02764','p03619','p03429', 'p03334','p03110', 'p03836', 'p03394', 'p02678', 'p03046', 'p04035', 'p02669', 'p02977', 'p02997', 'p03938', 'p02692', 'p03267', 'p02975', 'p02825', 'p03952', 'p02731', 'p02936', 'p02902', 'p03263', 'p02972', 'p02690', 'p04007', 'p03257', 'p03095', 'p03746', 'p02903', 'p03097', 'p02963', 'p03245', 'p02976', 'p02694', 'p02697', 'p03044', 'p02861', 'p02850']
    if not os.path.exists("results/"):
        os.makedirs("results/")
    def write_to_file(idx, content):
        with open(f"results/{idx}.txt", 'w+', encoding='utf8') as fw:
            fw.write(content)

    lock = threading.RLock()
    def execute_and_evaluate(idx, dt):
        #print("Processing Idx", idx)
        nonlocal lock
        nonlocal ran_prev
        nonlocal ran_now
        nonlocal total
        nonlocal data_count
        nonlocal invalid_problems
        #print("processing index: ", idx)
        one_example = dt.copy()
        if dt['tgt_id'].split("_")[0] in problemid_to_tc.keys():
            if dt['tgt_id'].split("_")[0] in invalid_problems:
                print(" an invalid problem is in test which should not happen", dt['tgt_id'])
                return
                
            test_case_folder = problemid_to_tc[dt['tgt_id'].split("_")[0]]
            if args.language=='java':
                compiles, correctTC_tgt, totalTC = run_java(dt['detokenized_tgt'],test_case_folder, idx)
                one_example['total_test_cases'] = totalTC
                if(compiles and correctTC_tgt == totalTC):
                    _, correctTC_src, _ = run_java(dt['detokenized_src'],test_case_folder, idx)
                    one_example['test_cases_run_by_src'] = correctTC_src
                    one_example['test_cases_run_by_generations'] = []
                    for generation in dt['detokenized_generations']:
                        _, correctTC_out, _ = run_java(generation,test_case_folder, idx)
                        one_example['test_cases_run_by_generations'].append(correctTC_out)
                    
                    #if(correctTC_out>correctTC_src):
                    #    write_to_file(idx, "Previous_code: \n"+
                    #    dt['detokenized_src']+"\n ###############   "+"Output Code:\n"+
                    #    dt['detokenized_output']+"\n##########   "+
                    #    "Correct Code:\n"+dt['detokenized_tgt'])
                    with lock:
                        ran_prev +=correctTC_src
                        ran_now +=correctTC_out
                        total+=totalTC
                        data_count+=1 
                        FINAL_RESULT.append(one_example)
                        with open('output.txt', 'a+') as f:
                            f.write(f'ran prev, ran now, total, idx = {ran_prev}, {ran_now}, {total}, {idx}\n')        
                print("ran_prev,ran_now, total, data_count ", ran_prev,ran_now, total, data_count)
            
            #needs change
            if args.language=='python':
                compiles, correctTC_tgt, totalTC = run_python(dt['detokenized_tgt'],test_case_folder, idx)
                one_example['total_test_cases'] = totalTC
                #print(compiles, correctTC_tgt, totalTC)
                
                if(compiles and correctTC_tgt == totalTC):
                    _, correctTC_src, _ = run_python(dt['detokenized_src'],test_case_folder, idx)
                    #print(correctTC_src,correctTC_tgt)
                    one_example['test_cases_run_by_src'] = correctTC_src
                    one_example['test_cases_run_by_generations'] = []
                    #pprint(one_example)
                    
                    for generation in dt['detokenized_generations']:
                        _, correctTC_out, _ = run_python(generation,test_case_folder, idx)
                        one_example['test_cases_run_by_generations'].append(correctTC_out)
                    
                    #if(correctTC_out>correctTC_src):
                    #    write_to_file(idx, "Previous_code: \n"+
                    #    dt['detokenized_src']+"\n ###############   "+"Output Code:\n"+
                    #    dt['detokenized_output']+"\n##########   "+
                    #    "Correct Code:\n"+dt['detokenized_tgt'])
                    with lock:
                        ran_prev +=correctTC_src
                        ran_now +=correctTC_out
                        total+=totalTC
                        data_count+=1 
                        FINAL_RESULT.append(one_example)
                with open('output_py.txt', 'a') as f:
                    f.write(f'ran prev, ran now, total, idx, len = {ran_prev}, {ran_now}, {total}, {idx}, {len(FINAL_RESULT)}\n')        
                print("ran_prev,ran_now, total, data_count ", ran_prev,ran_now, total, data_count)
        else:
            print(dt['src_id'])
            print("a problem found for which we have no test case which should not happen")
            return
    '''
    for idx in range(0, len(data)):
        execute_and_evaluate(idx, data[idx])
    '''
    import psutil
    current_process = psutil.Process()
    subproc_before = set([p.pid for p in current_process.children(recursive=True)])
    grouped_data = Parallel(n_jobs=4,prefer="threads")(delayed(execute_and_evaluate)(idx, dt) for idx, dt in enumerate(data)) #, prefer="threads"
    subproc_after = set([p.pid for p in current_process.children(recursive=True)])
    for subproc in subproc_after - subproc_before:
        print('Killing process with pid {}'.format(subproc))
        psutil.Process(subproc).terminate()
    
    with open('FINAL_RESULT_python2python_with_verdict.json', 'w', encoding='utf8') as fw:
        json.dump(FINAL_RESULT, fw)   
    
    print("ran_prev,ran_now, total, data_count, ran_prev/total, ran_now/total ", ran_prev,ran_now, total,data_count,ran_prev/total,ran_now/total )
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--references', help="filename of the labels, in jsonl format.")
    parser.add_argument('--problem_list', help="filename of the labels, in jsonl format.")
    
    #parser.add_argument('--predictions', help="filename of the leaderboard predictions, in txt format.")
    
    parser.add_argument("--language", type=str, required=True, help="Name of language")
    parser.add_argument("--test_cases", type=str, required=True, help="Name of language")
    
    params = parser.parse_args()
    main(params)        
    '''
    python ../evaluation/execution_evaluation_TC.py --references test_java2java_with_output.jsonl --language java --test_cases ../atcoder_test_cases --problem_list ../problem_list.csv
    #pandas , matplotlib, sacrebleu , needs to be installed

    pip install pandas
    pip install matplotlib
    pip install sacrebleu=="1.4.5" mecab-python3==0.996.5 unidic-lite tree-sitter javalang
    
    '''