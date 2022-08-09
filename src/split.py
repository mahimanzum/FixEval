import os
import json
import random
import argparse
from tqdm import tqdm
from pprint import pprint
from glob import glob
from collections import defaultdict
import sys
from difflib import SequenceMatcher
import pandas as pd
from random import sample
from deduplication import DuplicateDetector
sys.path.append("..")
random.seed(1234)
from joblib import Parallel, delayed

from codegen.preprocessing.lang_processors.java_processor import JavaProcessor
from codegen.preprocessing.lang_processors.python_processor import PythonProcessor

root_folder = "../third_party"
jprocessor = JavaProcessor(root_folder=root_folder)
pyprocessor = PythonProcessor(root_folder=root_folder)

def getJsonData(JsonFile):
    with open(JsonFile, encoding="utf8") as f:
        data = json.load(f)
    return data
def load_collected_test_suit(args):
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
    return problemid_to_tc

def calculate_similarity(code1_tokens, code2_tokens):
    code1 = ' '.join(code1_tokens)
    code2 = ' '.join(code2_tokens)
    return SequenceMatcher(None, code1, code2).ratio()

def deduplicate_jaccard(database, processor):
    accepted_sub = set()
    problem_to_dataidx = defaultdict(list)
    sim = []
    for idx,dt in enumerate(database):    
        if dt[1]['submission_id'] not in accepted_sub:
            accepted_sub.add(dt[1]['submission_id'])
            problem_to_dataidx[dt[1]['problem_id']].append(idx)
    duplicate_submission_id = []
    def solve(problem):
        print(len(sim))
        for idx in problem_to_dataidx[problem]:
            for idx2 in problem_to_dataidx[problem]:
                if idx!=idx2:
                    sim.append(calculate_similarity(database[idx][1]['code_tokens'], database[idx2][1]['code_tokens']))
    
    #Parallel(n_jobs=8, prefer="threads")(delayed(solve)(problem) for problem in tqdm(problem_to_dataidx.keys()))
    #print(len(sim))
    #print(sum(sim) / len(sim))
    #return []
    exclude_submissions = set()
    for problem in tqdm(problem_to_dataidx.keys()):
        try:
            detector = DuplicateDetector()
            data_idx_list = problem_to_dataidx[problem]
            if(len(data_idx_list)<=3):
                continue
            for idx in data_idx_list:
                detector.add_file(id = idx,tokens = processor.tokenize_code(database[idx][1]['code_tokens']))   
            exclude_document_ids = detector.compute_ids_to_exclude()
            for id in exclude_document_ids:
                exclude_submissions.add(database[idx][1]['submission_id'])
        except Exception as e:
            #print(e)
            pass
    deduplication_database = []
    for data in database:
        if data[1]['submission_id'] not in exclude_submissions:
            deduplication_database.append(data.copy())
    return deduplication_database
    

