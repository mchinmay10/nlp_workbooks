# Custom Tokenizer

## Brief Note

While creating this assignment I was determined in not using the NLTK library and to get in-depth hands-on experience about NLP pipeline stages: this one being data preprocessing!

As a result, I have created a Github repo which has step by step progress reports on how this "grounds-up" tokenizer has been built.

I will be deeply in gratitude if the reader checks it out, interacts with it, and suggests corrective changes (PS: There are going to be a lot of them :) )

Github Repo link: https://github.com/novice0/nlp_workbooks

Feel free to reach out to me for suggesting ANY corrections / improvements at my LinkedIN: https://www.linkedin.com/in/chinmay-m-996195254/

## Introduction

This is a text tokenizer built from scratch using the Python programming language. I designed a pipeline to apply tokenization on the corpus. The core idea of the pipeline is a hierarchy of stages that converts raw text into canonical formats and then process the file for further tokenization.

## Overview of the Hierarchy:

This is done to make sure one kind of token (eg; like an emoticon) is not mistaken for another kind of token (eg; like a punctuation).

This step by step approach ensures logical clean up and maintains the semantics of text tokenization.

The hierarchy followed while designing the custom tokenizer is as follows:
a. Removal of HTML tags

- This is done because the scraped corpus may contain some residual HTML tags

b. Conversion of date and time to canonical format

c. Word / Word composition split into new lines

- This ensures some compound, atomic entities like urls, hashtags, canonical date and time, hyphenated words lie in the same line,

- Enables efficient cleanup of a variety of tokens

d. Extraction and processing of various tokens like:

- Canonical dates
- Canonical times
- URLs
- Usermentions
- Hashtags

e. Extraction and conversion (splitting of clitics):

- clitics are extracted in this step

- a custom python dictionary is used to split the clitics into their corresponding split version,

- so if in the output if you come across a line saying that a particular clitic isn't being handled yet, please don't worry. Simply add the clitic and map its corresponding split words into our python dictionary.

- You can find out about how clitics are handled in the clitic_handler.py

f. Extract emoticons

g. Extract and process hyphenated words

h. Extract Abbreviations

i. Finally extracted punctuations

j. All the remaining tokens are considered as they are in the final clean up step

k. Stanford NERTagger is run on the tokenized text, and tagging is performed.

## Creation of Standard output files for each token type

1. This aids in the bottom-up creation of the final standard output file as mentioned in the assignment guidelines

2. Helps in debugging and tracing of errors

## Creation of intermediate files

1. After extracting each type of token, I am making sure that I remove the tokens of the type from the initial input file and then pass on this modified file further down in the tokenization pipeline

## Nuances to consider and to improve upon

Obviously this tokenizer isn't perfect. It is naive and built for the very reason of improving it and making it robust.

Following things that can be improved upon:

1. More abstraction and modularisation of code!

2. Right now my code is doing a lot of file I/O. This is NOT the most efficient approach in solving an NLP problem. I have to still find out a more efficient way to extract, process and delete tokens from the original input file in the subsequent stages of my pipeline.

3. Robust handling of date and time. As of now I am not consdering all the possible ways people write dates as well as times. This is resulting in incorrect tokenization and conversion of dates and times in their canonical formats.

4. Robust handling of clitics. The fundamental base python dictionary should be more extensive. As of now it isn't.

5. I ran the Stanford NER Tagger on the following test data sets I have used:

- corpus.txt (a generated novel from the repo: https://github.com/dariusk/harpooneers/tree/master)
- master_test.txt (contains all types of tokens mentioned in Moodle for primary testing of my tokenizer)

6. The Stanford tagger is working perfectly fine with these. But not the dataset given by our professor. This is because java is running out of memory.

7. Hence, to implement batch NER tagging. Currenly my NER Dict text file is created using a short version of the corpus given by our professor (one that doesn't run out of memory!)
