import os
import json
import random
import argparse
from tqdm import tqdm
from pprint import pprint
from glob import glob
from collections import defaultdict
import sys
import pandas as pd
sys.path.append("..")
random.seed(1234)

from codegen.preprocessing.lang_processors.java_processor import JavaProcessor
from codegen.preprocessing.lang_processors.python_processor import PythonProcessor

root_folder = "../third_party"
jprocessor = JavaProcessor(root_folder=root_folder)
pyprocessor = PythonProcessor(root_folder=root_folder)

def load_collected_test_suit():
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
    return problemid_to_tc

def calculate_similarity(code1_tokens, code2_tokens):
    code1 = ' '.join(code1_tokens)
    code2 = ' '.join(code2_tokens)
    return SequenceMatcher(None, code1, code2).ratio()

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
            
    problemid_to_tc = load_collected_test_suit()
    invalid_problems = ['p03619','p03429', 'p03334','p03110', 'p03836', 'p03394', 'p02678', 'p03046', 'p04035', 'p02669', 'p02977', 'p02997', 'p03938', 'p02692', 'p03267', 'p02975', 'p02825', 'p03952', 'p02731', 'p02936', 'p02902', 'p03263', 'p02972', 'p02690', 'p04007', 'p03257', 'p03095', 'p03746', 'p02903', 'p03097', 'p02963', 'p03245', 'p02976', 'p02694', 'p02697', 'p03044', 'p02861', 'p02850']
    
    train_problems = set()
    valid_problems = set()
    test_problems = set()

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
                    "src": jprocessor.tokenize_code(ex[0]['code_tokens']),
                    "src_verdict": ex[0]['verdict'],
                    "tgt": jprocessor.tokenize_code(ex[1]['code_tokens']),
                    "tgt_id": ex[1]['problem_id']+'_'+ex[1]['submission_id']
                }
                
                if ex[0]['problem_id'] in problemid_to_tc.keys() and ex[0]['problem_id'] not in invalid_problems:
                    # found a valid problem with suitable test cases 
                    test_problems.add(ex[0]['problem_id'])
                    test_examples.append(one_ex)
                # not suitable test cases so adding in train
                else:
                    all_data[ex[0]['problem_id']].append(one_ex)
                idx+=1
        except Exception as e:
            print(e)
    
    #this splitting is no valid
    #need to split by problem
    # make sure the problems used for testing not going in training

    num_valid = len(all_data) // 20  # 5% of the total problems goes to validation
        
    for idx,problem in enumerate(list(all_data.keys())):
        submissions = all_data[problem]
        if idx < len(all_data) - num_valid:
            train_problems.add(problem)
            train_examples.extend(submissions)
        else:
            valid_problems.add(problem)
            valid_examples.extend(submissions)

    del all_data

    print("train , valid, test length = ",len(train_examples), len(valid_examples), len(test_examples))
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
                src_writer.write(src+" "+ex['src_verdict'] + '\n')
                tgt_writer.write(tgt + '\n')

    single_prepare('train')
    single_prepare('valid')
    single_prepare('test')


if __name__ == '__main__':
    #need to tokenize here
    #lang either java or py 
    # default java
    # python command to run: python split.py --lang py --src_file ../data/Python/jsons/ --src_dir ../data/Python/processed/ --out_dir ../data/Python/processed/
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", type=str, help='Language', default='java')
    parser.add_argument("--src_file", type=str, help='Source file', default='../data/java/jsons/')
    parser.add_argument("--src_dir", type=str, help='Source directory', default='../data/java/processed/')
    parser.add_argument("--out_dir", type=str, help='Output directory', default='../data/java/processed')
    args = parser.parse_args()

    split(args)
    #elif args.fn == 'prepare':
    prepare(args)
