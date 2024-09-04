import json
import re
import nltk
from nltk.tokenize import RegexpTokenizer

#list of texts and #words, post by post
def clean_it_mix(data):
    
    regex="\W+\s+|@[A-Åa-å0-9]+\.*[A-Åa-å0-9]*|\w+:\/\/\S+|pic.twitter.com/*|:-.|[#*!\?\(\)\{\}\[\]]"
    
    regex2="\W+\s+|\W\W|\W$"
    
    token=[' '.join(re.sub(regex, " ", x).split()) for x in data]
    token2=[' '.join(re.sub(regex2, " ", x).split()).lower() for x in token]

    return token2

#list of #words
def clean_it_hash(data):

    tknzr = RegexpTokenizer('#[a-åA-Å0-9_][a-åA-Å0-9_]+')
    token = tknzr.tokenize(str(data))
    
    regex="\\\\n|#"
    
    token2=[' '.join(re.sub(regex, " ", x).split()).lower() for x in token]
    
    return token2

#list of texts, post by post
def clean_it_text(data): 

    regex="\W+\s+|@\w+\.*\w*|\w+:\/\/\S+|pic.twitter.com/*|:-.|[\(\)\{\}\[\]]|[!\?*]"
    
    regex2="\W+#+\w+|#\w+|\W+\s+|\W+$|\W\W"
    
    token=[' '.join(re.sub(regex, " ", x).split()) for x in data]
    token2=[' '.join(re.sub(regex2, " ", x).split()).lower() for x in token]

    return token2

#list whit a list for each cleaned post where each word is an entry in a list
def split_it_mix(data):         
    
    data=clean_it_mix(data)
    split_text=[]
    for line in data:
        tknzr = RegexpTokenizer('\w+\S*\w*\s*')
        token = tknzr.tokenize(line)
        if token != []:
            split_text.append(token)

    return split_text

def split_it_text(data):         
    
    data=clean_it_text(data)
    split_text=[]
    for line in data:
        tknzr = RegexpTokenizer('\w+\S*\w*\s*')
        token = tknzr.tokenize(line)
        if token != []:
            split_text.append(token)

    return split_text
