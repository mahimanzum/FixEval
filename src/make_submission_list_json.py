from glob import glob
import pandas as pd
import matplotlib.pyplot as plt
import json
from joblib import Parallel, delayed, parallel_backend
from multiprocessing import Process, Lock
from tqdm import tqdm


problemCsvList = glob("../Project_CodeNet/metadata/*.csv")
solutionFolderList = glob("../Project_CodeNet/data/*")
problemListCsvDF =pd.read_csv("../Project_CodeNet/metadata/problem_list.csv")
submissions = {}

def read_dic(path):
    return json.loads(path)

def write(data, path):
    a_file = open(path, "w")
    json.dumps(data, a_file)
    a_file.close()


    
def process(id):
    location = "../Project_CodeNet/metadata/"+id+'.csv'
    problem_df = pd.read_csv(location)
    #print(problem_df.columns)
    for inddex, row in tqdm(problem_df.iterrows()):
        information_tuple = (row['submission_id'], row['date'],row['language'],row['original_language'], row['filename_ext'], row['status'])
        #lock.acquire()
        if(row['user_id'] in submissions.keys()):
            if(row['problem_id'] in submissions[row['user_id']].keys()):
                submissions[row['user_id']][row['problem_id']].append(information_tuple)
            else:
                submissions[row['user_id']][row['problem_id']] = [information_tuple]
        else:
            submissions[row['user_id']] = {}
            submissions[row['user_id']][row['problem_id']] = [information_tuple]
        
        #lock.release()
    #from pprint import pprint
    #pprint(submissions)
'''
['submission_id', 'problem_id', 'user_id', 'date', 'language',
       'original_language', 'filename_ext', 'status', 'cpu_time', 'memory',
       'code_size', 'accuracy'],
'''  

if __name__=="__main__":
    #lock = Lock()
    #Parallel(n_jobs=4, prefer="threading")(
    #    delayed(process)(row['id'], lock) for index, row in problemListCsvDF.iterrows())
    for index, row in tqdm(problemListCsvDF.iterrows(), total = len(problemListCsvDF)):
        process(row['id'])
    write(submissions, "data/processed.json")