from __future__ import print_function
from time import time
import os
import sys
import json
import re
import numpy as np

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from constants import STOPWORDS
import matplotlib.pyplot as plt

class Fitter():
	''' 
	Class that will take a list where each document is an entry in the list and TF(-IDF) model it and subsequently fit NMF and LDA on it.
	@ Code adapted from sklearn example under LDA 
	@ Author: Olivier Grisel <olivier.grisel@ensta.org>, Lars Buitinck, Chyi-Kwei Yau <chyikwei.yau@gmail.com>
	'''
	def __init__(self, hashtag, corpus, topics = 10, features = 1000, top_words = 20):
		''' Needs hashtag for naming
		: hashtag : the hashtag or district being modelled on (used for file-naming)
		: corpus : (list) the corpus being trained on
		: topics : optional argument denoting the number of topics the model should output
		: features : the number of the most occuring words in corpus to consider
		: top_words : how many words each topics should be comprised of
		'''
		self.name = hashtag
		self.n_components = topics
		self.n_features = features
		self.n_top_words = top_words
		self.corpus = self._clean_it(corpus)
		self.tfidf, self.tfidf_vectorizer = self.TFIDF()
		self.tf, self.tf_vectorizer = self.TF()
		
	def _write_topics(self, model, prob, denoter, feature_names, n_top_words):
		with open("results/final.txt", "a", encoding = "UTF8") as outfile:
			outfile.write(f"Top {self.n_components} topics for {self.name} using the {denoter}.\n")
			for topic_idx, topic in enumerate(model.components_):
				message = "Topic #{} with probability {:.2%}: ".format(str(topic_idx + 1), prob[topic_idx])
				message += " ".join([feature_names[i]
									 for i in topic.argsort()[:-n_top_words - 1:-1]])
				outfile.write(message + "\n")
			outfile.write("\n")
			
	def _clean_it(self, corpus):
		# Regular expression string used for cleaning and separating the old from the gold.

		REGEX = "(@[A-Za-z0-9]+)|(\w+:\/\/\S+)|#|@|(pic.twitter.com/*)"

		# Make a new list of all the 
		new_corpus = [' '.join(re.sub(REGEX," ",x).split()).lower() for x in corpus]
		return new_corpus
	
	def TF(self):
		# Use tf (raw term frequency) features for LDA.
		print("Extracting tf features for LDA model...")
		tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
										stop_words=STOPWORDS)
		t_0 = time()
		tf = tf_vectorizer.fit_transform(self.corpus)
		print(f"done in {time()-t_0:.2f}s.")
		return tf, tf_vectorizer
	
	def TFIDF(self):
		# Use tf-idf features for NMF.
		print("Extracting tf-idf features for NMF...")
		tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,
										   stop_words=STOPWORDS,
										   sublinear_tf=True,
										   strip_accents="unicode")
		t_0 = time()
		tfidf = tfidf_vectorizer.fit_transform(self.corpus)
		print(f"done in {time()-t_0:.2f}s.")
		return tfidf, tfidf_vectorizer
		
	def fit_NMF(self):
		# Fit the NMF model
		print(f"Fitting the NMF model (Frobenius norm) with tf-idf features, n documents={len(self.corpus)} and n features={self.n_features}...")
		MODEL_STRING = "NMF model (Frobenius norm) with tf-idf features"
		t_0 = time()
		nmf = NMF(n_components=self.n_components, random_state=1,
				  alpha=.1, l1_ratio=.5).fit(self.tfidf)
		print(f"done in {time()-t_0:.2f}s.")
		tfidf_feature_names = self.tfidf_vectorizer.get_feature_names()
		boomchicka = nmf.transform(self.tfidf)
		boomchicka = boomchicka.mean(0)
		self._write_topics(nmf, boomchicka, MODEL_STRING, tfidf_feature_names, self.n_top_words)

		# Fit the NMF model
		print(f"Fitting the NMF model (generalized Kullback-Leibler divergence) with tf-idf features, n documents={len(self.corpus)} and n features={self.n_features}...")
		MODEL_STRING = "NMF model (generalized Kullback-Leibler divergence) with tf-idf features"
		t_0 = time()
		nmf = NMF(n_components=self.n_components, random_state=1,
				  beta_loss='kullback-leibler', solver='mu', max_iter=1000, alpha=.1,
				  l1_ratio=.5).fit(self.tfidf)
		print(f"done in {time()-t_0:.2f}s.")
		tfidf_feature_names = self.tfidf_vectorizer.get_feature_names()
		boomchicka = nmf.transform(self.tfidf)
		boomchicka = boomchicka.mean(0)
		self._write_topics(nmf, boomchicka, MODEL_STRING, tfidf_feature_names, self.n_top_words)

	def fit_LDA(self):
		print(f"Fitting LDA models with tf features, n_samples={len(self.corpus)} and n_features={self.n_features}...")
		MODEL_STRING = "LDA models with tf features"
		MODEL_STRING_2 = "LDA models with probabilities"
		lda = LatentDirichletAllocation(n_components=self.n_components, max_iter=5,
										learning_method='online',
										learning_offset=50.,
										random_state=0)
		t_0 = time()
		lda.fit(self.tf)
		print(f"done in {time()-t_0:.2f}s.")
		tf_feature_names = self.tf_vectorizer.get_feature_names()
		boomchicka = lda.transform(self.tf)
		boomchicka = boomchicka.mean(0)
		self._write_topics(lda, boomchicka , MODEL_STRING, tf_feature_names, self.n_top_words)
		self.plot_bar(boomchicka)
	
	def plot_bar(self, df):
	#This function plots a Barplot when supplied with a numpy matrix.

		objects = ('Topic 1', 'Topic 2', 'Topic 3', 'Topic 4', 'Topic 5', 'Topic 6', 'Topic 7', 'Topic 8')
		y_pos = np.arange(len(objects))
	 
		plt.bar(y_pos, df*100, align='center', alpha=0.5)
		plt.xticks(y_pos, objects)
		plt.ylabel('Probability in Percentage %')
		plt.title('Probability of Different Topic Occurance')
		plt.savefig('foo.png')

if __name__ == "__main__":

	if "final.txt" in os.listdir("results"):
		os.remove("results/final.txt")
		
	if len(sys.argv) < 2:
		file = sys.stdin.readlines()
		district = Fitter("File read in by user", file, topics = 8)
		print("Locked and loaded...")
		# Fit Non-negative Matrix
		#district.fit_NMF()
		# Fit Latent Dirichlet allocation
		district.fit_LDA()
	else:
		files = sys.argv[1]
		files = [file for file in os.listdir(files) if file.endswith(".json") or file.endswith(".txt")]
		for file in files:
			with open(sys.argv[1] + file, "r", encoding = 'UTF8') as infile:
				corpus = json.load(infile)

			filename = os.path.splitext("path_to_file")[0]
			# extract only text from the dataset of tweets and turning them into list making each a list of tweets
			# initialize the district corpus
			district = Fitter(file, corpus, topics = 8)
			print("Locked and loaded...")
			# Fit Non-negative Matrix
			#district.fit_NMF()
			# Fit Latent Dirichlet allocation
			district.fit_LDA()

