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
│        ├──jsons
│        ├──processed
├── evaluation
│   ├── CodeBLEU 
│   ├── codegen 
│   └── execution_evaluation_TC.py
└── src
    ├── make_submission_list_json.py
    ├── process_json.py
    └── split.py
```

# Environment creation  information



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
To run the codet5 model go to that folder and use run.sh. This will also evalualte the model on execution_evaluation, BLEU, CodeBleu
```
cd codet5/
nohup ./run.sh
```
