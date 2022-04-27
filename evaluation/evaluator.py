# Copyright (c) Microsoft Corporation. 
# Licensed under the MIT license.

import sys
sys.path.append(".")
sys.path.append("..")
#sys.path.append("../src")
from tqdm import tqdm
import json
import argparse
from evaluation.bleu import compute_bleu
from src.codegen.preprocessing.lang_processors.java_processor import JavaProcessor
from src.codegen.preprocessing.lang_processors.python_processor import PythonProcessor

root_folder = "../third_party"
jprocessor = JavaProcessor(root_folder=root_folder)
pyprocessor = PythonProcessor(root_folder=root_folder)


def main():
    parser = argparse.ArgumentParser(description='Evaluate leaderboard predictions for BigCloneBench dataset.')
    parser.add_argument('--references', help="filename of the labels, in jsonl format.")
    parser.add_argument('--txt_ref', action='store_true', help='reference file is a txt file')
    parser.add_argument('--predictions', help="filename of the leaderboard predictions, in txt format.")
    parser.add_argument('--language', help="language name evaluating on.")
    parser.add_argument('--detokenize_refs', action='store_true', help="perform detokenization before evaluating.")
    parser.add_argument('--detokenize_preds', action='store_true', help="perform detokenization before evaluating.")
    args = parser.parse_args()

    references = []

    with open(args.references, 'r', encoding='utf-8') as f:
        data = json.load(f)
        #refs = [x['tgt'].strip() for x in data]
        for line in tqdm(data):
            #print(line['tgt'])
            refs = [line['tgt']] # change here for tokenization detokenization
            if args.detokenize_refs:
                if args.language == 'python':
                    #refs = [pyprocessor.detokenize_code(r) for r in refs]
                    refs = [r for r in refs]
                elif args.language == 'java':
                    #refs = [jprocessor.detokenize_code(r) for r in refs]
                    refs = [r for r in refs]
            references.append([r for r in refs]) ## need to visualize referances I am suspecting it's all charecters
    

    translations = []
    with open(args.predictions, 'r', encoding='utf-8') as fh:
        for line in tqdm(fh):
            line = line.strip()
            if args.detokenize_preds:
                if args.language == 'python':
                    #line = [pyprocessor.detokenize_code(r) for r in refs]
                    line = [r for r in refs]
                elif args.language == 'java':
                    line = [jprocessor.detokenize_code(r) for r in refs]
            translations.append(line.split())

    assert len(references) == len(translations)

    #print(references[:5])
    #print('#####################')
    #print(translations[:5])
    count = 0
    for i in range(len(references)):
        refs = references[i]  # r is a list of 'list of tokens'
        t = translations[i]  # 'list of tokens'
        for r in refs:
            if r == t:
                count += 1
                break
    acc = round(count / len(translations) * 100, 2)
    print("inside function")
    bleu_score, _, _, _, _, _ = compute_bleu(references, translations, 4, True)
    bleu_score = round(100 * bleu_score, 2)

    print('BLEU:\t\t%.2f\nExact Match:\t\t%.2f' % (bleu_score, acc))


if __name__ == '__main__':
    main()
