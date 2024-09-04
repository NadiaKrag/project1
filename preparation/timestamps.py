import sys
import json

def timeline(file,year):

	#print(str(year))

	data_dict = dict(data)

	print("Total amount of tweets for " + file + " is: ", len(data_dict))

	dataset = []
	for time,tweet in data_dict.items():
		if year in time:
			dataset.append(tweet)

	#print(dataset)

	print("Total amount of tweets for " + file + " in " + year + " is: ", len(dataset))

	with open(f"{file}_{year}.json","w",encoding="utf8") as file:
		json.dump(dataset,file,default=str,indent=1,ensure_ascii=False)

if __name__ == "__main__":

	file = sys.argv[1]

	with open(file, "r") as infile:
		data = json.load(infile)

	timeline(file,sys.argv[2])