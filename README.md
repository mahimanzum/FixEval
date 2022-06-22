### Official Code for [FixEval: Execution-based Evaluation of Program Fixes for Competitive Programming Problems](https://arxiv.org/abs/2206.07796)
#### Abstract: 
Source code repositories consist of large codebases, often containing error-prone programs. The increasing complexity of software has led to a drastic rise in time and costs for identifying and fixing these defects. Various methods exist to automatically generate fixes for buggy code. However, due to the large combinatorial space of possible solutions for a particular bug, there are not many tools and datasets available to evaluate generated code effectively. In this work, we introduce FixEval, a benchmark comprising buggy code submissions to competitive programming problems and their respective fixes. We introduce a richtest suite to evaluate and assess the correctness of model-generated program fixes. We consider two Transformer language models pretrained on programming languages as our baselines, and compare them using match-based and execution-based evaluation metrics. Our experiments show that match-based metrics do not reflect model-generated program fixes accurately, while execution-based methods evaluate programs through all cases and scenarios specifically designed for that solution. Therefore, we believe FixEval provides a step towards real-world automatic bug fixing and model-generated code evaluation.

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Folder Structure](#folder-structure)
- [Dataset](#dataset)
    - [Download CodeNet Metadata](#download-codenet-metadata)
    - [Download Test Cases](#download-test-cases)
- [Installation](#installation)
- [Pre-processing ](#pre-processing-skip-this-if-you-want-to-run-from-our-preprocessed-files)
    - [Split The Data](#split-the-data-skip-this-if-you-want-to-continue-from-our-preprocessed-files)
- [Download Preprocessed Data](#download-preprocessed-data)
    - [Download our preprocessed Java dataset](#download-and-unzip-our-preprocessed-java-dataset)
    - [Download our preprocessed Python dataset](#download-and-unzip-our-preprocessed-python-dataset)
- [Training and Evaluation](#training-and-evaluation)
    - [Training](#training-the-model-and-evaluating-on-the-dataset)
    - [Evaluation](#evaluation)
    - [Evaluate on Execution](#evaluate-on-execution)
- [Benchmarks](#benchmarks)
    - [Match-based metrics](#match-based-metrics)
    - [Execution-based metrics](#execution-based-metrics)
- [License](#license)
- [Citation](#citation)

## Folder Structure 
```

├── codet5
│   ├── run.sh 
│   ├── configs.py
│   ├── models.py
│   ├── run_gen.py
│   └── ...
│ 
├── plbart
│   ├── run.sh 
│   ├── configs.py
│   ├── models.py
│   ├── run_gen.py
│   └── ...
│
├── data
│   ├── java
│   │    ├──jsons
│   │    ├──processed
│   ├── python
│   │    ├──jsons
│   │    ├──processed
│   ├── atcoder_test_cases
│   └── processed.json
│
├── third_party
│   ├── apex
│   ├── fairseq
│   ├── tree-sitter-cpp
│   ├── tree-sitter-java
│   └── tree-sitter-python
│
├── evaluation
│   ├── CodeBLEU 
│   ├── codegen 
│   ├── bleu.py
│   ├── compile.py
│   ├── compute_ca.py
│   ├── evaluator.py
│   ├── execution_evaluation_TC_arc_MP.py
│   └── ...
│
└── src
    ├── 01_preprocessing.ipynb
    ├── make_submission_list_json.py
    ├── process_json.py
    ├── deduplication.py
    ├── generate_eval_files.py
    ├── merge.py
    ├── split.py
    └── ...
```

## Dataset
All data for reproducing the results is available here:
```
https://drive.google.com/drive/folders/1dzuHuouuWzlFCy1CMj9DYG9JGraEay27?usp=sharing
```

Run the following commands in the root folder.

#### Download Project CodeNet Dataset (Skip this if you want to run from our preprocessed files)
Run this command to download the whole CodeNet dataset (around 8GB zip file) in the root directory and decompress it.
```
wget https://dax-cdn.cdn.appdomain.cloud/dax-project-codenet/1.0.0/Project_CodeNet.tar.gz
tar -xf Project_CodeNet.tar.gz
```
#### Download CodeNet Metadata
Run this command to download the CodeNet metadata (281Mb zip file) in the root directory and decompress it
```
wget https://dax-cdn.cdn.appdomain.cloud/dax-project-codenet/1.0.0/Project_CodeNet_metadata.tar.gz
tar -xf Project_CodeNet_metadata.tar.gz
```


#### Download Test Cases 
Make the data folder to store the test cases along with the Java and Python data files.
```
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1AInTHzaZqym7WsT1B7yc8nZy7dA3ovPf' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1AInTHzaZqym7WsT1B7yc8nZy7dA3ovPf" -O atcoder_test_cases.zip && rm -rf /tmp/cookies.txt
unzip atcoder_test_cases.zip
cd ../
```

## Installation

The preferred installation method is to run this command (You may need to change the bash file to update the environment names, etc.):
```
bash install_env.sh
```

Another method is to run the following (You may need to manually add some libraries): 
```
conda env create -n python -f src/environment.yml
conda activate python36
```
All the commands below assume that you installed everything in this environment correctly and activated the environment. 

## Pre-processing (Skip this if you want to run from our preprocessed files)
`src/make_submission_list_json.py` parses problem submission information, problem list csv, and the actual submission files folder to create an initial json, `processed.json`, which uses the following format:

`processed` is a dictionary containing a list of user_id's with information about each user in `processed.keys()`. <br>
`processed['user_id']` is a list containing a list of problem_id's solved by that user. <br>
`processed['user_id']['problem_id']` contains list of tuples. Each tuple consists of information about a submission (submission_id,date,language,original_language,filename_ext,status) <br>


To create this, use the followint script (You may need to change the path information):
```
cd src
python make_submission_list_json.py
cd ../
```

#### Create Language Specific Data (Skip this part if you just want to download our version)
We use the `processed.json` file to create the training data chunk by chunk (10k per file) and store them in the data folder for individual programming languages. The following code preprocesses and stores both Java and Python data into the json format in folders stored at `data/{language}/jsons/`.
```
cd src
python process_json.py
cd ../
```

Or, you can also download the `processed.json` file, which is the root file for all data generation and processing: 
```
cd data/
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1gxZYObARqJytI9gf6gEX-CZhCpc4JPE6' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1gxZYObARqJytI9gf6gEX-CZhCpc4JPE6" -O processed.zip && rm -rf /tmp/cookies.txt
unzip processed.zip
cd ../
```

#### Split The Data (Skip this if you want to continue from our preprocessed files)
`split.py` merges all the json chunks, deduplicates using jaccard similarity function, and splits the data into the train-valid-test (80-10-10) ratio. This is done on the problem level so that no datapoints for a single problem exist in multiple splits, like train and test. During the split, we also mantain the condition that for all the datapoints in the valid and test sets- we have the test cases available so that execution-based evaluation can be done on both the valid and test set data. 
```
cd src
python split.py 
python split.py --lang py --src_file ../data/Python/jsons/ --src_dir ../data/Python/processed/ --out_dir ../data/Python/processed/
cd ../
```

## Download Preprocessed Data 
Run the following commands if you want to download the processed data and train:

#### Download and unzip our preprocessed Java dataset 
```
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1vsuUrJ2j86EYGb2WWQatqsqJ-V8Sl6en' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1vsuUrJ2j86EYGb2WWQatqsqJ-V8Sl6en" -O java.zip && rm -rf /tmp/cookies.txt
unzip java.zip
```
#### Download and unzip our preprocessed Python dataset 
```
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1rjjYW8SB8f5Hr34ig84OKpNYOzdt03Ar' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1rjjYW8SB8f5Hr34ig84OKpNYOzdt03Ar" -O python.zip && rm -rf /tmp/cookies.txt
unzip python.zip
```
After successful completion, we derive 4 datasets from this part:  <br>
* java buggy code to java fixed code (`data/java/processed/`) <br>
* java buggy code with verdict information to java fixed code (`data/java/processed_with_verdict/`)<br>
* python buggy code to python fixed code (`data/python/processed/`)<br>
* python buggy code with verdict information to python fixed code in (`data/python/processed_with_verdict/`)<br>

Each of these 4 directories contains:
* `{train, test, eval}.jsonl` files containing all the information for the datapoints. This also allows us to always revert back to the original dataset <br>
* `{train, valid, test}.{language-language}.id` files, where language is in the set [java, python] <br>
* 6 raw test files for training.  <br>
* `{src, tgt}_{train, valid, test}.{language-language}.language`

## Training and Evaluation

#### Training the model and evaluating on the dataset
To run the codet5 model, go to the `codet5` folder and use the `run.sh` script file. This will also evalualte the model on match-based metrics (BLEU, CodeBleu, Syntax Match, Dataflow Match, etc.).
Some changes are required to execute the `run.sh` script: <br>
* Change the source and target languages on lines 14-15 to one of these ['java', 'python'] <br>
* Change `path_2_data` at the end of line 22 to the folder name with the processed or processed_with_verdict data <br>
* Change line 27 to make the Model and Cached data save directory consistent with the data as well. For example, append "\_with_verdict" if the associated data path contains "\_with_verdict" as well. <br>
To simply run the evaluation, comment out the train function in the bottom of the `run.sh` file <br>

Each `run.sh` file has a similar structure:

```
./run.sh GPU_ID SRC_LANGUAGE TARGET_LANGUAGE DATA_SOURCE WITH_VERDICT
```

`GPU_ID` is how many GPUs you want to use. For single GPU, input "0". <br>
`SRC_LANGUAGE`, `TARGET_LANGUAGE` are both the same for a single run. They can be either "java" or "python".<br>
`DATA_SOURCE` is the location of the preprocessed data. For example, "`codenet`" if the stored preprocessed data folder is named "codenet".<br>
`WITH_VERDICT` can be either "true" or "false" depending on if you want to use the verdict information in the input or not.
```
cd codet5/
nohup ./run.sh 0 java java codenet false #TODO Briefly explain one or all of these examples i.e.:
nohup ./run.sh 0 java java codenet true #Executes the Java dataset with one GPU and verdict information
nohup ./run.sh 0 python python codenet false #Executes the Python dataset with one GPU and without verdict information
nohup ./run.sh 0 python python codenet true
```

Similarly, for training and evaluating the plbart model, navigate to the root directory and use the following:

```
cd plbart/
nohup ./run.sh 0 java java codenet false
nohup ./run.sh 0 java java codenet true
nohup ./run.sh 0 python python codenet false
nohup ./run.sh 0 python python codenet true
```
The `run.sh` script for each of the models contains 3 function: <br>
* `train` -> Trains that specific model and saves the checkpoints and logs all the necessary matrices. <br>
* `evaluate` -> Loads a pretrained model (usually the checkpoint-best-ppl) model and evaluates all metrics except the execution-based evaluation with pass@k accuracy. <br>
* `generate` -> Loads a pretrained model (usually the checkpoint-best-ppl) and generates a json file with the predictions from the loaded model.

## Evaluation
#### Evaluate on Execution 
This part is not included in the usual evaluation because changes are required based on your system to run this efficiently. <br>

First, run the below commands. These commands will create 4 additional splits in the 4 core data folders (`data/language/{processed, processed_with_verdict}`) named `eval` which are similar to `train`, `valid`, and `test` but smaller.
The main difference between eval and test set is that `{train, test, valid}` are created using our split method and all the datapoints are split between these. <br>
But here we create an eval split which is sampled from the test datapoints using `generate_eval_files.py`, keeping the true data distribution similar to the test file but on a smaller scale (500 in our case) to keep the runtime and computational complexity in check as we need to generate multiple submissions and run each of them with many test cases to calculate our pass@k accuracy.

```
cd src/
python generate_eval_files.py 
python generate_eval_files.py --with_verdict True
python generate_eval_files.py --lang python
python generate_eval_files.py --with_verdict True --lang python
cd ../
```

#### Let's generate the file with the model predictions
Go to the specific model folder and execute the `run.sh` command with only the `generate` function uncommented and `save_dir`, `path_2_data`, and `languages` set to the correct versions. For example:
```
cd plbart/
./run.sh
```
To use our open sourced pretrained models, download plbart.zip or codeT5.zip from the link below and verify the results using the same procedure.
```
https://drive.google.com/drive/folders/1dzuHuouuWzlFCy1CMj9DYG9JGraEay27?usp=sharing
```


#### Pre-preprocess the generated files that contains all tokenized and detokenized source, target, and predictions

First, we need to create a self-contained json with all of the necessary versions to detokenize the code and execute. We split this portion explicitly because it is not possible to run the code and install all the libraries required to tokenize the Java and Python programs using the ARC (Advanced Research Computing) supercomputer at Virginia Tech. Thus, we do it elsewhere and create the resulting json file which can be used to generate results. 

```
cd src/
python merge.py --references data/java/processed/generation.json --language java
python merge.py --references data/java/processed_with_verdict/generation.json --language java
python merge.py --references data/python/processed/generation.json --language python
python merge.py --references data/python/processed_with_verdict/generation.json --language python
cd ../
```
These will create 4 json files. You may need to change the output file names for your own clarification.

#### Finally, let's run the code to execute and evaluate
First, we expect the test cases folder and the "`problem_list.csv`" file to be in the root directory. So let's copy those: <br>

```
cp -r data/atcoder_test_cases atcoder_test_cases
cp Project_CodeNet/metadata/problem_list.csv problem_list.csv 
```
Now, let's run the `execute` and `evaluate` methods:
```
python evaluation/execution_evaluation_TC_arc_MP.py --references test_python2python_with_verdict_output.jsonl --language python --test_cases atcoder_test_cases --problem_list problem_list.csv
```
To run on ARC, we provide a file for using in slurm clusters where you might need to change your credentials.
```
sbatch batch_run.sh
```
The previous commands will create a json file which contains all the fields necessary for visualizing and getting pass@k accuracy.

#### Use results.py to get the results 
We can use `results.py` to generate the results.
We can also use the previous json in the `src/01_preprocessing.ipynb` notebook for visualizing.

## Benchmarks


#### Match-based metrics

We evaluate the models' performances on the test set in terms of Compilation Accuracy (CA), BLEU, Syntax Match (SM), Dataflow Match (DM), CodeBLEU (CB), and Exact Match (EM). We report the model performances below.


<table>
    <thead>
        <tr>
            <th>Method</th>
            <th>Language</th>
            <th>Verdict</th>
            <th>BLEU</th>
            <th>EM</th>
            <th>SM</th>
            <th>DM</th>
            <th>CB</th>
            <th>CA</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=2> Naive Copy </td>
            <td> Java</td>
            <td>No</td>
            <td>80.28</td>
            <td>0.03</td>
            <td>84.22</td>
            <td>53.64</td>
            <td>75.43</td>
            <td>89.93</td>
        </tr>
        <tr>
            <td>Python</td>
            <td>No</td>
            <td>68.55</td>
            <td>0.73</td>
            <td>70.12</td>
            <td>60.51</td>
            <td>68.47</td>
            <td>96.56</td>
        </tr>
        <tr>
            <td rowspan=4> PLBART </td>
            <td align ="center", rowspan=2>Java</td>
            <td>No</td>
            <td>58.49</td>
            <td>0.45</td>
            <td>66.92</td>
            <td>43.08</td>
            <td>57.23</td>
            <td>31.36</td>
        </tr>
        <tr>
            <td>Yes</td>     
            <td>59.84</td>
            <td>1.46</td>
            <td>68.01</td>
            <td>44.99</td>
            <td>58.62</td>
            <td>33.04</td>
        </tr>
        <tr>
            <td align ="center", rowspan=2>Python</td>
            <td>No</td> 
            <td>61.89</td>
            <td>2.32</td>
            <td>64.32</td>
            <td>48.81</td>
            <td>61.13</td>
            <td>91.16</td>
        </tr>
        <tr>
            <td>Yes</td>
            <td>62.25</td>
            <td>2.46</td>
            <td>63.31</td>
            <td>49.73</td>
            <td>62.21</td>
            <td>92.21</td>
        </tr>
        <tr>
            <td rowspan=4> CodeT5 </td>
            <td align ="center", rowspan=2>Java</td>
            <td>No</td>
            <td>62.31</td>
            <td>2.96</td>
            <td>74.01</td>
            <td>52.30</td>
            <td>63.37</td>
            <td>63.03</td>
        </tr>
        <tr>
            <td>Yes</td>
            <td>62.54</td>
            <td>2.45</td>
            <td>73.93</td>
            <td>53.29</td>
            <td>63.71</td>
            <td>64.23</td>
        </tr>
        <tr>
            <td align ="center", rowspan=2>Python</td>
            <td>No</td>
            <td>64.92</td>
            <td>2.74</td>
            <td>68.79</td>
            <td>56.21</td>
            <td>63.53</td>
            <td>92.80</td>
        </tr>
        <tr>
            <td>Yes</td>
            <td>64.67</td>
            <td>2.97</td>
            <td>68.45</td>
            <td>56.04</td>
            <td>63.28</td>
            <td>92.70</td>
        </tr>
    </tbody>
</table>


#### Execution-based metrics
We also evaluate our model using pass@k and test case average. Here are the benckmark results: 

<table>
    <thead>
        <tr>
            <th rowspan=2>Language </th>
            <th rowspan=2>Verdict</th>
            <th colspan=4>pass@k</th>
            <th colspan=4>TCA@k</th>
        </tr>
        <tr>
        <td>k = 1</td>
        <td>k = 3</td>
        <td>k = 5</td>
        <td>k = 10</td>
        <td>k = 1</td>
        <td>k = 3</td>
        <td>k = 5</td>
        <td>k = 10</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align ="center", rowspan=2>Java</td>
            <td>No</td>
            <td>8.65</td>
            <td>15.62</td>
            <td>19.63</td>
            <td>24.44</td>
            <td>41.00</td>
            <td>34.00</td>
            <td>32.70</td>
            <td>29.60</td>
        </tr>
        <tr>
            <td>Yes</td> 
            <td>10.94</td>
            <td>18.77</td>
            <td>22.66</td>
            <td>27.96</td>
            <td>44.99</td>
            <td>38.80</td>
            <td>35.87</td>
            <td>32.90</td>
        </tr>
        <tr>
            <td align ="center", rowspan=2>Python</td>
            <td>No</td> 
            <td>6.86</td>
            <td>13.07</td>
            <td>16.27</td>
            <td>20.51</td>
            <td>50.20</td>
            <td>41.20</td>
            <td>38.50</td>
            <td>35.20</td>
        </tr>
        <tr>
            <td>Yes</td> 
            <td>7.32</td>
            <td>13.94</td>
            <td>17.47</td>
            <td>22.63</td>
            <td>58.75</td>
            <td>41.16</td>
            <td>38.37</td>
            <td>34.88</td>
        </tr>
    </tbody>
</table>

## License
MIT License

Copyright (c) 2022 Md. Mahim Anjum Haque

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

## Citation

@article{haque2022fixeval,
  title={FixEval: Execution-based Evaluation of Program Fixes for Competitive Programming Problems},
  author={Haque, Md Mahim Anjum and Ahmad, Wasi Uddin and Lourentzou, Ismini and Brown, Chris},
  journal={arXiv preprint arXiv:2206.07796},
  year={2022}
}
