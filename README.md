### All data for reproducing the results is available Here:
```
https://drive.google.com/drive/folders/1dzuHuouuWzlFCy1CMj9DYG9JGraEay27?usp=sharing
```

<table>
    <thead>
        <tr>
            <th>Method</th>
            <th>Verdict</th>
            <th>BLEU</th>
            <th>EM</th>
            <th>SM</th>
            <th>DM</th>
            <th>CB</th>
            <th>CA</th>
        </tr>
    </thead>

</table>

### Folder Structure 
```
├── README.md 
├── third_party 
├── codet5
│   ├── run.sh 
│   ├── configs.py
│   ├── models.py
│   └── run_gen.py
├── plbart
│   ├── run.sh 
│   ├── configs.py
│   ├── models.py
│   └── run_gen.py
├── data
│   ├── java
│   │    ├──jsons
│   │    ├──processed
│   ├── Python
│   │    ├──jsons
│   │    ├──processed
│   ├── atcoder_test_cases
│   └── processed.json
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
│   └── execution_evaluation_TC_arc_MP.py
└── src
    ├── make_submission_list_json.py
    ├── process_json.py
    ├── deduplication.py
    ├── generate_eval_files.py
    ├── merge.py
    └── split.py
```
## Run all these commands into the root folder
## Downloading Portions
### Download Project Codenet Dataset (Skip this if you want to run from our preprocessed files)
Run this command to download the whole codenet dataset(Around 8GB zipped file) in the root directory and decompress it.
```
wget https://dax-cdn.cdn.appdomain.cloud/dax-project-codenet/1.0.0/Project_CodeNet.tar.gz
tar -xf Project_CodeNet.tar.gz
```
### Codenet Metadata
Run this command to download codenet Metadata (281Mb zip file) in the root directory and decompress it
```
wget https://dax-cdn.cdn.appdomain.cloud/dax-project-codenet/1.0.0/Project_CodeNet_metadata.tar.gz
tar -xf Project_CodeNet_metadata.tar.gz
```


### Download Test Cases 
Make the data folder to store the test cases, along with java , python data files.
```
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1AInTHzaZqym7WsT1B7yc8nZy7dA3ovPf' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1AInTHzaZqym7WsT1B7yc8nZy7dA3ovPf" -O atcoder_test_cases.zip && rm -rf /tmp/cookies.txt
unzip atcoder_test_cases.zip
cd ../
```
## Installation Portion

Best way is to run this command(You may need to change the bash file to change your preferance on environment names etc.)
```
bash install_env.sh
```

Another way will be( You may need to manually add some libraries): 
```
conda env create -n python -f src/environment.yml
conda activate python36
```
All the commands below assumes that you installed everything on this environment correctly and activate the environment. 

### Create Pre-processed File (Skip this if you want to run from our preprocessed files)
src/make_submission_list_json.py parses problem submission informations, problem list csv, and the actual submission files folder to create an initial json processed.json which is a format like this.

processed is a dictionary containing a list of user_id's containing information about each user processed.keys(). <br>
processed['user_id'] is a list containing a list of problem_id's solved by that user. <br>
processed['user_id']['problem_id'] contains list of tuples. Each tuple consists of information about a submission (submission_id,date,language,original_language,filename_ext,status) <br>


to create this(May need to change the path informations):
```
cd src
python make_submission_list_json.py
cd ../
```

### Create Language Specific Data (Skip this part if you just want to download our version)
We use the 'processed.json' file to create the training data chunk by chunk(10k per file) and store them in the data folder in individual language folders. The same code preprocesses and stores both java and python data in json format in folders named data/{language}/jsons/.
```
cd src
python process_json.py
cd ../
```
Or you can also download "processed.json" file which is kind of the root file for all data generation and processing. 
```
cd data/
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1gxZYObARqJytI9gf6gEX-CZhCpc4JPE6' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1gxZYObARqJytI9gf6gEX-CZhCpc4JPE6" -O processed.zip && rm -rf /tmp/cookies.txt
unzip processed.zip
cd ../
```

#### Split The Data (Skip this if you want to run from our preprocessed files)
split.py merges all the json chunks, deduplicates using jaccard similarity function and splits the data in train-valid-test (80-10-10) ratio on problem level so that no datapoints for a single problem exists in multiple splits like train and test. During the split We also mantaining the condition that for all the datapoints in valid and test set we have the test cases available so that execution based evaluation can be done in both valid and test set. 
```
cd src
python split.py 
python split.py --lang py --src_file ../data/Python/jsons/ --src_dir ../data/Python/processed/ --out_dir ../data/Python/processed/
cd ../
```

### Run these commands if you just want to download the processed data and train
#### Download and unzip java dataset 
```
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1vsuUrJ2j86EYGb2WWQatqsqJ-V8Sl6en' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1vsuUrJ2j86EYGb2WWQatqsqJ-V8Sl6en" -O java.zip && rm -rf /tmp/cookies.txt
unzip java.zip
```
#### Download and unzip python dataset 
```
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1rjjYW8SB8f5Hr34ig84OKpNYOzdt03Ar' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1rjjYW8SB8f5Hr34ig84OKpNYOzdt03Ar" -O python.zip && rm -rf /tmp/cookies.txt
unzip python.zip
```
After successfull completion till this part we have 4 datasets.  <br>
java buggy to java fixed in, (data/java/processed/) <br>
java buggy with verdict information to java fixed in (data/java/processed_with_verdict/)<br>
python buggy code to python fixed code in (data/python/processed/)<br>
python buggy code with verdict information to python fixed code in (data/python/processed_with_verdict/)<br>

