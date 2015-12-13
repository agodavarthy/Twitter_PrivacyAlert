import tweepy
import json
import time
import sys
import os
import re
import pymongo
from pymongo import MongoClient

auth_keys_list = [
       	{"cust_key":"6taGCp7HzLyDmms4wwbOqDdmO","cust_secret":"4fTmvQEy4vcL4hDgKe9zc1fMIG2aArLFUXHGNPUSBCVwiqXcHs","access_key":"4209262152-huA29ViWEKptn8NAmdywtC0rJtKn13HYcSZsCsk","access_secret":"gZgcUE8k1WnGIkU1tRvjSiCGJQBDJ3Cazwvk9k4i2eBTt"},
	{"cust_key":"1hY1D5BMWEFKXoZNr67k5AVle","cust_secret":"LsbLFs6Jmsf2Rvdq1qjBBHqT4tvVfezT3C7Q2OdOfnyy4R6GkL","access_key":"4209262152-2LuyC3uk3p5557hatdT1RkhD5SEHbNFqpseRzPn","access_secret":"EIoHfhoWz6pcfEqsK1CjawLfvUw0Jr0lIMg8uTMKTBIBh"},
	{"cust_key":"jt8RTBLULVZ4HwXxQVjcnpDwu","cust_secret":"u75Q4LPR80TYwtsfsXaI9Gp2GPBSNmaISPOwDSO62hqK3x6N89","access_key":"290705256-Zn4YGV8pNfE0wogX5AOZMGa3iZpRwB0ZMn5Te8Kr","access_secret":"9S81krhaq1uEggSonKPlEIc0QStSMHo0IYcWCU6QMB33L"},
	{"cust_key":"gyQgQDV7qT87OREQPFGNnNpnE","cust_secret":"dUZDoC05XFdHXyF4Cw6StyT5fo2vqOMxnBfNTsnupYoYwn6dg3","access_key":"290705256-Yha8gIFc55FUC6kKcagpa6MVJcohskGTGPeWQpbR","access_secret":"fJpcv8CH2lVabJni0bzCfmYxKATwZC7jCTREI3PcFNxoB"},
	{"cust_key":"L2AY5XDc1MbVunIH4QeNt0Gkt","cust_secret":"M5WXorm54j8eahaCvdhKynqaTC2lIJ4tbs556VKJD5Pu69IlNV","access_key":"290705256-0i4UFUG404prhYRbllDwwivKqiuqxh1ISOTwn8aR","access_secret":"hTVyT6ikPigIBHnIcQaYcbluNj04gLSsqnJbG7oTvpqp7"},
	{"cust_key":"qD97vtupfpZW9fmsKzuHGL57c","cust_secret":"dEctMX1uBLXv4KXLo4MxPfMObiT7kRKhbaOcULXQ2n8V41cPXd","access_key":"4209262152-fMUvJr3gMXCG92QL8qbKv56y0tx51WyMjhEfSKs","access_secret":"XjYLgrwct4hmQDGeZS5n0jnYt40tZ55p7ebabf8Kr7qcs"}
]

def get_access_tokens(list_key):
    list_index = list_key - 1
    print list_index
    auth = tweepy.OAuthHandler(auth_keys_list[list_index]["cust_key"], auth_keys_list[list_index]["cust_secret"]) # consumerkey, consumersecret
    auth.set_access_token(auth_keys_list[list_index]["access_key"],auth_keys_list[list_index]["access_secret"]) # accesstoken, accesstokensecret
    return tweepy.API(auth), auth 

def get_time_stamp():
    ts = "_"+str(time.localtime().tm_mon)+'_'+str(time.localtime().tm_mday)+'_'+str(time.localtime().tm_hour)+'_'+str(time.localtime().tm_min)
    return ts

def get_user_tweets(user_id, api):
    print "Getting user tweets...."
    user_tweets_obj = tweepy.Cursor(api.user_timeline, id=user_id, count=10000) 
    return user_tweets_obj

def writeTweets2File(user_id, user_tweets_obj, outfile_fd):
    complete_obj = {}
    complete_obj["user_id"] = user_id
    tweet_list = []
    tweet_cnt = 0
    for tweet in user_tweets_obj.items():
	obj = {}
	tweet_cnt += 1
        obj['tweet_id'] = tweet.id
        obj['text'] = tweet.text
        obj['in_reply_to_status_id'] = tweet.in_reply_to_status_id
        obj['retweet_count'] = tweet.retweet_count
        obj['retweeted'] = tweet.retweeted
        obj['source'] = tweet.source
        obj['lang'] = tweet.lang
        obj['entities'] = tweet.entities
	tweet_list.append(obj)
    print "user_id = ", user_id
    print "#tweets = ", len(tweet_list)
    complete_obj['tweets'] = tweet_list
    complete_obj['tweets_cnt'] = len(tweet_list)
    if len(tweet_list) > 1000:
	    json.dump(complete_obj, outfile_fd, ensure_ascii=True)
	    outfile_fd.write("\n")

def main():
          auth_set = int(sys.argv[1])
	  input_fileno = sys.argv[2]
	  
	  if(auth_set < 1 or auth_set > 20):
		print "Auth key:", auth_set, " is invalid"
		sys.exit(1)
	  api, auth = get_access_tokens(auth_set)
	  print 'Using the auth set %d' % auth_set
	  ts = get_time_stamp()
	  path = "/data/shared/twitter/UOIUserProfiles/"
	  input_filename = "DataToAnalyze/NegSamples/NoMaritalUniqueIDs_"+input_fileno+".txt" 
	  input_user_profile_fd = open(path+input_filename, 'r')
	  output_filename = "tweets/NegSamples/tweets_"+input_fileno+"_"+ts+".json" 
	  output_user_profile_fd = open(path+output_filename, 'w')
         
	  for line in input_user_profile_fd.readlines():
		try:
			user_id = line.strip()
			user_tweets_obj = get_user_tweets(user_id, api)
			writeTweets2File(user_id, user_tweets_obj, output_user_profile_fd) 
			time.sleep(60)
		except tweepy.error.TweepError as e:
			reason = e.reason 
			if reason == "Rate limit exceeded":
				print user_id, ":", reason 
				time.sleep(600)
				
			else:
				print user_id, ":",reason 
				time.sleep(60)
			pass
		except pymongo.errors.DuplicateKeyError as pe:
			print "pymongo duplicate error:", user_id
			pass	
	  output_user_profile_fd.close()

main()

