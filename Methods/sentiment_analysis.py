from nltk.tokenize import TweetTokenizer
from afinn import Afinn
from collections import Counter
import nltk
import json
import re
import sys
import statistics

AFINN_da = Afinn(language = "da",emoticons=True)
AFINN_en = Afinn(language = "en",emoticons=True)
AFINN_dict = dict(AFINN_da._dict, **AFINN_en._dict)

def sentiment_words(text):

	#----------------sentiment analysis for each word---------------------

	#tokenize with smileys
	string = ' '.join(dataset)
	tokenize = TweetTokenizer()
	tokens = tokenize.tokenize(string)

	#count sentiment score for each token

	score = 0
	sentiments = []

	for word in tokens:
		if word in AFINN_dict:
			score += int(AFINN_dict[word])
			sentiments.append(word)

	#print(Counter(sentiments).most_common(100))

	return sentiments

def sentiment_tweets(text):

	#---------------sentiment analysis for each tweet----------------------

	#count total sentiment score for each tweet

	tweet_score = 0
	tweets_values = []
	temp_score = 0
	tweet_sentiments = {}

	i = 0
	for tweets in dataset:
		temp_score = 0
		tweet_words = tweets.split()
		for word in tweet_words:
			if word in AFINN_dict:
				tweet_score += int(AFINN_dict[word])
				temp_score += int(AFINN_dict[word])
				tweets_values.append(int(AFINN_dict[word]))
		tweet_sentiments[i] = [tweets,temp_score]
		i += 1

	print(f"Sentiment total score for {text} is: ",tweet_score)
	print(f"Mean sentiment value for each tweet for {text} is: ",tweet_score/len(dataset))
	print(f"Standard diviation for each tweet for {text} is: ", statistics.stdev(tweets_values))

	return tweet_sentiments


def feature_extraction(text):

	#---------------feature extraction for topic modelling--------------------

	tweet_sent = sentiment_tweets(text)

	neg_sentiments = []
	pos_sentiments = []
	zero = []

	for key,j in tweet_sent.items():
		if j[1] < 0:
			neg_sentiments.append(j)
		elif j[1] > 0:
			pos_sentiments.append(j)
		else:
			zero.append(j)

	print("Total tweets/posts: ", len(dataset))
	print("Number of neutral tweets/posts: ", len(zero))

	print(neg_sentiments[:10])
	print("Numbers of negative tweets/posts", len(neg_sentiments))
	print("Percentage of negative posts", ((len(neg_sentiments))/(len(dataset)))*100)	

	print(pos_sentiments[:10])
	print("Numbers of positive posts",len(pos_sentiments))
	print("Percentage of positive posts",((len(pos_sentiments))/(len(dataset)))*100)

	neg_list = []

	for i in neg_sentiments:
		neg_list.append(i[0])

	pos_list = []

	for i in pos_sentiments:
		pos_list.append(i[0])

	#with open(text + ".json","w",encoding="utf8") as file:
		#json.dump(neg_list,file,default=str,indent=1,ensure_ascii=False)

	#with open(text + ".json","w",encoding="utf8") as file:
		#json.dump(pos_list,file,default=str,indent=1,ensure_ascii=False)

if __name__ == "__main__":

	text = sys.argv[1]

	with open(text,"r") as file:
		dataset = json.load(file)
		data = dataset

	#remove hashtags, usertags and other junk

	REGEX = "(@[A-Za-z0-9]+)|(\w+:\/\/\S+)|#|@|(pic.twitter.com/*)" 
	dataset = [' '.join(re.sub(REGEX," ",x).split()).lower() for x in data]

	sentiment_tweets(sys.argv[1])
	feature_extraction(sys.argv[1])
