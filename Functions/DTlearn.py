# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from math import log
import copy
import arff

def calEn(data_train):
    total = len(data_train)#the number of the total examples
    labels = {} #the label dict,where the value of each label is the total number of it.
    for instance in data_train:
        in1 = instance[-1]
        if in1 not in labels.keys():
            labels[in1] = 1
        else:
            labels[in1] += 1     
    en = float(0) # the entropy of this dataset
    for in2 in labels:
        p = labels[in2]/float(total)
        en -= p * log(p,2)
    return(en)
    
    
def dataSplit(dataset, feature , value):
    # in this function, the feature is given by the number in it
    # the first argument is the position, the second one is the value for this point
    newdata = []
    for example in dataset:
            if example[feature] == value:
                temp = example[:feature]
                temp.extend(example[feature+1:])
                newdata.append(temp) #this step will append the newdata
    return(newdata)


def helpNum(numlist):
    #unique first and then do the sort thing
    #numlist = list(set(numlist))
    numlist.sort()
    l = len(numlist)
    midpoints = []
    for i in range(1,l):
        midpoints.append( (numlist[i-1]+numlist[i])/2  )
    return(midpoints)


def dataSplitNum(data_train, feature , mid ):
    #this function will return the data splited by the given numerical feature:
    newdataLow = []
    newdataHigh = []
    for example in data_train:
        if example[feature] <= mid: #watch this point, we need to do the <=
            temp = copy.copy(example)
            newdataLow.append(temp)
        else:
            temp2 = copy.copy(example)
            newdataHigh.append(temp2)
    return(newdataLow,newdataHigh) 
    
  
    
def bestNumMid(data_train, label):
    # the total entropy before the split
    all_ent = calEn(data_train)
    values = [example[label] for example in data_train]
    midvalues = helpNum(values)
    #do the entropy calculation:
    infoGain = 0.0
    resultpoint = None
    l = len(midvalues)
    for i in range(l):
        mid = midvalues[i]
        temp_en = 0.0
        new1, new2 = dataSplitNum(data_train, label , mid)
        prob1 = len(new1)/ float(len(data_train))
        prob2 = len(new2)/ float(len(data_train))
        temp_en += prob1*calEn(new1)
        temp_en += prob2*calEn(new2)
        temp_infoGain = all_ent - temp_en
        if(temp_infoGain  > infoGain):
            resultpoint = mid
            infoGain = temp_infoGain
    return(resultpoint,infoGain)


def findBestsplit(data_train):
    # the total entropy before the split
    all_ent = calEn(data_train)
    # the total number of features
    fe_len = len(data_train[0])-1
    infoGain = float(0)
    result_feature = None
    midvaluefornumeric = None
    for i in range(fe_len):
        #print(infoGain)
        temp_entropy = float(0)
        feat = data_train[0][i]
        if type(feat) == float: #or type(feat) == int
            temp_midvalue,temp_infoGain = bestNumMid(data_train ,i )
            if(temp_infoGain > infoGain):
                infoGain = temp_infoGain
                result_feature = i
                midvaluefornumeric = temp_midvalue           
        elif type(feat) == str:
            featurelist = []
            for example in data_train:
                if example[i] in featurelist:
                    pass
                else:
                    featurelist.append(example[i])       
            for feature in featurelist:
                kset = dataSplit(data_train , i , feature )
                prob = len(kset)/float(len(data_train))
                temp_entropy += prob * calEn(kset)
            temp_infoGain = all_ent - temp_entropy
            if (temp_infoGain > infoGain): # Since we only change the reslut_feature if it's equal and smaller,thus, this will work
                infoGain = temp_infoGain
                result_feature = i
                midvaluefornumeric = None
    return(result_feature , midvaluefornumeric)



def MakeNode(classes):
    # this fucntion will return a dict which will take the majoity of this class to be the node
    #create a dict to store the node
    number = {}
    for each in classes:
        if each in number:
            number[each] +=1
        else:
            number[each] =1
    #sort the dict by their number:
    new_number = sorted(number.items(), key = lambda item:item[1], reverse = True)
    return(new_number[0][0])
    
    
def MakeTreeM(data_train , labels , m = 5):
    classes = [example[-1] for example in data_train]# the calsssse of the dataset
    
    #If data_set all belong to one class   ##or we have fewer than m instances
    
    if classes.count(classes[0]) == len(classes): #or len(data_train) < m:
        return(classes[0])
        
    elif  len(data_train[0]) ==1: # if there is no more classes, make a node here
        return(MakeNode(classes))
    
    elif  len(data_train) < m :  #if the data left is less than 5, make a node here
        return(MakeNode(classes))
        
    else:
        S , M = findBestsplit(data_train)
        
        if S is None:
            return(MakeNode(classes))
            
        if M is None:
            Node_Name = labels[S]
        else:
            Node_Name = labels[S] + ' <=' + str(M)
        
        Tree = {Node_Name:{}}
        
        if M is None:
            
            S_values = [example[S] for example in data_train]
            
            uniqueS_values = set(S_values)
            
            del(labels[S]) 
            
            for each in uniqueS_values:
                Dnew = dataSplit(data_train , S , each)
                nextlabels = labels[:]
                Tree[Node_Name][each] = MakeTreeM(Dnew , nextlabels)
                
        elif M is not None:
            Dnew = dataSplitNum(data_train , S , M)
            for i in range(2):
                Dnew_temp = Dnew[i]
                newlables = labels[:]
                Tree[Node_Name][i] = MakeTreeM( Dnew_temp , newlables)
    return(Tree)
    
    
    
################################################
#debugging time:

data = arff.load(open('credit_train.arff', 'r'))
data_train = data['data']
labels = data['attributes']
newlabels = [exampel[0] for exampel in labels]
newlabels = newlabels[0:len(newlabels)-1]

tree1 = MakeTreeM(data_train , newlabels)