All of these 4 folders contain {train, test, eval}.jsonl file containing all the information for the datapoints so the we can always reverse back to the original data <br>
contains {train, valid, test}.{language-language}.id files where language is [java, python] <br>
Also contains 6 raw test files for training.  <br>
{src, tgt}_{train, valid, test}.{language-language}.language

## Training and Evaluation Portion

### Training the model and evaluating on the dataset
To run the codet5 model go to that folder and use run.sh. This will also evalualte the model on execution_evaluation, BLEU, CodeBleu, Syntax match dataflow match all at the same time.
some changes are required in run.sh. <br>
Change source and target languages online 14-15-> from these ['java', 'python'] <br>
Change path_2_data line 22 at the end folder name as 'processed' or processed_with_verdict <br>
Change Line 27 , Model and Cached data save directory to be consistent with the data as well. Append "_with_verdict" if associated data path contains "_with_verdict" as well. <br>
To just evaluate comment the train function in the bottom of the run.sh file

Each run.sh files have similar structure

```
./run.sh GPU_ID SRC_LANGUAGE TARGET_LANGUAGE DATA_SOURCE WITH_VERDICT
```

GPU_ID is basically how many gpus you want to use for single GPU it's usually "0". <br>
SRC_LANGUAGE, TARGET_LANGUAGE both are usually same for a single run. Both can be either "java" or "python"
DATA_SOURCE is "codenet" because stored the preprocessed datra named "codenet". It can be anything
WITH_VERDICT can be either "true" or "false" which means if we want to use the verdict information in the input or not.
```
cd codet5/
nohup ./run.sh 0 java java codenet false
nohup ./run.sh 0 java java codenet true
nohup ./run.sh 0 python python codenet false
nohup ./run.sh 0 python python codenet true
```

Similarly for training and evaluating plbart model go to the root directory and run these.

```
cd plbart/
nohup ./run.sh 0 java java codenet false
nohup ./run.sh 0 java java codenet true
nohup ./run.sh 0 python python codenet false
nohup ./run.sh 0 python python codenet true
```
The run.sh for each of the model folders contain 3 function. <br>
train -> Trains that specific model and saves the checkpoints and logs all the necessary matrices
evaluate -> loades a pretrained model (usually the checkpoint-best-ppl) model and Evaluates all the usual matrices except the execution based evaluation with pass@k accuracy. <br>
generate -> Loads a pretrained model (usually the checkpoint-best-ppl) and generates a json file with the predictions from the loaded model.

## Evaluation
### Evaluate on Execution 
This part is not included in the usual evaluation because changes are requires based on system to run this efficiently. <br>

First run these commands. These commands will create additional 4 splits in the 4 core data folders in data/language/{processed, processed_with_verdict} named eval which similar to train , valid and test but smaller.
The main difference between eval and test set is that {train, test, valid} are created using our split method and all the datapoints ar split between these. <br>
But here we create eval split which is sampled from the test datapoints using generate_eval_files.py keeping the true data distribution similar to the test file but smaller(500 in our case) just to make the runtime and computational complexity in check as we need to generate multiple submissions and run each of them in many test cases to calculate our pass@k accuracy.

```
cd src/
python generate_eval_files.py 
python generate_eval_files.py --with_verdict True
python generate_eval_files.py --lang python
python generate_eval_files.py --with_verdict True --lang python
cd ../
```

#### First lets generate the test file
Just go to that specific model folder and execute the run.sh command with only generate function uncommented and save_dir, path_2_data, and languages set to the correct versions. for example
```
cd plbart/
./run.sh
```

#### pre-preprocess the test file that contains all tokenized and detokenized source , target and prediction on all beam size

First We need to create a self contrained json containing all the necessary versions to detokenize the code and execute. We split this portion explicitly because we use ARC(Advanced Research Computing), Virginia Tech for parallel running of these code and installing all the libraries required to tokenize java and python codes is not possible in the ARC supercomputer. So we do it elsewhere and create this self contained json file which can be used to generate results. 

```
cd src/
python merge.py --references data/java/processed/generation.json --language java
python merge.py --references data/java/processed_with_verdict/generation.json --language java
python merge.py --references data/python/processed/generation.json --language python
python merge.py --references data/python/processed_with_verdict/generation.json --language python
cd ../
```
These will create 4 json files. You might need to change the output file names just for clarification.

#### Finally lets run the code to execute and evaluate
First we expect the "test cases folder" and the "problem_list.csv" file is in the root directory so lets copy those. <br>

```
cp -r data/atcoder_test_cases atcoder_test_cases
cp Project_CodeNet/metadata/problem_list.csv problem_list.csv 
```
Now lets run the Execute and evaluate method
```
python evaluation/execution_evaluation_TC_arc_MP.py --references test_python2python_with_verdict_output.jsonl --language python --test_cases atcoder_test_cases --problem_list problem_list.csv
```
To run on arc We provide a file for using in slurm clusters where you might need to change some credectials.
```
sbatch batch_run.sh
```
Any of the previous commands will create a json file which will contain all the fields necessary for visualizing and getting pass@k accuracy.
#### use results.py to get the results 
We can use results.py to generate the results
We can also use the previous json in the src/01_preprocessing.ipynb notebook for visualizing.