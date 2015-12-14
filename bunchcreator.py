'''
Created on Nov 30, 2015

@author: archana
'''
import json
from sklearn.datasets.base import Bunch

def LoadFileAsBunch(fpath, target_names):
    """This function takes a file and returns a Bunch"""
    data = []
    filenames = []
    target_ids = []
    target_names = []
    with open(fpath,'r') as fd:
        for line in fd:
            jsonObj = json.loads(line)
            data.append(jsonObj["tweet_doc"])
            filenames.append(jsonObj["user_id"])
            target_ids.append(int(jsonObj["target_id"]))
#     target_names = {target_id: target_name}
    target_names = target_names
    return Bunch(data=data, filenames=filenames, target=target_ids, target_names=target_names)

# def LoadFileAsBunchTest(fpath):
#     """This function takes a file and returns a Bunch"""
#     data = []
#     filenames = []
#     target_ids = []
#     target_names = []
#     with open(fpath,'r') as fd:
#         for line in fd:
#             jsonObj = json.loads(line)
#             data.append(jsonObj["tweet_doc"])
#             filenames.append(jsonObj["user_id"])
# #     target_names = {target_id: target_name}
#     return Bunch(data=data, filenames=filenames)
