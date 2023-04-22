import jieba
import re
from LoadData import *
from bayes import *
from sklearn.metrics import accuracy_score,f1_score,classification_report,precision_score
import numpy as np


postingList,classVec = loadData()
vocabList = createVocabList(postingList)

trainMat = []  #训练数据矩阵。[[1,0,0,1,0,1],[0,1,1,0,0,1],[1,1,0,0,1,1]]
n = 0 
for doc in postingList:
	n += 1
	if n % 1000 == 0:
		print('doc2Vec',n)
	trainMat.append(word2Vec(vocabList, doc)) #某条短信对应的词向量
p0V,p1V,pSpam = trainNB(array(trainMat), array(classVec))

testSet,testClass = testLoadData()
errorCount = 0 ; n = 0

pred_list=[]

for doc in testSet:
	if n % 1000 == 0:
		print('doc2Vec',n)
	testVec = word2Vec(vocabList, doc)
	pred_list.append(classifyNB(array(testVec), p0V, p1V, pSpam))
	if classifyNB(array(testVec), p0V, p1V, pSpam) != testClass[n]:
		errorCount += 1
		print(testClass[n],'----',doc)
	n += 1
np.savetxt('pred.txt',pred_list)
np.savetxt('real.txt',testClass)

print(classification_report(testClass,pred_list))


print('errorCount:',errorCount)
