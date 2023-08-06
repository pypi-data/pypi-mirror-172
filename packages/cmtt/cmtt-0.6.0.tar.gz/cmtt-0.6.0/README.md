[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

<div>
<img width="600px" height="180px" src= "https://user-images.githubusercontent.com/76529011/185376373-787f65d5-b78b-4f11-a7fb-e9aa19dc3a04.png">
</div>

-----------------------------------------
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)![Compatibility](https://img.shields.io/badge/compatible%20with-python3.9.x-blue.svg)

CMTT is a wrapper library that makes code-mixed text processing more efficient than ever. More documentation incoming!
 
## Installation
```
pip install cmtt
```

## Getting Started
How to use this library:

```Python
from cmtt.data import *
from cmtt.preprocessing import *

# Loading json files
result_json = load_url('https://world.openfoodfacts.org/api/v0/product/5060292302201.json')

# Loading csv files
result_csv = load_url('https://gist.githubusercontent.com/rnirmal/e01acfdaf54a6f9b24e91ba4cae63518/raw/b589a5c5a851711e20c5eb28f9d54742d1fe2dc/datasets.csv')

# List the key properties available for the datasets provided by the cmtt library
keys = list_dataset_keys()

# List all datasets provided by cmtt based on search_key and search_term
data = list_cmtt_datasets(search_key="task", search_term = "ner", isPrint=True)

# Download multiple datasets provided by cmtt, returning a list of paths where the datasets get downloaded
# The Datasets are downloaded into a new 'cmtt' directory inside the user profile directory of the operating system
lst = download_cmtt_datasets(["linc_ner_hineng", "L3Cube_HingLID_all", "linc_lid_spaeng"])

# Download a dataset from a url, returning the path where the dataset gets downloaded
# The Dataset is downloaded into a new directory 'datasets' inside the current working directory
path = download_dataset_url('https://world.openfoodfacts.org/api/v0/product/5060292302201.json')

# CMTT currently provides 3 tokenizers - basic, word and wordpiece tokenizers
# Whitespace Tokenizer
text = "This Python interpreter is in a conda environment, but the environment has not been activated.  Libraries may fail to load.  To activate this environment"
tokenized_text_whitespace = whitespace_tokenize(text)

# Word Tokenizer
WordT = WordTokenizer()
tokenized_text_word = WordT.tokenize(text)

# Wordpiece Tokenizer
WordpieceT = Wordpiece_tokenizer()
tokenized_text_wordpiece  = WordpieceT.tokenize(text)

# Search functionality
instances, list_instances = search_word(text, 'this', tokenize = True, width = 3)

# Sentence piece based tokenizers for Hindi and Hinglish
# Download the models for the tokenizers. If already downloaded then cmtt does not download it again.
download_models('hi')
download_models('hi-en')

# Sentence piece based Tokenizer for Hindi
_hi = "मैं इनदोनों श्रेणियों के बीच कुछ भी० सामान्य नहीं देखता।"
lst = tokenize(_hi ,'hi-en')
# Output of tokenizer written on a txt file as terminal does not show devanagari text accurately.
with open(r"test_hi.txt", 'w', encoding = "utf-8") as f:
  for i in lst:
    f.write(i + "\n")

# Sentence piece based Tokenizer for Hinglish
_hien = "hi kya haal chaal? hum cmtt naam ki python library develop kar rahe hain"
lst = tokenize(_hien ,'hi-en')
with open(r"test_hien.txt", 'w', encoding = "utf-8") as f:
  for i in lst:
    f.write(i + "\n")
```

## Contributors
- [Paras Gupta](https://github.com/paras-gupt)
- [Tarun Sharma](https://github.com/tarun2001sharma)
- [Reuben Devanesan](https://github.com/Reuben27)