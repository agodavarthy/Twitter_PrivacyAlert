import os
import re
import sys
import json
import time

family_keywords = ['marriage', 'married', 'marry', 'wife', 'husband', 'dad', 'mom', 'father', 'mother', 'parent', 'kid']
religion_keywords = ['christian', 'muslim', 'hindu', 'religion', 'atheist', 'religious', 'god']
sexual_orientation_keywords = ['gay', 'lesbian', 'hetero', 'heterosexual', 'bisexual']
nationality_keywords = ['american', 'indian', 'asian' 'european', 'african', 'mexican', 'chinese', 'japanese']
profession_keywords = ['scientist', 'researcher', 'professor', 'engineer' 'doctor', 'actor', 'sports', 'teacher', 'politician']

file_line_cnt = 0
family_info_cnt = 0
religion_info_cnt = 0
nationality_info_cnt = 0
profession_info_cnt = 0

def search_terms(desc, keyword_list):
	desc = '.' + desc.lower() + '.'
        for kw in keyword_list:
		restr = '\\W(' + kw + ')\\W'
                searchObj = re.search(restr, desc) 
		if searchObj:
			return True

def extract(line):
	start_ind = line.find("id")
	line = line[start_ind+len("id")+1:]
	end_ind = line.find(", ")
	userid = line[:end_ind]
	start_ind = line.find("description")
	line = line[start_ind+len("description")+2:]
	end_ind = line.find("', ")
	desc = line[:end_ind]
	if desc == 'null':
		desc = ''
	return userid, desc	
#inputpath = "./twitter/UserProfiles/"
'''inputpath = "/data/shared/twitter/ScreenName1to1M/UserProfiles/"
outputpath = "/data/shared/twitter/ScreenName1to1M/DataToAnalyze/"
outputfilename = "FamilyinfoUserIDs.txt"'''
inputpath = "/data/shared/twitter/UOIUserProfiles/profile/"
outputpath = "/data/shared/twitter/UOIUserProfiles/DataToAnalyze/"
outputfilename = "SexualOrientationinfoUserIDsUOI.txt"
outputfd = open(outputpath+outputfilename, 'w')


'''*Note ; for marital negate single word'''

cnt = 0
#filenames = ['10001to15000__11_7_14_49', '15001to20000__11_7_14_50', '1to5000__11_6_22_29', '20001to25000__11_7_14_50', '5001to10000__11_6_22_30']
for filename in os.listdir(inputpath):
	  filepath = inputpath+filename 
	  fd = open(filepath, 'r')
	  for line in fd.readlines():
		file_line_cnt += 1
		user_id, desc = extract(line)
		user_id = filename.strip('.ascii')
		desc = desc.lower()
		if(search_terms(desc, sexual_orientation_keywords)):
		    	#if desc.find("single") < 0:	
			#print user_id
			print desc
			print "********************"
			outputfd.write(str(user_id)+"\n")
			family_info_cnt += 1
		#else:
			#print user_id
			#print desc
			#print "********************"
			#outputfd.write(user_id+"\n")	'''
			#cnt += 1
			#if cnt > 15000:
			#	sys.exit(1)
		'''if(search_terms(desc, religion_keywords)):
			religion_info_cnt += 1
		if(search_terms(desc, nationality_keywords)):
			nationality_info_cnt += 1
		if(search_terms(desc, profession_keywords)):
			profession_info_cnt += 1'''

  	  fd.close()
outputfd.close()
print family_info_cnt, " out of ", file_line_cnt, " have family related info"
#print religion_info_cnt, " out of ", file_line_cnt, " have religion related info"
#print nationality_info_cnt, " out of ", file_line_cnt, " have nationality related info"
#print profession_info_cnt,==  " out of ", file_line_cnt, " have profession related info"
