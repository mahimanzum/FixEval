readme added new

# Download project Codenet Whole dataset
wget https://dax-cdn.cdn.appdomain.cloud/dax-project-codenet/1.0.0/Project_CodeNet.tar.gz?_ga=2.133483278.1486692882.1645896851-1137262026.1645896851

# Download project Codenet Metadata
wget https://dax-cdn.cdn.appdomain.cloud/dax-project-codenet/1.0.0/Project_CodeNet_metadata.tar.gz?_ga=2.191718442.1486692882.1645896851-1137262026.1645896851

# folder structure (Need to edit)
```
├── README.md 
├── data 
├── gen 
│   ├── analysis 
│   ├── data-preparation 
│   └── paper
└── src
    ├── analysis
    ├── data-preparation
    └── paper
```

# Environment creation  information



# creating submission type json
make_submission_list_json.py parses problem submission informations, problem list csv, and the actual submission files folder to create an initial json processed.json which is a format like this.
```
cd src
python make_submission_list_json.py
```