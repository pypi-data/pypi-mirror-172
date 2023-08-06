#Import Library and Modules
import time
import os, os.path
from os import listdir
from os.path import isfile, join
import numpy as np
import pandas as pd 
import sys
import re
import random
from Bio import SeqIO
from Bio import Entrez
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import StratifiedKFold
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score,balanced_accuracy_score
from sklearn.metrics import confusion_matrix
import warnings
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
warnings.filterwarnings('ignore')

###############################################
def Change_DNA(dna):
    line = "".join(dna.split("\n")[1:])
    dna = line.upper()
    return dna
###############################################
def PC_mer(dna, k):    
    vector = k #Determining the length of three vectors {weak or strong}, {amino or keto} and {purine or pyrimidine} based on k-mer size==>2^k
    start = vector // 2
    x = start

    weakStrong = [0] * (vector) #CG , AT
    aminoKeto = [0] * (vector) #AC , GT
    PurPyr = [0] * (vector) #AG , CT

    #weak or strong
    for i in range(len(dna)):
        if dna[i] == "C" or dna[i] == "G":
            x = (x + vector) // 2
            weakStrong[x] = weakStrong[x] + 1 
        
        elif dna[i] == "A" or dna[i] == "T":
            x = (x + 0) // 2
            weakStrong[x] = weakStrong[x] + 1

    x = start
    #amino or keto       
    for i in range(len(dna)):
        if dna[i] == "C" or dna[i] == "A":
            x = (x + vector) // 2
            aminoKeto[x] = aminoKeto[x] + 1 
        
        elif dna[i] == "G" or dna[i] == "T":
            x = (x + 0) // 2
            aminoKeto[x] = aminoKeto[x] + 1

    x = start
    #purine or pyrimidine
    for i in range(len(dna)):
        if dna[i] == "C" or dna[i] == "T":
            x = (x + vector) // 2
            PurPyr[x] = PurPyr[x] + 1 
        
        elif dna[i] == "A" or dna[i] == "G":
            x = (x + 0) // 2
            PurPyr[x] = PurPyr[x] + 1

    arr = np.concatenate((PurPyr, aminoKeto, weakStrong))
    return arr
###############################################
def GFL(mypath):
    ffolders = []
    dna = []
    label = []
    # define Dataset path
    mypath = mypath
    my_list = os.listdir(mypath)
                
    for i in range(len(my_list)):
        path = mypath + "\\" + my_list[i]
        s = os.listdir(path)
        n = len(s)
        
        for j in range(n):
            path1 = path + "\\" + s[j]
            f = open(path1 , "r")
            line = f.read()
            f.close()
            line = Change_DNA(line)
            x = PC_mer(line)
            dna.append(x)
            label.append(i) 
    return dna, label 
###############################################

def get_metrics(y_test, y_predicted):
    precision = precision_score(y_test, y_predicted, average='weighted')
    recall = recall_score(y_test, y_predicted, average='weighted')
    f1 = f1_score(y_test, y_predicted, average='weighted')
    acc=accuracy_score(y_test, y_predicted)
    return precision, recall, f1, acc
###############################################

def perf_measure(y_actual, y_hat):
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    for i in range(len(y_hat)): 
        if y_actual[i]==y_hat[i]==1:
           TP += 1
        if y_hat[i]==1 and y_actual[i]!=y_hat[i]:
           FP += 1
        if y_actual[i]==y_hat[i]==0:
           TN += 1
        if y_hat[i]==0 and y_actual[i]!=y_hat[i]:
           FN += 1   
    sen = TP / (TP+FN)
    spec = TN / (TN+FP)
    return(sen , spec)
###############################################

def comp_confmat(actual, predicted):
    classes = np.unique(actual) # extract the different classes
    matrix = np.zeros((len(classes), len(classes))) # initialize the confusion matrix with zeros
    for i in range(len(classes)):
        for j in range(len(classes)):
            matrix[i, j] = np.sum((actual == classes[i]) & (predicted == classes[j]))
    return matrix

###############################################
def pcmer_api(fname,seqid):
    Entrez.email = "https://pubmed.ncbi.nlm.nih.gov/"  
    filename = fname
    if not os.path.isfile(filename):
        # Downloading...
        net_handle = Entrez.efetch(
            db="nucleotide", id=seqid, rettype="fasta", retmode="text"
        )
        out_handle = open(filename, "w")
        out_handle.write(net_handle.read())
        out_handle.close()
        net_handle.close()
        print("Saved")

    print("Parsing...")
    record = SeqIO.read(filename, "fasta")
    print(record)
