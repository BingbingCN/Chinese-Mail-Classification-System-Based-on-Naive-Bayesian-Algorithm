import jieba
import re
trainDataNum = 8000  # 设置训练数据的数量，10w 条时 8G 内存不够
testDataNum = 5000  # 设置测试数据的数量
path_to_testMess = '../data/filterMess.txt'
# 28.8M 一般测试文件小，训练文件大
path_to_trainMess = '../data/带标签短信.txt'
# 58.2M


'''
testLoadData(): 加载test数据，已除去train数据

# testPostingList:数据为list的list，把垃圾短信进行了分词
[['我','最近','在','学车'],['然后','科二','科三','都','挂了'],['是的','都','挂了']]

# testClassVec:一维标签 list，表示 testPostingList 中数据的类型
[1,1,0,0,1,0]
testClassVec length:  5000
testPostingList length:  5000
vocabSet length:  19631

'''

def testLoadData():

	testPostingList = []; testClassVec = []
	try:
		f = open(path_to_testMess,'r', encoding='utf-8')
		n = 0
		if not f:
			print('open file failed~')
			raise ValueError('open file failed~')
		print('open file succeed~')
		while n < trainDataNum:  
			n = n + 1
			line = f.readline()
		n = 0
		while n < testDataNum:
			n = n + 1
			line = f.readline()
			m = re.split('\t',line)  #返回list
			# m:  ['0', '飞机机身上喷的是“淘宝网”字样\n']
			# print('m:', m) #显示编码
			flag = int(m[0])  # str -> int 标签
			mess = m[1]  # str类型 短信内容 
			messList = jieba.lcut(mess,cut_all=False) # 短信分词
			# messlist:  ['飞机', '机身', '上', '喷', '的', '是', '“', '淘宝网', '”', '字样', '\n']
			# jieba.lcut 直接返回list	
			if(n % 1000 == 0):
				print('testLoadData：',n)
			
			# print('messlist: ', messList) #一条短信分词的list,没处理
			testPostingList.append(messList) # 收集所有短信内容
			testClassVec.append(flag) # 收集所有短信的标签
		# print('testClassVec length: ', len(testClassVec))
		# print('testPostingList length: ', len(testPostingList)) #print postingList
	finally:
		if f:
			f.close()
	return testPostingList, testClassVec


'''
LoadData(): 加载train数据

# PostingList:数据为list的list，把垃圾短信进行了分词
[['我','最近','在','学车'],['然后','科二','科三','都','挂了'],['是的','都','挂了']]

# ClassVec:一维标签list，表示testPostingList中数据的类型
[1,1,0,0,1,0]

classVec length:  8000
postingList length:  8000
vocabSet length:  24552

'''

def loadData():

	postingList = []; classVec = []
	try:
		f = open(path_to_trainMess,'r', encoding='utf-8')
		n = 0
		if f:
			print('open file succeeed')
		while n < trainDataNum:  
			n = n + 1
			line = f.readline()
			m = re.split('\t',line)  # 返回list
			# print('m: ', m) # 显示编码
			flag = int(m[0])  # str -> int
			mess = m[1]  #str类型
			messList = jieba.lcut(mess,cut_all=False)
			if(n % 1000 == 0):
				print('loadData',n)
			# print(str(messList).decode('string_escape'))
			# print('messlist: ', messList) # 一条短信分词的list, 没处理
			postingList.append(messList)
			classVec.append(flag)
		# print('classVec length: ', len(classVec))
		# print('postingList length: ', len(postingList)) #print postingList
	finally:
	# 	if f:
	# 		f.close()
		return postingList,classVec

'''
createVocabList(dataSet):构建词向量列表

# dataSet:loadData() 函数返回的 postingList
[['我','最近','在','学车'],['然后','科二','科三','都','挂了'],['是的','都','挂了']]

# vocabSet:一维list，表示PostingList中所有词的集合
['我','最近','在','学车','然后','科二','科三','都','挂了','是的']

'''

def createVocabList(dataSet):
	vocabSet = set([])
	n = 0
	for doc in dataSet:
		n += 1
		# 并集，取两集合全部的元素
		vocabSet = vocabSet | set(doc)
		if n % 1000 == 0:
			print('createVocabList',n)
	return list(vocabSet)

'''
word2Vec(vocabList, inputSet): 把分词后的短信转化为词向量

#vocabList:createVocabList函数返回的vocabSet
vocabSet:一维list，['我','最近','在','学车','然后','科二','科三','都','挂了','是的']

#inputSet:分词后的短信list。可以是postingList中的一个元素。
['我','最近','在','学车']

returnVec:一维list，为词向量。
[1,1,0,0,1,0]
'''

def word2Vec(vocabList, inputSet):
	returnVec = [0]*len(vocabList) #与词汇表等长的list
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)] += 1
			# returnVec从0开始
		#else:
		#	print "the word: %s is not in my Vocabulary!" % word
	return returnVec  #list 类型

##### test code ##### 
# postingList, classVec = loadData() 
# vocabSet = createVocabList(postingList) # vocabSet是词汇表
# print('vocabSet length: ', len(vocabSet))

# for doc in postingList:
# 	print(word2Vec(vocabSet, doc),'ooc') #某条短信对应的词向量
# 	#returnVec
