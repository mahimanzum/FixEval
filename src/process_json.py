from glob import glob
import pandas as pd
import matplotlib.pyplot as plt
import json
from joblib import Parallel, delayed, parallel_backend
from multiprocessing import Process, Lock
from tqdm import tqdm
import os
import json
import threading
import timeout_decorator 

def getJsonData(JsonFile):
    with open(JsonFile, encoding="utf8") as f:
        data = json.load(f)
    return data

data = getJsonData("data/processed.json")
ans = 0
for user in tqdm(data.keys()):
    for problem_id in data[user].keys():
        ans+=len(data[user][problem_id])
print("total data = ", ans)

from difflib import SequenceMatcher
from codegen.preprocessing.lang_processors.java_processor import JavaProcessor
from codegen.preprocessing.lang_processors.python_processor import PythonProcessor

root_folder = "../third_party"
jprocessor = JavaProcessor(root_folder=root_folder)
pyprocessor = PythonProcessor(root_folder=root_folder)

class Solution:
    def __init__(
            self,
            source,
            lang,
            problem_id,
            code_tokens,
            functions_standalone=[],
            functions_class=[],
            submission_id="",
            verdict=""
    ):
        self.source = source
        self.lang = lang
        self.problem_id = problem_id
        self.code_tokens = code_tokens
        self.submission_id = submission_id
        self.functions_standalone = functions_standalone
        self.functions_class = functions_class
        self.verdict=verdict

    def __repr__(self):
        return 'source: ' + self.source + '\n' + \
               'lang: ' + self.lang + '\n' + \
               'problem_id: ' + self.problem_id + '\n' + \
               'code: ' + self.code_tokens + '\n' + \
               'submission_id: ' + self.submission_id + '\n' + \
               'verdict: ' + self.verdict + '\n'

    def __str__(self):
        return 'source: ' + self.source + '\n' + \
               'lang: ' + self.lang + '\n' + \
               'problem_id: ' + self.problem_id + '\n' + \
               'code: ' + self.code_tokens + '\n' + \
               'submission_id: ' + self.submission_id + '\n'+ \
               'verdict: ' + self.verdict + '\n'
    def toJSON(self):
        return self.__dict__

@timeout_decorator.timeout(1) 
def calculate_similarity(code1_tokens, code2_tokens):
    code1 = ' '.join(code1_tokens)
    code2 = ' '.join(code2_tokens)
    return SequenceMatcher(None, code1, code2).ratio()

#Lock = threading.Lock()

def write_output_to_file(problems, file_to_write):
    Lock.acquire()
    mode = 'w'
    if os.path.exists(file_to_write):
        mode = 'a'
        with open(file_to_write, mode, encoding='utf8') as fw:
            fw.write('\n')
    with open(file_to_write, mode, encoding='utf8') as fw:
        fw.write('\n'.join([json.dumps(p) for p in problems]))
    Lock.release()

java_file_id = 0
python_file_id = 0
java_solutions = []
python_solutions = []

def write_output_to_json_file(file_name, one_example={}, fnl = False):
    global java_solutions
    global python_solutions
    global java_file_id
    global python_file_id
    #global Lock

    if one_example[1]['submission_id'] == "s473235135":
        print(one_example[1]['code_tokens'])
    return
    
    if(file_name =='Java'):
        #Lock.acquire()
        if not fnl:
            java_solutions.append(one_example)
        #print("java len", len(java_solutions))
        if(fnl or len(java_solutions)==10000):
            pth = '../data/java/jsons/{}.json'.format(java_file_id)
            with open(pth, 'w+', encoding="utf8") as f:
                json.dump(java_solutions, f)
            java_solutions=[]
            java_file_id+=1
        #Lock.release()
    if(file_name=='Python'):
        #Lock.acquire()
        #print("python len", len(python_solutions))
        if not fnl:
            python_solutions.append(one_example)
        if(fnl or len(python_solutions)==10000):
            pth = '../data/python/jsons/{}.json'.format(python_file_id)
            with open(pth, 'w+', encoding="utf8") as f:
                json.dump(python_solutions, f)
            python_solutions=[]
            python_file_id+=1
        #Lock.release()
    
