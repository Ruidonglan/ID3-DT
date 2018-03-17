# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 20:26:23 2018

@author: nmlan
"""
def predNewDataM(myTree, labels , testVec):
    
    
    fstStr  = list(myTree.keys())[0]
    
    if type(myTree[fstStr]) == str:
        finallabel = myTree[fstStr]
        return(finallabel)
    
    if len(fstStr) > 3:#if its larger than 3, we have a real value here:
        temp1,temp2 = fstStr.split(" ")
        
        sdnDic = myTree[fstStr]
        
        featIndex = labels.index(temp1)
        
        for key in sdnDic:# 对于数值型的，下一步有两种情况，0 或者 1 ，所以我们
            #要判断是0 还是 1 并且它的下一个是什么类型：
            if eval( str( testVec[featIndex] ) + temp2) == key:
                if type(sdnDic[key]) == dict:
                    finallabel = predNewDataM(sdnDic[key] , labels ,testVec)
                else:
                    finallabel = sdnDic[key]
                    
    else:#else, we have a str value here: 
        sdnDic = myTree[fstStr]
        featIndex = labels.index(fstStr)
        for key in sdnDic:
            if testVec[featIndex] == key:
                if type(sdnDic[key]) == dict:
                    finallabel = predNewDataM(sdnDic[key], labels , testVec)
                else:
                    finallabel = sdnDic[key]
    return(finallabel)



data2 = arff.load(open('credit_test.arff', 'r'))
data_test = data2['data']
labels2 = data2['attributes']
newlabels2 = [exampel[0] for exampel in labels2]
newlabels2 = newlabels2[0:len(newlabels2)-1]

real =[]
pred =[]
for each in data_test:
    test = each[:-1]
    real.append(each[-1])
    temp = predNewDataM(tree10 , newlabels ,test)
    pred.append(temp)
    real2 = each[-1]
    print(real2,temp)
    
    
n= 0
for i in range(len(real)):
    if real[i] == pred[i]:
        n+=1
total = len(real)
acc = float(n)/total
print(acc)






