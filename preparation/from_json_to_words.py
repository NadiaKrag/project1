''' This code is a json extractor, that takes a json file as input, targets a, then collects 
		 and cleans the data. In this case from json to ready-to-go words for NLP        '''

'''  The code can be modified and adapted to fit different kind of json data and different targets'''

import json                              # For reading in json files                              # For later regular expression processing through sentences                          # The whole natural language toolkit 
from nltk.tokenize import TweetTokenizer # For later natural language for the adaption of tweet feeds/insta posts 


''' Load and transform  json data into Python dictionary '''
def load_insta_text(target): 
    with open str(target)+ ".json", "r") as f: # Loading the json file into python as read 
        data = json.load(f) # Making the json file into a Python dict
        
        # Creating a string of words 
        raw_characters = ""
        for line in data: 
            try: 
                text = line["edge_media_to_caption"]['edges'][0]['node']['text']
            except IndexError:
                continue
            raw_characters+=(text) 
    
    # Tokenizing the words, keeps hashtags and signs
    tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)  # Removes handles and shortens consective characters more info on: goo.gl/T7iMx4
    tweet_token_words = tknzr.tokenize(raw_characters)    
        
    # Save file as txt file
    with open(str(target) + 'filename.txt', 'w') as f:
    f.write('\n'.join(tweet_token_words)) 

    ''' Next methods can be used to load in the txt file, 
    and have the same output as tweet_token_words to apply to any method''' 

    # Just copy paste it into the begining of the method
#def load_ready_text_to_go()
#    data = []
#    with open("filename.txt", "r") as file:  
#        for line in file.readlines():
#            data.append(line)

#with open("whatever.json", "r") as f:       # Opening the json file in 'r' mode as f
#	data = json.load(f)                     # Loading the json file into a Python dict


''' Creating a string of words '''
raw_characters = ''                         # Making an empty string 
for characters in data:                     # For each character in 'data'/python dict, apppend the following: 
	try:									# Try target following line
		text = characters["edge_media_to_caption"]['edges'][0]['node']['text'] # Targeting each character for 'text', inside 'node', inside 'edges', inside 'edge_media_to_caption''
	except IndexError:						# Except for when people didn't write anything about their uploaded picture
		continue
	raw_characters += text                  # Each character gets joined to the empty string

'''Removing URL from the string of words'''

no_URL_raw_characters = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', raw_characters) #making a string of raw characters without URL

'''----------------- Introducing two methods for splitting by word ---------------------'''

''' Method 1 - Tweet_token (keeps words - keeps signs) '''
tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)  # Removes handles and shortens consective characters more info on: goo.gl/T7iMx4

tweet_token_words = tknzr.tokenize(raw_characters)           # This nltk tokenizer splits every word in 'Twitter-recognizing' matter 
# OBS: KEEPS/recognize hashtags words, smileys, exclamation points, hypen and other signs 

#print(tweet_token_words[0:2])                               # Testing the visual results 
#print(len(tweet_token_words))                               # Checking the number of found words


''' Method 2 - Regular expression (keeps words - removes signs) '''
re_token_words = re.findall(r"[\w]+", raw_characters)        # This regular expression module splits every word by whitespace 
# OBS: REMOVES hashtag words, smileys, exclamation  --> ONLY KEEPS words and numbers, other unknown signs gets removed

#print(re_token_words[0:2])                                  # Testing the visual results
#print(len(re_token_words))                                  # Checking the number of found words


# Inspiration for NLP: https://marcobonzanini.com/2015/03/17/mining-twitter-data-with-python-part-3-term-frequencies/ 