def process_user(user_id):
    for problem_id in data[user_id].keys():
        #print("problem id = ", problem_id)
        submissions = data[user_id][problem_id]

        acceptedJavaSolution = ""
        closeJavaSolution = ""
        acceptedPythonSolution = ""
        closePythonSolution = ""

        functions_standalone_py=[]
        functions_class_py = []
        functions_standalone_java=[]
        functions_class_java = []

        closeSubmissionIdpy = ""
        closeSubmissionIdjava=""
        submission_id_py=""
        submission_id_java=""
        verdict_py=""
        verdict_java=""

        for submisson in submissions:
            try:
                #print("in submission 152")
                if(submisson[2]=="Java"):
                    if(submisson[5]=="Accepted"):
                        solution_path = "../Project_CodeNet/data/"+problem_id+"/Java/"+submisson[0]+'.java'
                        with open(solution_path, 'r', encoding='utf8') as f:
                            code = f.read()
                            acceptedJavaSolution = code[::]
                            submission_id_java = submisson[0]
                            #code_tokens_java = jprocessor.tokenize_code(code)
                            #fn_standalone_java, fn_class_java = jprocessor.extract_functions(code_tokens_java)
                            #functions_standalone_java = [(jprocessor.get_function_name(fn), fn) for fn in fn_standalone_java]
                            #functions_class_java = [(jprocessor.get_function_name(fn), fn) for fn in fn_class_java]


                if(submisson[2]=="Python"):
                    if(submisson[5]=="Accepted"):
                        solution_path = "../Project_CodeNet/data/"+problem_id+"/Python/"+submisson[0]+'.py'
                        with open(solution_path, 'r', encoding='utf8') as f:
                            code = f.read()
                            acceptedPythonSolution = code[::]
                            submission_id_py = submisson[0]
                            #code_tokens_py = pyprocessor.tokenize_code(code)
                            #fn_standalone_py, fn_class_py = pyprocessor.extract_functions(code_tokens_py)
                            #functions_standalone_py = [(pyprocessor.get_function_name(fn), fn) for fn in fn_standalone_py]
                            #functions_class_py = [(pyprocessor.get_function_name(fn), fn) for fn in fn_class_py]
            except BaseException as error:
                print("error for submission top problem id line 175",problem_id, submisson, error)
                pass
        
        java_min_distance = 999999
        python_min_distance = 999999

        for submisson in submissions:
            #print("in submission 185")
            try:
                if(submisson[2]=="Java"):
                    if(submisson[5]!="Accepted"):
                        solution_path = "../Project_CodeNet/data/"+problem_id+"/Java/"+submisson[0]+'.java'
                        with open(solution_path, 'r', encoding='utf8') as f:
                            code = f.read()
                            closeJavaSolution=code[::]
                            closeSubmissionIdjava = submisson[0]
                            verdict_java=submisson[5]
                            
                            if(len(acceptedJavaSolution)*len(closeJavaSolution)):
                                write_output_to_json_file("Java", (Solution(
                                                            "source",
                                                            'java',
                                                            problem_id,
                                                            closeJavaSolution,
                                                            functions_standalone_java,
                                                            functions_class_java,
                                                            closeSubmissionIdjava,
                                                            verdict_java
                                                        ).toJSON(),Solution(
                                                            "source",
                                                            'java',
                                                            problem_id,
                                                            acceptedJavaSolution,
                                                            functions_standalone_java,
                                                            functions_class_java,
                                                            submission_id_java,
                                                            "Accepted"
                                                        ).toJSON())
                                                    )



                            '''
                            #for closest solution
                            dis = calculate_similarity(code,acceptedJavaSolution)
                            if(dis<java_min_distance):
                                closeJavaSolution=code[::]
                                java_min_distance = dis
                                closeSubmissionIdjava = submisson[0]
                                verdict_java=submisson[5]
                            '''
                if(submisson[2]=="Python"):
                    if(submisson[5]!="Accepted"):
                        solution_path = "../Project_CodeNet/data/"+problem_id+"/Python/"+submisson[0]+'.py'
                        with open(solution_path, 'r', encoding='utf8') as f:
                            code = f.read()
                            closePythonSolution=code[::]
                            closeSubmissionIdpy = submisson[0]
                            verdict_py=submisson[5]
                            if(len(acceptedPythonSolution)*len(closePythonSolution)):  
                                write_output_to_json_file("Python",(Solution(
                                                            "source",
                                                            'python',
                                                            problem_id,
                                                            closePythonSolution,
                                                            functions_standalone_py,
                                                            functions_class_py,
                                                            closeSubmissionIdpy,
                                                            verdict_py
                                                        ).toJSON(),Solution(
                                                            "source",
                                                            'python',
                                                            problem_id,
                                                            acceptedPythonSolution,
                                                            functions_standalone_py,
                                                            functions_class_py,
                                                            submission_id_py,
                                                            "Accepted"
                                                        ).toJSON())
                                                    )

                            '''
                            dis = calculate_similarity(code,acceptedPythonSolution)
                            if(dis<python_min_distance):
                                closePythonSolution=code[::]
                                python_min_distance = dis
                                closeSubmissionIdpy = submisson[0]
                                verdict_py=submisson[5]
                            '''
            except BaseException as error:
                print("error for submission line 265", submisson, error)
                pass
        '''
        if(len(acceptedPythonSolution)*len(closePythonSolution)):  
            write_output_to_json_file("Python",(Solution(
                                        "source",
                                        'python',
                                        problem_id,
                                        closePythonSolution,
                                        functions_standalone_py,
                                        functions_class_py,
                                        closeSubmissionIdpy,
                                        verdict_py
                                    ).toJSON(),Solution(
                                        "source",
                                        'python',
                                        problem_id,
                                        acceptedPythonSolution,
                                        functions_standalone_py,
                                        functions_class_py,
                                        submission_id_py,
                                        "Accepted"
                                    ).toJSON())
                                )
        if(len(acceptedJavaSolution)*len(closeJavaSolution)):
            write_output_to_json_file("Java", (Solution(
                                        "source",
                                        'java',
                                        problem_id,
                                        closeJavaSolution,
                                        functions_standalone_java,
                                        functions_class_java,
                                        closeSubmissionIdjava,
                                        verdict_java
                                    ).toJSON(),Solution(
                                        "source",
                                        'java',
                                        problem_id,
                                        acceptedJavaSolution,
                                        functions_standalone_java,
                                        functions_class_java,
                                        submission_id_java,
                                        "Accepted"
                                    ).toJSON())
                                )
    '''
        #write in a file next task
    '''
    if(len(java_solutions)):
        write_output_to_file(java_solutions, "java_solutions.jsonl")
    if(len(python_solutions)):
        write_output_to_file(python_solutions, "python_solutions.jsonl")
    '''

if __name__=="__main__":
    #Parallel(n_jobs=8,prefer="threads")(delayed(process_user)(user) for user in tqdm(list(data.keys())))
    index = 0
    #process_user('u745688558')
    for user in tqdm(list(data.keys())): #[:10]
        print("Processing index: {}, User: {}".format(index, user))
        process_user(user)
        index+=1
    write_output_to_json_file("Python", fnl=True)
    write_output_to_json_file("Java", fnl=True)
    
    
# stuck in u326609687 idx 30535+46 30581 near