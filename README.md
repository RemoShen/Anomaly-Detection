# Description of the project
* The development of the network, the abnormality of the equipment, the increasingly obvious detection detection tools and tools are usually only for spelling, spelling and format detection detection detection detection network service repetitive work work work work work work work work The detection speed of working tools is slow, the detection ability is weak, the ability is weak, and the general versatility is poor, etc. Unsupervised anomaly detection calculation method. Through statistical analysis, the calculation method can determine 7 detectable anomaly types, and supports anomaly location and anomaly modification scheme.

# Basic structure of the project
Data preprocessing -> frequency analysis of co-occurrence corpus -> construction of parsing tree model -> anomaly detection

# Detailed structure of the project
## training model treetr.py
* According to the calculation of tf and df, the keywords are saved in big.txt, and finally the data in attr.txt/attr.csv is used, because it is the result of multiple iterations of training and has high versatility.
* Build a configuration statement tree for the pre-training file pre_load_file and save it in lgtree.
* Extract the characteristics of the configuration statement tree structure and save it in vc.csv
* Cluster the configuration statement tree, the model is saved in set.pkl

## detection model checkError.py
* Build a configuration statement tree for the file to be detected and save it in rstree
* Profiles for computing exceptions according to the model and their location and error types
* Throw an exception according to the rules and save it in error.txt

# Project details
* create_tree.py Create a configuration statement tree (the core algorithm of this project)
* dataloader.py Load data
* define_occr 
* func_paratools.py Toolkit, including detection rules used in the project, paragraph word matching and other methods
* CorrectWords.py Some methods of word processing, such as edit distance, word cutting, etc.
* listdir_inmac 
* tf_df.py Calculation method of word frequency and document frequency
* tools.py Some tools, such as ip and port detection packages, clustering methods, etc.
* train_tree.py  Extract the structural information of the configuration statement tree
* tree_tools.py Some detailed tools used in the process of processing trees, such as word segmentation, segmentation, etc.
* atre.txt The shape of a configuration statement tree

# Environment
* python 3.9.7
* base on Linux or macOS Monterey

# Package
install command：pip install + package name
* joblib==1.1.0
* numpy==1.21.4
* scikit_learn==1.2.1
* treelib==1.6.1
* collections
* matplotlib

# How to use
* run py 'checkError.py' to achieve errors in the files