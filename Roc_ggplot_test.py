'''
Created on Dec 9, 2015

@author: archana
'''
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from edu.scu.infolab.privacyalert import bunchcreator
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from sklearn import svm

import sys
import json
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import pandas as pd
from ggplot import *


def main():
    fpath_train = "/Users/archana/Desktop/PhD/Code/PrivacyAlert/data/CurrentProcessingFiles/FinalProductionFiles/TestTrainData/MaritalTrainData.txt"
    bunch_train = bunchcreator.LoadFileAsBunch(fpath_train, ["NoMarital", "Marital"])
    fpath_test = "/Users/archana/Desktop/PhD/Code/PrivacyAlert/data/CurrentProcessingFiles/FinalProductionFiles/TestTrainData/MaritalTestData.txt"
    bunch_test = bunchcreator.LoadFileAsBunch(fpath_test, ["NoMarital", "Marital"])

    print("Done with Bunching");
    
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(bunch_train.data)

    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    X_test_counts = count_vect.transform(bunch_test.data)
    X_test_tfidf = tfidf_transformer.transform(X_test_counts)
    print "Done with TFIDF"
    clf = LogisticRegression()
    clf.fit(X_train_tfidf, bunch_train.target)
    
    preds_int = clf.predict(X_test_tfidf)
    preds_float = clf.decision_function(X_test_tfidf)
    y_true = np.array(bunch_test.target)
    filepath = "/Users/archana/Desktop/PhD/Code/PrivacyAlert/data/CurrentProcessingFiles/FinalProductionFiles/OutputFiles/GT_Pred.txt"
    fw = open(filepath, 'w')
    for i in range(len(bunch_test.target)):
        fw.write(str(bunch_test.target[i])+":"+str(preds_int[i])+":"+str(preds_float[i])+"\n")

    fpr, tpr, _ = metrics.roc_curve(y_true, preds_float)
    
    plt.figure()
    plt.plot(fpr, tpr, label='ROC curve ' )
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()
if __name__ == "__main__":
    main()      