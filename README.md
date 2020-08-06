# Wikimedia To Text Corpus

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![MIT license](https://img.shields.io/badge/License-MIT-green.svg)

[Wikimedia](https://www.wikimedia.org/) is the driving force behind [Wikipedia](https://www.wikipedia.org/).
They provide a monthly full backup of all the data on Wikipedia as well as their properties.
The purpose of this repo is to convert the Wikimedia dump format into our standard text corpus format.
I.E., one document per file, one sentence per line, paragraphs have a blank line between them.

# Setup

This repository follows both our standard [prerequisite](https://github.com/TextCorpusLabs/getting-started#prerequisites) and [Python](https://github.com/TextCorpusLabs/getting-started#python) instructions.

# Steps

The below document describes how to retrieve the text corpus.
The walkthrough assumes both a particular target folder and wiki.
Both of these can be modified without changing the code.
For the target folder, make sure you have a _lot_ of space.
[This page](https://dumps.wikimedia.org/backup-index.html) lists all the available wiki dumps.
In general, they are updated twice a month.
If they are still in progress, get the former dump.

1. Clone this repository then open a shell to the `~/code` directory.
2. [Retrieve](./code/download_wikimedia.py) the dataset.
   ```{shell}
   python download_wikimedia.py -wiki enwiki -date 20200720 -dest d:/enwiki
   ```
3. Extract the data in-place.
   ```{shell}
   "C:/Program Files/7-Zip/7z.exe" e -od:/enwiki "d:/enwiki/*.bz2"
   del "d:\enwiki\*.xml.bz2"
   ```
4. [Extract](./code/extract_article_metadata.py) the article metadata.
   This will create a single `metadata.csv` containing some useful information.
   In general this would be used as part of segementation or as part of a MANOVA.
   ```{shell}
   python extract_article_metadata.py -in d:/enwiki/enwiki-20200720.xml -out d:/enwiki/metadata.csv
   ```
5. [Extract](./code/extract_article_text.py) the article text.
   This will create a folder containing all the articles in text only form.
   One article per file.
   ```{shell}
   python extract_article_text.py -in d:/enwiki/enwiki-20200720.xml -out d:/enwiki/articles
   ```
6. [Tokenize](./code/tokenize_article_text.py) the article text.
   This will create a folder containing all the tokenized documents.
   Creating one sentence per line with paragraphs have a blank line between them.
   ```{shell}
   python tokenize_article_text.py -in d:/enwiki/articles -out d:/enwiki/tokenized
   ```