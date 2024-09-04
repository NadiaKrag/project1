
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


#Open a file and put it into data_merge()

def gettext(file):
    raw_text = []                #returns a list of textst, not cleaned
    for line in file:
        try:
            text = line["edge_media_to_caption"]['edges'][0]['node']['text']
            raw_text.append(text)
        except IndexError:
            continue
    return raw_text


def data_merge(data1, data2, outfile):   #data1 could be location and data2 hashtags.
    
    text1= gettext(data1)   		# returns a list of texts
    text2= gettext(data2)   		# same as above
    merge_text=text1.copy()    		
    
    
    for line in text2:
        merge_text.append(line)  	#append each post
    
        
    with open(outfile + '_merge.txt', 'w') as out1:
        json.dump(merge_text, out1)
    
#Open the file generated from data_merge() and put it into split_it()

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