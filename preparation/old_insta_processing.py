import json
import re
import nltk
from nltk.tokenize import TweetTokenizer, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
nltk.download('stopwords')
import random
from nltk.util import ngrams
from operator import itemgetter


with open(filename_hash, 'r') as file1, open(filename_loc, 'r') as file2:
    data1= json.load(file1, encoding='utf-8')
    data1= json.load(file2, encoding='utf-8')

def gettext(data):
    raw_text = []           #returns a list of text    
    for caption in data:
        try:
            text = caption["edge_media_to_caption"]['edges'][0]['node']['text']
        except IndexError:
            continue
        raw_text.append(text)
    return raw_text


def gethash(data):
raw_tags = []               #returns a list of #words without #
for line in data:
    try:
        hashtag = line.get('tags')
    except IndexError:
        continue
    raw_tags.append(hashtag)
return raw_tags


def no_dupl(data1, data2, outfile):   #list1 could be location and list2 hashtags. outfile e.g. 'nørrebro_fil'.
    
    text1= gettext(data1)   # returns a list of dics with key 'text' and values as strings
    text2= gettext(data2)   # same as above
    no_dup_text=set()       # this is the string that will be written into a file with only raw text
    
    hash1= gethash(data1)   # returns a list of #words without #
    hash2= gethash(data2)   # same as above
    no_dup_hash=hash1.copy()# copy the first list to add onto from the second list 
    
    for line in text1:
        for key, value in line.items():   #try to get the value from the dict key 'text' if availabe
            #if value not in no_dup_text:
            no_dup_text.add(value)  #add the text to the string
    
    for line in text2:      #each line in the list is a dictionary
        for key, value in line.items():   #get the value from the dict key 'text'
            #if value not in no_dup_text:  #if the value is not already a string in no_dup_hash: add it
            no_dup_text.add(value)
    
    for line in hash2:      #for the line of hashtags in the list
        if line not in no_dup_hash:  #if the line is not already in no_dup_hash: append it
            no_dup_hash.append(line)
            
    
    text =[]
    for line in no_dup_text:
        text.append(line)
        
    with open(outfile + '_text.txt', 'w', encoding='utf-8') as out1:
        json.dump(text, out1)
        #out1.write("".join(text))
    
    with open(outfile + "_hash.txt", "w") as out2:    #write hashtag file from the final list (with no duplicates)
        json.dump(no_dup_hash, out2)
        
    print("textfile with length", len(no_dup_text), "has been saved as", outfile + "_text.txt")
    print("hashtag file with length", len(no_dup_hash), "has been saved as", outfile + "_hash.txt")



def final_text(data):
    #raw_text= str(gettext(data))
    
    raw_text = str(data)

    tknzr = RegexpTokenizer('\S+\w+')
    token_words = tknzr.tokenize(raw_text)

    words = []
    for word in token_words:
        match=re.search(r'(http)|\\u\d{3}\w', word)
        if match:
            continue
        elif word[0] == '#':
            continue
        elif word[0] == '@':
            continue
        else:
            words.append(word)
            
    new_list=''
    for word in words:
        match=re.search("#+|\*+|\!+|[\n]+|[\\\]+", word)
        if match:
            #print(word)
            spl=re.split(r'\\n#|\\n|#',word)
            for word in spl:
                match=str(re.match('\w', word))
                if match:
                    new_list+=word + ' '
        else:
            new_list+=word + ' '
    
    new_token_words = tknzr.tokenize(new_list)
    
    lowercase=[]
    for word in new_token_words:
        word=word.lower()
        lowercase.append(word)
        
    return lowercase

    def gram(data, n):    # For final text

    words= final_text(data)
    counts ={}
    raw_ngrams = ngrams(words, n)
    for ngram in raw_ngrams:
        counts[ngram]=counts.get(ngram,0)+1
       
    return sorted(counts.items(), key=itemgetter(1), reverse=True)


    def hgram(data, n):    # For #words

    counts ={}
    for line in data:
        raw_ngrams = ngrams(line, n)
        for ngram in raw_ngrams:
            counts[ngram]=counts.get(ngram,0)+1
       
    return sorted(counts.items(), key=itemgetter(1), reverse=True)


    def bigram(words):
    the_dict={}
    while len(words) > 2:
        word = words.pop(0)
        next_word = words[0]
        if word in the_dict:
            the_dict[word].append(next_word)
        if word not in the_dict:
            the_dict[word]=[next_word]
    return the_dict