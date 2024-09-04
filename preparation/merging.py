import json
import sys

#Merge districts

def merge_districts(text):

	new_data = list(set())

	for district in text:
		with open(f"raw_twitter_data/{district}_raw.json","r") as file:
			data = json.load(file)
			dataset = data["text"]
			print(f"Number of tweets in {district} is ", len(dataset))
			for tweet in dataset:
					new_data.append(tweet)

	print(f"Number of tweets in merged file is ", len(new_data))

	with open(f"raw_twitter_data/{district}.json","w") as file:
		json.dump(new_data,file,default=str,indent=1,sort_keys=True,ensure_ascii=False)

#if __name__ == "__main__":

	#merge_districts(sys.argv[1:])

#Merge years

def merge_years(years):

	new_data = list(set())

	for year in years:
		with open(f"zip/indreby_merged_zip.json_{year}.json","r") as file:
			data = json.load(file)
			print(f"Number of tweets in {year} is ", len(data))
			for tweet in data:
					new_data.append(tweet)

	print(f"Number of tweets in merged file is ", len(new_data))

	with open(f"zip/twitter_recent_10k/indreby_merged_10K.json","w") as file:
		json.dump(new_data,file,default=str,indent=1,sort_keys=True,ensure_ascii=False)

if __name__ == "__main__":

	merge_years(sys.argv[1:])

