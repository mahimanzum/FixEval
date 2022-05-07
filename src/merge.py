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
import os
from joblib import Parallel, delayed
from subprocess import TimeoutExpired
import threading

def getJsonData(JsonFile):
    with open(JsonFile, encoding="utf8") as f:
        data = json.load(f)
    return data

def main(args):

    data = getJsonData(args.references)
    print(data[0].keys())
    root_folder = "../third_party"
    jprocessor = JavaProcessor(root_folder=root_folder)
    pyprocessor = PythonProcessor(root_folder=root_folder)
    
    processor = jprocessor if args.language == 'java' else pyprocessor
    new_data = []
    for idx, dt in enumerate(tqdm(data)):
        one_data = dt.copy()
        one_data['detokenized_tgt'] = processor.detokenize_code(dt['tgt'])
        one_data['detokenized_src'] = processor.detokenize_code(dt['src'])
        #one_data['output'] = output_programs[idx]
        
        temp_detok = []
        for generation in dt['generations']:
            temp_detok.append(processor.detokenize_code(generation))
        one_data['detokenized_generations'] = temp_detok
        new_data.append(one_data)
    
    with open('test_python2python_with_verdict_output.jsonl', 'w', encoding='utf8') as fw:
        json.dump(new_data, fw)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--references', help="filename of the labels, in jsonl format.")
    
    parser.add_argument("--language", type=str, required=False, help="Name of language")
    #parser.add_argument("--test_cases", type=str, required=True, help="Name of language")
    
    params = parser.parse_args()
    main(params)        
    