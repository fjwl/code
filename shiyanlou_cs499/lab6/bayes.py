# coding: utf-8
import feedparser
ny=feedparser.parse('http://labfile.oss.aliyuncs.com/courses/499/ny.txt')
sf=feedparser.parse('http://labfile.oss.aliyuncs.com/courses/499/sf.txt')
import re
def loadFromRss(feed):
    data=feed['summary']
    regEx=re.compile('\\W*')
    wordList=regEx.split(data)
    return [tok.lower() for tok in wordList if len(tok) >2]
def createVocabList(docList):
    vocabSet=set([])
    for document in docList:
        vocabSet=vocabSet|set(document)
    return list(vocabSet)
from numpy import *
def bagOfWords2VecMN(vocabList,inputSet):
    returnVec=[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]+=1
    return returnVec
def trainNB0(trainMatrix,trainCategory):
    numTrainDocs=len(trainMatrix)
    numWords=len(trainMatrix[0])
    pAbusive=sum(trainCategory)/float(numTrainDocs)
    p0Num=ones(numWords);p1Num=ones(numWords)
    p0Denom=2.0;p1Denom=2.0
    for i in range(numTrainDocs):
        if trainCategory[i]==1:
            p1Num+=trainMatrix[i]
            p1Denom+=sum(trainMatrix[i])
        else:
            p0Num+=trainMatrix[i]
            p0Denom+=sum(trainMatrix[i])
    p1Vect=log(p1Num/p1Denom)
    p0Vect=log(p0Num/p0Denom)
    return p0Vect,p1Vect,pAbusive
def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
    p1=sum(vec2Clsssify*p1Vec)+log(pClass1)
    p0=sum(vec2classify*p0Vec)+loa(1.0-pClass1)
    if p1>p0:
        return 1
    else:
        return 0
    
def calcMostFreq(vocabList,fullText):
    import operator
    freqDict={}
    for token in vocabList:
        freqDict[token]=fullText.count(token)
    sortedFreq=sorted(freqDict.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedFreq[:30]

def localWords(feed1,feed0):
    import feedparser
    docList=[];classList=[];fullText=[]
    minLen=min(len(feed1['entries']),len(feed0['entries']))
    for i in range(minLen):
        wordList=loadFromRss(feed1['entries'][i])
        docList.append(wordList);fullText.extend(wordList)
        classList.append(1)
        wordList=loadFromRss(feed0['entries'][i])
        docList.append(wordList)
        fullText.extend(wordList);classList.append(0)
    vocabList=createVocabList(docList)
    top30Words=calcMostFreq(vocabList,fullText)
    for pairW in top30Words:
        if pairW[0]in vocabList:vocabList.remove(pairW[0])
    trainingSet=range(2*minLen);testSet=[]
    for i in range(10):
        randIndex=int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat=[];trainClasses=[]
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2VecMN(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam=trainNB0(array(trainMat),array(trainClasses))
    errorCount=0
    for docIndex in testSet:
        wordVector=bagOfWords2VecMN(vocabList,docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam)!=classList[docIndex]:
            errorCount+=1
    print 'the error rate is :',float(errorCount)/len(testSet)
def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
    p1=sum(vec2Classify*p1Vec)+log(pClass1)
    p0=sum(vec2Classify*p0Vec)+log(1.0-pClass1)
    if p1>p0:
        return 1
    else:
        return 0    
localWords(ny,sf)

