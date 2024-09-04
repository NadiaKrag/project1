from collections import Counter
import nltk
import json
import re
import math
import sys
import operator
from constants import STOPWORDS
from clean import clean_it_hash, clean_it_text, split_it_text
import os

#remove stopwords
def no_stopwords(text):

	no_stopwords = []
	for word in text:
		if word not in STOPWORDS:
			no_stopwords.append(word)

	return no_stopwords

def ngram_extraction(text):

	#extract hashtags and remove stopwords for unigram_hashtag
	h=clean_it_hash(text)
	hashtags=no_stopwords(h)

	#extract texts for or bi- and trigrams
	t=clean_it_text(text)
	gramtext=split_it_text(t)

	#and remove stopwords for unigram_text
	uni_text=no_stopwords(gramtext)

	#extract ngrams
	#unigram_hashtag = nltk.unigram(hashtags)
	#unigram_text = nltk.unigram(uni_text)
	bigram_text = nltk.bigrams(gramtext)
	trigram_text = nltk.trigrams(gramtext)

	#calculate frquency distribution
	#uni_hash_dist = nltk.FreqDist(unigram_hashtag)
	#uni_dist = nltk.FreqDist(unigram_text)
	bi_dist = nltk.FreqDist(bigram_text)
	tri_dist = nltk.FreqDist(trigram_text)


	#uni_hash_dict = dict(uni_hash_dist)
	#uni_dict = dict(uni_dist)
	bi_dict = dict(bi_dist)
	tri_dict = dict(tri_dist)


	#sorted_uni_hash_dist = sorted(uni_hash_dict.items(), key=operator.itemgetter(1), reverse=True)
	#sorted_uni_dist = sorted(uni_dict.items(), key=operator.itemgetter(1), reverse=True)
	sorted_bi_dist = sorted(bi_dict.items(), key=operator.itemgetter(1), reverse=True)
	sorted_tri_dist = sorted(tri_dict.items(), key=operator.itemgetter(1), reverse=True)

	#print("unigram from hashtags: "+sorted_uni_hash_dist)
	#print("unigrams from text: "+sorted_uni_dist)
	print("bigrams from text: "+ sorted_bi_dist)
	print("trigrams from text: "+ sorted_tri_dist)


if __name__ == "__main__":

	#load in data

	files = sys.argv[1]
	files = [file for file in os.listdir(files) if file.endswith(".json")]
	for file in files:
		print(file)
		with open(sys.argv[1] + file, "r", encoding = 'UTF8') as infile:
			text = json.load(infile)

ngram_extraction(text)
