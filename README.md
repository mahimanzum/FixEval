readme added new

# Download project Codenet
## Whole dataset
wget https://dax-cdn.cdn.appdomain.cloud/dax-project-codenet/1.0.0/Project_CodeNet.tar.gz?_ga=2.133483278.1486692882.1645896851-1137262026.1645896851

## Codenet Metadata
wget https://dax-cdn.cdn.appdomain.cloud/dax-project-codenet/1.0.0/Project_CodeNet_metadata.tar.gz?_ga=2.191718442.1486692882.1645896851-1137262026.1645896851

# folder structure (Need to edit)
```
├── README.md 
├── third_party 
├── codet5
│   ├── run.sh 
│   ├── configs.py
│   └── models.py
├── data
│   ├── java
│   │    ├──jsons
│   │    ├──processed
│   ├── Python
│   │    ├──jsons
│   │    ├──processed
│   ├── atcoder_test_cases
│   └── processed.json
│   
│
├── evaluation
│   ├── CodeBLEU 
│   ├── codegen 
│   └── execution_evaluation_TC.py
└── src
    ├── make_submission_list_json.py
    ├── process_json.py
    └── split.py
```
# Additional Downloads (Incomplete link)
Need to download the data folder in the parent directory
Download the atcoder test cases folder in the src or evaluation directory and change the code. (Change needed in split.py and execution_evaluation_TC.py)

## download all the test cases of atcoder 
```
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1AInTHzaZqym7WsT1B7yc8nZy7dA3ovPf' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1AInTHzaZqym7WsT1B7yc8nZy7dA3ovPf" -O atcoder_test_cases.zip && rm -rf /tmp/cookies.txt
```
move this zip file to the data folder and extract there (unzip atcoder_test_cases.zip)



# Environment creation  information
Best way is 
```
bash install_env.sh
```

Another way will be : 
```

conda env create -n python -f src/environment.yml
conda activate python36
```

# creating preprocessed json
make_submission_list_json.py parses problem submission informations, problem list csv, and the actual submission files folder to create an initial json processed.json which is a format like this.

processed is a dictionary containing a list of user_id's containing information about each user processed.keys(). <br>
processed['user_id'] is a list containing a list of problem_id's solved by that user. <br>
processed['user_id']['problem_id'] contains list of tuples. Each tuple consists of information about a submission (submission_id,date,language,original_language,filename_ext,status) <br>


to create this(May need to change the path informations):
```
cd src
python make_submission_list_json.py
```

# creating training data
We use the 'processed.json' file to create the training data chunk by chunk(10k per file) and stores them in the data folder in individual language folders. 
```
cd src
python process_json.py
```
# splitting the data
split.py merges all the chunks, deduplicates using jaccard similarity function and splits the data in train-test-valid(80-10-10) ratio mantaining the condition that for all the datapoints in valid and test set we have the test cases so that execution based evaluation can be done. 
```
cd src
python split.py 
python split.py --lang py --src_file ../data/Python/jsons/ --src_dir ../data/Python/processed/ --out_dir ../data/Python/processed/
```

# training the model and evaluating on the data
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
