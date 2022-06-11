# Keywords extraction

## Introduction
This program is used to extract keywords, keypharses from a French text.
This program now supports as a CLI app.
The program will accept text from CLI, txt file, and json format.
For option of using server, please insert json format and use postman to test.

## Prerequistites
Please ensure the following requirements are satisfied:
* OS system: Linux or Mac OS
* Python 3
* You have installed Virtual Environement for Python
* Downloaded the project to your folder

## Installation
Open your CLI, go to the project path and run following commands
* pipenv shell
Initialize the Virtual Environement in your project directory
* pipenv install -r requirements.txt
Install all requirements for the project
* pipenv check
Check if there is any conflict in the environement
* python3 -m spacy download fr_core_news_lg
Download this model from spacy

## Usage
If you want to type the text directly from your CLI, use following command
* python3 -m run --text
You can also insert your txt file path by using following command
* python3 -m run -t yourtxtfilepath
For choosing server option, you need to insert json format with method POST
* python3 -m run -s

## Citations
* Keybert
@misc{grootendorst2020keybert,
  author       = {Maarten Grootendorst},
  title        = {KeyBERT: Minimal keyword extraction with BERT.},
  year         = 2020,
  publisher    = {Zenodo},
  version      = {v0.3.0},
  doi          = {10.5281/zenodo.4461265},
  url          = {https://doi.org/10.5281/zenodo.4461265}
}
* Sbert
@article{reimers2019sentence,
   title={Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks},
   author={Nils Reimers, Iryna Gurevych},
   journal={https://arxiv.org/abs/1908.10084},
   year={2019}
}
* Camembert
@article{martin2020camembert,
   title={CamemBERT: a Tasty French Language Mode},
   author={Martin, Louis and Muller, Benjamin and Su{\'a}rez, Pedro Javier Ortiz and Dupont, Yoann and Romary, Laurent and de la Clergerie, {\'E}ric Villemonte and Seddah, Djam{\'e} and Sagot, Beno{\^\i}t},
   journal={Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics},
   year={2020}
}

## References 
### Keywords extraction
* [Keyword Extraction with BERT] (https://towardsdatascience.com/keyword-extraction-with-bert-724efca412ea)
* [Benchmark of 7 Algorithms for Keyword in Python] (https://towardsdatascience.com/keyword-extraction-a-benchmark-of-7-algorithms-in-python-8a905326d93f)
* [MDERank] (https://arxiv.org/pdf/2110.06651v2.pdf)

### Models
* [SentencePiece Tokenizer Demystified] (https://towardsdatascience.com/sentencepiece-tokenizer-demystified-d0a3aac19b15)
* [BERT] (https://arxiv.org/pdf/1810.04805.pdf)
* [Sentence-BERT] (https://arxiv.org/pdf/1908.10084.pdf)
* [Train Sbert 1] (https://www.sbert.net/examples/training/sts/README.html)
* [Train Sbert 2] (https://www.youtube.com/watch?v=RHXZKUr8qOY)
* [Data Augmentation Method to improve SBERT] (https://towardsdatascience.com/advance-nlp-model-via-transferring-knowledge-from-cross-encoders-to-bi-encoders-3e0fc564f554)
* [Sentence Embedding Fine-tuning for the French Language] (https://lajavaness.medium.com/sentence-embedding-fine-tuning-for-the-french-language-65e20b724e88)
* [Camembert] (https://camembert-model.fr/)

# TODO
## Improve performance of program
* Improve filter POS speed
* Multi processing of spacy model
## Improve accuracy
* Re-training Sbert
* Preprocessing with Regex
* Preprocessing HTML file