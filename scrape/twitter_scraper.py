from twitterscraper import query_tweets
import datetime as dt
import json
import sys
import itertools

if __name__ == "__main__":

    district = sys.argv[1]

    list_of_tweets = query_tweets(district, 
        begindate=dt.date(2008,1,1), 
        enddate=dt.date.today(), 
        poolsize=20)

    dict_of_tweets = dict()
    dict_of_tweets["user"] = list(set())
    dict_of_tweets["timestamp"] = list(set())
    dict_of_tweets["text"] = list(set())

    for i in range(len(list_of_tweets)):
        dict_of_tweets["user"].append(list_of_tweets[i].user)
        dict_of_tweets["timestamp"].append(str(list_of_tweets[i].timestamp))
        dict_of_tweets["text"].append(list_of_tweets[i].text)

    time_text_list = tuple(zip(dict_of_tweets["timestamp"],dict_of_tweets["text"]))

    print("Found " + str(len(dict_of_tweets["text"])) + f" tweets for {district}.json")
    print(f"Found {len(time_text_list)} tweets for {district}_zip.json")

    with open(f"raw_twitter_data/{district}.json","w",encoding="utf8") as file:
        json.dump(dict_of_tweets,file,default=str,indent=1,sort_keys=True,ensure_ascii=False)

    with open(f"raw_twitter_data/{district}_zip.json","w",encoding="utf8") as file:
        json.dump(time_text_list,file,default=str,indent=1,sort_keys=True,ensure_ascii=False)