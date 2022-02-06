import os
import json
import random
import argparse
from tqdm import tqdm
from pprint import pprint
from glob import glob
from collections import defaultdict
import sys
sys.path.append("..")
random.seed(1234)

from codegen.preprocessing.lang_processors.java_processor import JavaProcessor
from codegen.preprocessing.lang_processors.python_processor import PythonProcessor

root_folder = "../third_party"
jprocessor = JavaProcessor(root_folder=root_folder)
pyprocessor = PythonProcessor(root_folder=root_folder)

'''
class OneExample:
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
'''

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
    data = []
    for file in glob(files+'*.json'):
        print(file)
        with open(file, 'r') as f:
            temp = json.load(f)
            data.extend(temp)
            
    #data = data[:40] #debug
    #total = len(data)
    #print(len(data))
    
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
                all_data[ex[0]['problem_id']].append(one_ex)
                idx+=1
        except Exception as e:
            print(e)

    for problem in all_data.keys():
        submissions = all_data[problem]
        total = len(submissions)
        num_test = total // 10  # 10% of the total
        num_valid = total // 20  # 5% of the total
        num_train = total - (num_valid + num_test)

        train_examples.extend(submissions[:num_train])
        valid_examples.extend(submissions[num_train:num_train+num_valid])
        test_examples.extend(submissions[num_train+num_valid:])

    #total = len(all_data)
    #num_test = total // 10  # 10% of the total
    #num_valid = total // 20  # 5% of the total
    #num_train = total - (num_valid + num_test)
    
    #train_examples = all_data[:num_train]
    #valid_examples = all_data[num_train:num_train+num_valid]
    #test_examples = all_data[num_train+num_valid:]

    del all_data

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
                
                id_writer.write(ex['id'] + '\n')
                src_writer.write(src+" "+ex['src_verdict'] + '\n')
                tgt_writer.write(tgt + '\n')

    single_prepare('train')
    single_prepare('valid')
    single_prepare('test')


if __name__ == '__main__':
    #need to tokenize here
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", type=str, nargs='+', help='Language', default='java')
    parser.add_argument("--src_file", type=str, nargs='+', help='Source file', default='../data/java/jsons/')
    parser.add_argument("--src_dir", type=str, help='Source directory', default='../data/java/processed/')
    parser.add_argument("--out_dir", type=str, help='Output directory', default='../data/java/processed')
    
    #parser.add_argument("--fn", type=str, choices=['split', 'prepare'], help='Name of the function')
    #parser.add_argument("--k", type=int, default=5, help='Number of submissions to consider for train split')
    
    args = parser.parse_args()

    #if args.fn == 'split':
    split(args)
    #elif args.fn == 'prepare':
    prepare(args)
