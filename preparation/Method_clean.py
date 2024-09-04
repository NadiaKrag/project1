'''  
This is an automatic script. 
It's an updated, optimized and improvemed version of the first script that can be used for both Pre-Processing and Term Frequency.
-- 
It runs through the terminal for which it takes an input and outputs: 
Messy wordlist: 
- A file with messy words (with stopwords) = wordlist = tokenized by tweet_token
- A file with messy words (with stopwords) = wordlist_2 = tokenized by re 
---- 
Cleaned data: 
- A file of cleaned for stopwords = cleaned_for_stopwords_tweet
- A file of cleaned for stopwords = cleaned_for_stopwords_re 
---- 
Terms filtering: 
- A file with all hashtags from the input (no stopwords)
- A file with all the term only (no stopwords nor hashtags)
- A file with all the terms (and emojis) (no stopwords nor hashtags)
---- 
The output of these files will be txt, and seperated by commas. 
The output files can be used for which ever purposes, TF, TF-IDF, Sentiment analysis etc.: 
-- 
OBS: Remember to comment out the section which you don't want to use
'''

import json
import sys
import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer


class TF(object): 
    def __init__(self):
        self.wordlist = [] # Messy wordlist with stopwords with tweet tokenzier 
        self.wordlist_2 = [] # Messy wordlist with stopwords with regular expression

        self.cleaned_for_stopwords_tweet = [] # Cleaned for stopwords with tweet
        self.cleaned_for_stopwords_re = []    # Cleaned for stopwords with re

        self.term_hash = [] # Only hash list 
        self.term_only = [] # Terms & (possible) emojis list 
        self.term_re = []   # Only terms

        self.term_hash_top = [] # Most common hashtags (10) list 
        self.term_only_top = [] # Most common terms with possible emojis list 
        self.term_re_top = []   # Most common terms (no emojis) 
# -------------------------------------------------------

        ''' This function reads the data, targets the values, tokenize it and makes a list of 'messy words' '''

    def preprocessing(self, target): 
        with open(target,"r") as file:      # Opening the json file in 'r' mode as f
            data = json.load(file)          # Loading the json file into a Python dict


                                            
            raw_characters = ""             # Making an empty string
            for characters in data:         # Targeting each character inside 'text', inside 'node', inside 'edges', inside 'edge_media_to_caption''
                try:                        # Try to get the values 
                    text = characters["edge_media_to_caption"]['edges'][0]['node']['text']
                except IndexError:          # If file structure is corrupt then continue
                    continue
                raw_characters += text

# -------------------------------------------------------

        ''' Two different splitting methods - If no changes is applied, both will be outputted '''

        # Splitting by regular expression
        self.wordlist_2 = re_token_words = re.findall(r"[\w]+", raw_characters)   

        # Splitting by tweet-tokenizer 
        tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)  # Removes handles and shortens consective characters more info on: goo.gl/T7iMx4
        self.wordlist = tknzr.tokenize(raw_characters)               # Save the tokenized words into wordlist  
        
        # Output the messy wordlist (with stopwords) - Tweet_tokenizer
        with open(str(target) + "_wordlist.txt","w") as file:        # Save the wordlist and output it 
            file.write(",".join(self.wordlist))                      # If not output is needed, comment this section out 
        
        # Output the messy wordlist (with stopwords) - Regular Expression
        with open(str(target) + "_wordlist_2.txt","w") as file:      # Save the wordlist and output it 
            file.write(",".join(self.wordlist_2))                    # If not output is needed, comment this section out 

# -------------------------------------------------------

        ''' Stopword implementation '''

        # Implementing stopwords 
        stop_dan = stopwords.words("danish")        # Danish stopwords 
        stop_eng =  stopwords.words("english")      # English stopwords 
        stop = stop_eng+stop_dan
        
        # Removing the stopwords & outputting the cleaned words
        self.cleaned_for_stopwords_tweet = [word for word in self.wordlist if word not in stop] 
        with open(str(target) + "_cleaned_for_words_tweet.txt","w") as file:
            file.write(",".join(self.cleaned_for_stopwords_tweet))

        # Removing the stopwords & outputting the cleaned words <- (UNCOMMENT TO RUN) 
        self.cleaned_for_stopwords_re = [word for word in self.wordlist_2 if word not in stop] 
        #with open(str(target) + "_cleaned_for_words_re.txt","w") as file:
        #    file.write(",".join(self.cleaned_for_stopwords_re))

# -------------------------------------------------------

        ''' Methods - Term filtering '''

        # ONLY HASHTAGS - NO WORDS WITH NO HASHTAGS IN THE BEGINING
        self.term_hash = [term for term in self.cleaned_for_stopwords_tweet if term.startswith("#")] # Only words with '#' gets saved
        with open(str(target) + "_term_hash.txt","w") as file:                                       # Outputs only the hashtags 
            file.write(",".join(self.term_hash))
        

        # WORDS & EMOJIS
        self.term_only = [term for term in self.cleaned_for_stopwords_tweet if term not in stop and not term.startswith(("#", "@", "-", "_", ",", ".", "/", "’", "!", "?", ")", "(", ":", ";"))] # Only terms gets saved 
        with open(str(target) + "_term_only.txt","w") as file:                                                                                # Outputs only the hashtags     
            file.write(",".join(self.term_only))


        # ONLY WORDS - NO HASHTAGS NOR EMOJIS 
        self.term_re = [term for term in self.cleaned_for_stopwords_re if term not in stop and not term.startswith(("#", "@", "-", "_", ",", ".", "/", "’", "!", "?", ")", "(", ":", ";"))] # Only terms gets saved 
        with open(str(target) + "_term_re.txt","w") as file:                                                                                # Outputs only the hashtags     
            file.write(",".join(self.term_re))

# -------------------------------------------------------

        ''' Term frequency of words '''

        # Top hashtags 
        term_hash_count = Counter(self.term_hash)               # Counting term_hash
        self.term_hash_top = term_hash_count.most_common(10)    # Making a top of common words <- Resizable
        print("The 10 most commom hashtags are:", self.term_hash_top)

        # Top terms (no emojis)
        term_re_count = Counter(self.term_re)                   # Count terms only
        self.term_re_top = term_re_count.most_common(10)        # Making a top of common words <- Resizable
        print("The 10 most common terms (without emojis) are:", self.term_re_top)
        
        # Top terms (inclusive emojis)
        term_only_count = Counter(self.term_only)               # Counting terms_only
        self.term_only_top = term_only_count.most_common(10)    # Making a top of common words or emojis <- Resizable 
        print("The 10 most common terms with emojis are:", self.term_only_top)

# -------------------------------------------------------

        ''' The function caller '''
args = sys.argv
filename = args[1]
technique = TF()
technique.preprocessing(filename)
