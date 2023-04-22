from flask import Flask, render_template, request, flash

app = Flask(__name__)

#测试算法需要
import jieba
from handWriting_bayes.LoadData import *
from handWriting_bayes.bayes import *

@app.route('/recog', methods=['POST'])
def recog():
    # request.form 能获取到输入的数据
    # 传回的两个参数，message为短信内容，algorithm_name为1时使用第一种算法，2时使用第二种。
    print("recog()", request.form['message'], "***")
    print("recog()", request.form['algorithm_name'], "***")
    # 模拟使用算法
    messList = jieba.lcut(request.form['message'], cut_all=False)
    '''
    jieba 是 python 中的中文分词第三方库，可以将中文的文本通过分词获得单个词语，返回类型为列表类型。

    jieba 分词共有三种模式：精确模式、全模式、搜索引擎模式。

    （1）精确模式语法：jieba.lcut(字符串,cut_all=False)，默认时为cut_all=False,表示为精确模型。精确模式是把文章词语精确的分开，并且不存在冗余词语，切分后词语总词数与文章总词数相同。

    （2）全模式语法：ieba.lcut(字符串,cut_all=True)，其中cut_all=True表示采用全模型进行分词。全模式会把文章中有可能的词语都扫描出来，有冗余，即在文本中从不同的角度分词，变成不同的词语。

    （3）搜索引擎模式：在精确模式的基础上，对长词语再次切分。
    '''
    # jieba.lcut 直接返回 list   
    print("***",messList)
    # 构建词向量
    receVec = word2Vec(vocabList, messList)
    
    print('*********** word2Vec ***********')
    if classifyNB(array(receVec), p0V, p1V, pSpam) == 1:
        print("识别为垃圾短信")
        return "识别为垃圾短信"
    else:
        print("识别为正常短信")
        return "识别为正常短信"

@app.route('/')
def index():
    print("index()")
    return render_template('index.html')


if __name__ == '__main__':
    # 以下代码测试算法的初始化过程
    postingList, classVec = loadData()
    vocabList = createVocabList(postingList)
    # print("test test test")
    # vocabList 是中文词汇表
    trainMat = []  # 训练数据矩阵。[[1,0,0,1,0,1],[0,1,1,0,0,1],[1,1,0,0,1,1]]
    n = 0 
    for doc in postingList:
        n += 1
        if n % 1000 == 0:
            print('doc2Vec',n)
        trainMat.append(word2Vec(vocabList, doc)) # 某条短信对应的词向量

    p0V,p1V,pSpam = trainNB(array(trainMat), array(classVec))
    # 以下代码 Flask 必需
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
    #外部可访问。  app.run() #外部不可访问
