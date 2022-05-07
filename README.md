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
### Download Project Codenet Dataset
Run this command to download the whole codenet dataset(Around 8GB zipped file) in the root directory and decompress it.
```
wget https://dax-cdn.cdn.appdomain.cloud/dax-project-codenet/1.0.0/Project_CodeNet.tar.gz?_ga=2.133483278.1486692882.1645896851-1137262026.1645896851
tar -xf Project_CodeNet.tar.gz
```
### Codenet Metadata
Run this command to download codenet Metadata (281Mb zip file) in the root directory and decompress it
```
wget https://dax-cdn.cdn.appdomain.cloud/dax-project-codenet/1.0.0/Project_CodeNet_metadata.tar.gz?_ga=2.191718442.1486692882.1645896851-1137262026.1645896851
tar -xf Project_CodeNet_metadata.tar.gz
```


### Download Test Cases 
Make the data folder to store the test cases, along with java , python data files.
```
mkdir data
cd data
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1AInTHzaZqym7WsT1B7yc8nZy7dA3ovPf' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1AInTHzaZqym7WsT1B7yc8nZy7dA3ovPf" -O atcoder_test_cases.zip && rm -rf /tmp/cookies.txt
unzip atcoder_test_cases.zip
cd ../
```

### Environment Creation
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

### Create Pre-processed File 
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

#### Split The Data
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
cd data
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1vsuUrJ2j86EYGb2WWQatqsqJ-V8Sl6en' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1vsuUrJ2j86EYGb2WWQatqsqJ-V8Sl6en" -O java.zip && rm -rf /tmp/cookies.txt
unzip java.zip
cd ../
```
#### Download and unzip python dataset 
```
cd data
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1rjjYW8SB8f5Hr34ig84OKpNYOzdt03Ar' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1rjjYW8SB8f5Hr34ig84OKpNYOzdt03Ar" -O python.zip && rm -rf /tmp/cookies.txt
unzip python.zip
cd ../
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


### Training the model and evaluating on the dataset
To run the codet5 model go to that folder and use run.sh. This will also evalualte the model on execution_evaluation, BLEU, CodeBleu, Syntax match dataflow match all at the same time.
some changes are required in run.sh. <br>
Change source and target languages online 14-15-> from these ['java', 'python'] <br>
Change path_2_data line 22 at the end folder name as 'processed' or processed_with_verdict <br>
Change Line 27 , Model and Cached data save directory to be consistent with the data as well. Append "_with_verdict" if associated data path contains "_with_verdict" as well. <br>
To just evaluate comment the train function in the bottom of the run.sh file
```
cd codet5/
nohup ./run.sh
```

Similarly for training and evaluating plbart model go to the root directory and run these.

```
cd plbart/
nohup ./run.sh
```

### Evaluate on Execution 
This will take the test.json file in each of the data generate 
```
cd src/
python generate_eval_files.py 
python generate_eval_files.py --with_verdict True
python generate_eval_files.py --lang python
python generate_eval_files.py --with_verdict True --lang python
cd ../
```
These commands will create additional 4 files in the 4 core data folders in data/language/{processed, processed_with_verdict} named eval.
The main difference between eval and test set is that {train, test, valid} are created using our split method and all the datapoints ar split between these. <br>
But eval files are sampled from the test datapoints using generate_eval_files.py keeping the true data distribution similar to the test file but smaller(500 in our case) just to make the runtime and computational complexity in check as we need to generate multiple submissions and run each of them in many test cases to calculate our pass@k accuracy.

#### First lets generate the test file
This 
#### Now lets generate the predictions on the test file


#### pre-preprocess the test file that contains all tokenized and detokenized source , target and prediction on all beam size
First We need to create a self contrained json containing all the necessary versions to detokenize the code and execute. 

This part is not included in the usual evaluation because changes are requires based on system to run this efficiently.
First we expect the test cases folder and the problem_list.csv file is in the root directory so lets copy those. 

```
cd plbart/
nohup ./run.sh
```

#### Finally lets run the code to execute and evaluate
python execution_evaluation_TC.py --input ../data/Python/processed/test.jsonl --lang py --test_cases ../src/atcoder_test_cases

#### use results.py to get the results 
pass@k
