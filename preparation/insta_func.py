#read in files as ususal. i.e.:
#import json
#with open('filename.json' , 'r') as f1, open('filename2.json' , 'r') as f2:
    #hasht = json.load(f1, encoding='utf-8')
    #loca = json.load(f2, encoding='utf-8')


'''Merging while removing duplicates and writing as new file'''

def no_dupl(list1, list2, outfile):   #list1 could be location and list2 hashtags. outfile e.g. 'nørrebro_fil.json'.
	import json
	no_dup=[] 
	for line in list1:
		no_dup.append(line)
	for line in list2:
		if line in no_dup:
			pass
		else:
			no_dup.append(line)
	with open(outfile, 'w') as out:
		json.dump(no_dup, out) 
	print("file with length", len(no_dup), "has been saved as", outfile)


'''Getting the text with hashtags, emojis etc.'''

def gettext(path):                      #returns a list of texts by feeding the path for the json file
	import json
	with open(path , 'r') as f:
		data = json.load(f, encoding='utf-8')

	raw_text = []
	for caption in data:
		try:
			text = caption["edge_media_to_caption"]['edges'][0]['node']['text']
		except IndexError:
			continue
		raw_text.append(text)
	return raw_text

'''Getting only hashtags from the file'''

def gethash(path):                       #returns a list of hashtags by feeding the path for the json file
	import json
	with open(path , 'r') as f:
		data = json.load(f, encoding='utf-8')

	raw_tags = []
	for line in data:
		try:
			hashtag = line.get('tags')
		except IndexError:
			continue
		raw_tags.append(hashtag)
	return raw_tags