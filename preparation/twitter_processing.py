import json
import re
import nltk
from nltk.tokenize import TweetTokenizer, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
nltk.download('stopwords')
import random
from nltk.util import ngrams
from operator import itemgetter
import sys


# Open twitter file and run gettwtext()


def gettwtext(data, outfile):			#writes a list with only texts into file
    raw_text =[]
    for line in data['text']:
        raw_text.append(line)
    
    with open(outfile + '_twtext.txt', 'w') as out1:
        json.dump(raw_text, out1)

# Open file generated from gettwtext() and put into split_it()

def clean_it_mix(data):			#returns a list of mixed texts and #words. keeps formation as post by post
    
    regex="\W+\s+|@[A-Åa-å0-9]+\.*[A-Åa-å0-9]*|\w+:\/\/\S+|pic.twitter.com/*|:-.|[#*!\?\(\)\{\}\[\]]"
    
    regex2="\W+\s+|\W\W|\W$"
    
    token=[' '.join(re.sub(regex, " ", x).split()) for x in data]
    token2=[' '.join(re.sub(regex2, " ", x).split()).lower() for x in token]

    return token2

def clean_it_hash(data):		#returns a list of #words. does NOT keep post by post formation. 
   
    tknzr = RegexpTokenizer('#[a-åA-Å0-9_][a-åA-Å0-9_]+')
    token = tknzr.tokenize(str(data))
    
    regex="\\\\n|#"
    
    token2=[' '.join(re.sub(regex, " ", x).split()).lower() for x in token]
    
    return token2


def clean_it_text(data): 		#returns a list of texts. keeps formation as post by post
    
    regex="\W+\s+|@\w+\.*\w*|\w+:\/\/\S+|pic.twitter.com/*|:-.|[\(\)\{\}\[\]]|[!\?*]"
    
    regex2="\W+#+\w+|#\w+|\W+\s+|\W+$|\W\W"
    
    token=[' '.join(re.sub(regex, " ", x).split()) for x in data]
    token2=[' '.join(re.sub(regex2, " ", x).split()).lower() for x in token]

    return token2


def split_it(data, outfile):

	# writes a .txt file for each of the sections above. keeps formation as in the functions above but tokenizez
	# each post - i.e. splitting the words in the post.
    
    data1=clean_it_text(data)         
    data2=clean_it_hash(data)         
    data3=clean_it_mix(data)          
    
    split_text=[]
    for line in data1:
        tknzr = RegexpTokenizer('\w+\S*\w*\s*')
        token = tknzr.tokenize(line)
        if token != []:
            split_text.append(token)

    split_hash = []
    for line in data2:
        tknzr = RegexpTokenizer('\w+\S*\w*\s*')
        token = tknzr.tokenize(line)
        if token != []:
            split_hash.append(token)
            
    split_mix=[]
    for line in data3:
        tknzr = RegexpTokenizer('\w+\S*\w*\s*')
        token = tknzr.tokenize(line)
        if token != []:
            split_mix.append(token)
    
    with open(outfile + '_text.txt', 'w') as out1:
        json.dump(split_text, out1) 
    
    with open(outfile + '_hash.txt', 'w') as out2:
        json.dump(split_hash, out2)  
        
    with open(outfile + '_mix.txt', 'w') as out3:
        json.dump(split_mix, out3)  

