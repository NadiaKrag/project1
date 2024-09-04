import json
import sys

def drop_dupl(file):

	with open(file,"r") as file:
		dataset = json.load(file)
		data = dataset["text"]
	
	print(f"Length of original dataset for {file} is: ",len(data))

	no_dupl = set()

	for tweet in data:
		no_dupl.add(tweet)

	print(f"Length of no duplicates is: ",len(no_dupl))

	#print(no_dupl)

	my_list = list(no_dupl)

	#print(my_list)

if __name__ == "__main__":

	drop_dupl(sys.argv[1])