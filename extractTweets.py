import json
import os
import sys

def main():
	arg1 = sys.argv[1]
	arg2 = sys.argv[2]
	arg3 = sys.argv[3]
	if(arg3 = "0"):
		target_id = 0
		target_name = "marital_neg"
	else if (arg3 == "1"):
		target_id = 1
		target_name = "marital_pos"
	path = "/data/shared/twitter/UOIUserProfiles/tweets/NegSamples/"+arg1+"/"
	outpath = "/data/shared/twitter/UOIUserProfiles/tweets/LuceneInputDocs/"
	fd3 = open(outpath+"MasterLuceneInput"+arg2+".json", 'a')
	id_set = set()
	for filename in os.listdir(path):
		complete_path = path+filename
		fd = open(complete_path, 'r')
		for line in fd.readlines():
			jsonObj = json.loads(line)
			user_id = jsonObj["user_id"]
			if user_id not in id_set:
				id_set.add(user_id)
				tweet_doc = ""
				tweets = jsonObj["tweets"]
				tweet_cnt = len(tweets)
				print user_id, ":", len(tweets)
				if tweet_cnt > 1000: 
					for tweet in tweets:
						tweet_txt = tweet["text"]
						tweet_doc += tweet_txt + " "
						 
					obj = {}
					obj["user_id"] = user_id
					obj["tweet_doc"] = tweet_doc
					obj["target_id"] = target_id
					obj["target_name"] = target_name
					json.dump(obj, fd3, ensure_ascii=True)
					fd3.write("\n")
				print "**********"
		fd.close()
	fd3.close()
main()
