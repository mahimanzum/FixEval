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
from collections import Counter

def generate(args):
    root_path = args.src_dir+args.lang+'/'
    destination_path = root_path+ 'processed_with_verdict/' if args.with_verdict else root_path+'processed/'
    test_file_path =  destination_path+'test.jsonl'
    
    test = []
    with open(test_file_path, 'r') as f:
        test = json.load(f)
    lst = [dt['src_verdict'] for dt in test]
    cnt = Counter(lst)
    probabilities = list(cnt.values())
    sm_probs = sum(probabilities)
    for i in range(len(probabilities)):
        probabilities[i]/=sm_probs
    
    verdicts = list(cnt.keys())

    idx_map = {}
    for val in verdicts:
        idx_map[val] = []
    
    for idx in range(len(test)):
        idx_map[test[idx]['src_verdict']].append(idx)

    eval_indexes = []
    while len(eval_indexes)!=500:
        while True:
            random_verdict = random.choices(population=verdicts,weights=probabilities,k=1)[0]
            #print(random_verdict)
            #print(idx_map[random_verdict])
            
            rand_idx = random.choice(idx_map[random_verdict])
            if rand_idx not in eval_indexes:
                eval_indexes.append(rand_idx)
                break

    eval_data = []
    for idx in eval_indexes:
        eval_data.append(test[idx])
    
    with open(os.path.join(destination_path, 'eval.jsonl'), 'w', encoding='utf8') as fw:
        json.dump(eval_data, fw)
    
    def single_prepare(split):
        file_prefix = '{}.{}-{}'.format(split, args.lang,args.lang)
        id_file = os.path.join(destination_path, '{}.id'.format(file_prefix))
        src_file = os.path.join(destination_path, 'src_{}.{}'.format(file_prefix, args.lang))
        tgt_file = os.path.join(destination_path, 'tgt_{}.{}'.format(file_prefix, args.lang))

        with open(id_file, 'w', encoding='utf8') as id_writer, \
            open(src_file, 'w', encoding='utf8') as src_writer, \
            open(tgt_file, 'w', encoding='utf8') as tgt_writer, \
            open(os.path.join(destination_path, '{}.jsonl'.format(split))) as f:

            data = json.load(f)

            for ex in tqdm(data):
                
                src = " ".join(ex['src'])
                tgt = " ".join(ex['tgt'])
                id_writer.write(ex['src_id']+"_"+ex['tgt_id'] + '\n')
                
                if args.with_verdict==True:
                    src_writer.write(src+" verdict: "+ex['src_verdict'] + '\n')
                else:
                    src_writer.write(src + '\n')
                
                tgt_writer.write(tgt + '\n')
            
    single_prepare('eval')

def prepare_again(args):
    root_path = args.src_dir+args.lang+'/'
    destination_path = root_path+'processed/'
    test_file_path =  root_path+ 'processed_with_verdict/eval.jsonl'
    
    data = []
    with open(test_file_path, 'r') as f:
        data = json.load(f)
    
    split = 'eval'

    file_prefix = '{}.{}-{}'.format(split, args.lang,args.lang)
    id_file = os.path.join(destination_path, '{}.id'.format(file_prefix))
    src_file = os.path.join(destination_path, 'src_{}.{}'.format(file_prefix, args.lang))
    tgt_file = os.path.join(destination_path, 'tgt_{}.{}'.format(file_prefix, args.lang))

    with open(id_file, 'w', encoding='utf8') as id_writer, \
        open(src_file, 'w', encoding='utf8') as src_writer, \
        open(tgt_file, 'w', encoding='utf8') as tgt_writer:

        for ex in tqdm(data):
            
            src = " ".join(ex['src'])
            tgt = " ".join(ex['tgt'])
            id_writer.write(ex['src_id']+"_"+ex['tgt_id'] + '\n')
            src_writer.write(src + '\n')
            
            tgt_writer.write(tgt + '\n')


if __name__ == '__main__':
    
    # lang either java or python
    # default java
    # python command to run: python split.py --lang python --src_file ../data/python/jsons/ --src_dir ../data/python/processed_with_verdict/ --out_dir ../data/python/processed_with_verdict/ --test_cases ../data/atcoder_test_cases --with_verdict yes
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", type=str, help='Language', default='java')

    parser.add_argument("--src_dir", type=str, help='Source directory', default='../data/') #processed_with_verdict
    parser.add_argument("--with_verdict", type=bool, help="Name of language",default=False)
    
    args = parser.parse_args()
    prepare_again(args)
    generate(args)