def split(args):
    train_examples = []
    valid_examples = []
    test_examples = []
    unique_data = set()
    idx = 0
    files = args.src_file
    #print(files)
    data = []
    for file in glob(files+'*.json'):
        print(file)
        with open(file, 'r') as f:
            temp = json.load(f)
            data.extend(temp)
    data = data[:-1]
    problems_of_lang = set()
    for ex in tqdm(data):
        problems_of_lang.add(ex[0]['problem_id'])
    processor = jprocessor if args.lang == 'java' else pyprocessor
    print("previous data size ", len(data))
    data = deduplicate_jaccard(data,processor)
    #sys.exit(0)
    print("data size after deduplication", len(data))
    

    problemid_to_tc = load_collected_test_suit(args)

    invalid_problems = ['p03619','p03429', 'p03334','p03110', 'p03836', 'p03394', 'p02678', 'p03046', 'p04035', 'p02669', 'p02977', 'p02997', 'p03938', 'p02692', 'p03267', 'p02975', 'p02825', 'p03952', 'p02731', 'p02936', 'p02902', 'p03263', 'p02972', 'p02690', 'p04007', 'p03257', 'p03095', 'p03746', 'p02903', 'p03097', 'p02963', 'p03245', 'p02976', 'p02694', 'p02697', 'p03044', 'p02861', 'p02850']
    print("len of problems solved in ", args.lang, len(problems_of_lang))
    
    train_problems = set()
    valid_problems = set()
    test_problems = []
    
    for problem in problemid_to_tc.keys():
        if problem in problems_of_lang and problem not in invalid_problems:
            test_problems.append(problem)
    test_problems = list(set(test_problems))

    valid_problems = set(test_problems[int(0.1*len(problems_of_lang)):min(len(test_problems),int(0.2*len(problems_of_lang)))])
    test_problems = test_problems[:int(0.1*len(problems_of_lang))]
    test_problems = set(test_problems)
    
    

    print("len test problems", len(test_problems))

    all_data = defaultdict(list)
    
    for ex in tqdm(data):
        #ex = json.loads(line)
        try:
            if (len(ex[0]['code_tokens'])<6000 and len(ex[1]['code_tokens'])<6000):
                problem_id = ex[0]['problem_id']+'_'+ex[0]['submission_id']
                #code_tokens_java = jprocessor.tokenize_code(code)
                uniq_str = ex[0]['problem_id']+ex[0]['code_tokens']+ex[1]['code_tokens']

                if(uniq_str not in unique_data):
                    unique_data.add(uniq_str)
                else:
                    continue
                
                one_ex = {
                    "src_id": problem_id,
                    "src": processor.tokenize_code(ex[0]['code_tokens']),
                    "src_verdict": ex[0]['verdict'],
                    "tgt": processor.tokenize_code(ex[1]['code_tokens']),
                    "tgt_id": ex[1]['problem_id']+'_'+ex[1]['submission_id']
                }
                
                if ex[0]['problem_id'] in test_problems:
                    # found a valid problem with suitable test cases and data is less than 20 % 
                    test_examples.append(one_ex)
                else:
                    # not suitable test cases so adding in train
                    all_data[ex[0]['problem_id']].append(one_ex)
                
        except Exception as e:
            pass
            #print(e)
    
    #this splitting is no valid
    #need to split by problem
    # make sure the problems used for testing not going in training

    
    for idx,problem in enumerate(list(all_data.keys())):
        submissions = all_data[problem]
        if problem not in valid_problems:
            train_problems.add(problem)
            train_examples.extend(submissions)
        else:
            valid_examples.extend(submissions)

    del all_data

    print("train , valid, test length = ",len(train_problems), len(valid_problems), len(test_problems))
    
    print("intersection between problems ...")
    print(train_problems & test_problems)
    print(train_problems & valid_problems)
    print(test_problems & valid_problems)
    
    with open(os.path.join(args.out_dir, 'train.jsonl'), 'w', encoding='utf8') as fw:
        json.dump(train_examples, fw)
        #fw.write('\n'.join([json.dumps(ex) for ex in train_examples]) + '\n')

    with open(os.path.join(args.out_dir, 'valid.jsonl'), 'w', encoding='utf8') as fw:
        json.dump(valid_examples, fw)
        #fw.write('\n'.join([json.dumps(ex) for ex in valid_examples]) + '\n')

    with open(os.path.join(args.out_dir, 'test.jsonl'), 'w', encoding='utf8') as fw:
        json.dump(test_examples, fw)
        #fw.write('\n'.join([json.dumps(ex) for ex in test_examples]) + '\n')


def prepare(args):

    def single_prepare(split):
        file_prefix = '{}.{}-{}'.format(split, args.lang,args.lang)
        id_file = os.path.join(args.out_dir, '{}.id'.format(file_prefix))
        src_file = os.path.join(args.out_dir, 'src_{}.{}'.format(file_prefix, args.lang))
        tgt_file = os.path.join(args.out_dir, 'tgt_{}.{}'.format(file_prefix, args.lang))

        with open(id_file, 'w', encoding='utf8') as id_writer, \
            open(src_file, 'w', encoding='utf8') as src_writer, \
            open(tgt_file, 'w', encoding='utf8') as tgt_writer, \
            open(os.path.join(args.src_dir, '{}.jsonl'.format(split))) as f:

            data = json.load(f)

            for ex in tqdm(data):
                
                src = " ".join(ex['src'])
                tgt = " ".join(ex['tgt'])
                id_writer.write(ex['src_id']+"_"+ex['tgt_id'] + '\n')
                
                if args.with_verdict=="yes":
                    src_writer.write(src+" verdict: "+ex['src_verdict'] + '\n')
                else:
                    src_writer.write(src + '\n')
                
                tgt_writer.write(tgt + '\n')

    single_prepare('train')
    single_prepare('valid')
    single_prepare('test')


if __name__ == '__main__':
    
    # lang either java or python
    # default java
    # python command to run: python split.py --lang python --src_file ../data/python/jsons/ --src_dir ../data/python/processed_with_verdict/ --out_dir ../data/python/processed_with_verdict/ --test_cases ../data/atcoder_test_cases --with_verdict yes
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", type=str, help='Language', default='java')

    parser.add_argument("--src_file", type=str, help='Source file', default='../data/java/jsons/')
    parser.add_argument("--src_dir", type=str, help='Source directory', default='../data/java/processed_with_verdict/') #processed_with_verdict
    parser.add_argument("--out_dir", type=str, help='Output directory', default='../data/java/processed_with_verdict')
    parser.add_argument("--test_cases", type=str, help="Name of language",default='../data/atcoder_test_cases')
    parser.add_argument("--with_verdict", type=str, help="Name of language",default='yes')
    
    args = parser.parse_args()

    #call single function if jsons are already created
    split(args)
    
    prepare(args)
