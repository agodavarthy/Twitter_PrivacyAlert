import json
import time
import sys
import re

def pruneTextSelfModules(tweet):
	new_words = [] 
	words = re.split(' |\n|\t', tweet)
	for word in words:
		#if re.match('http', word):
		#	print word
		
		if not re.match('@', word) and not re.match('http', word):
			#print word
			new_words.append(word)
		
	str1 = ' '.join(new_words)
	return str1 

def retainTopFreqTerms(content, topFreqTerms):
        new_words = []
        words = re.split(' |\n|\t', content)
        for word in words:
                if word in topFreqTerms: 
                        new_words.append(word)

        str1 = ' '.join(new_words)
        return str1	

def buildFreqTerms(fd):
	terms_list = []
	for line in fd:
		term = line.split(" = ")[0]
		#term = line.strip()
		terms_list.append(term)
	return terms_list
if not sys.argv[1]:
	print "Please enter the input file"
	sys.exit(1)

if not sys.argv[2]:
	print "Please enter the output file"
	sys.exit(1)


inputfile = sys.argv[1]
outputfile = sys.argv[2]
target_id = sys.argv[3]
target_name = sys.argv[4]
path = '/Users/archana/Desktop/PhD/Code/PrivacyAlert/data/CurrentProcessingFiles/FinalProductionFiles/'
fd1 = open(path+inputfile, 'r')
fd2 = open(path+outputfile, 'w')
#fd3 = open(path+terms_input_file, 'r')
#topFreqTerms = buildFreqTerms(fd3)
for line in fd1:
	jsonObj = json.loads(line)
	tweet = jsonObj["tweet_doc"]
	user_id = jsonObj["user_id"]
	modified_tweet = pruneTextSelfModules(tweet.encode('ascii', 'ignore'))
	#modified_tweet = retainTopFreqTerms(tweet.encode('ascii', 'ignore'), topFreqTerms)
	obj = {"user_id":user_id, "tweet_doc": modified_tweet, "target_id": target_id, "target_name": target_name}
	json.dump(obj, fd2)
	fd2.write("\n")
fd1.close()
fd2.close()
	

