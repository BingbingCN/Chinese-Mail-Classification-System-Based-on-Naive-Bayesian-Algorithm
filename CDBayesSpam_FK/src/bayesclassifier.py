#!usr/bin/python
# -*- coding:utf-8 -*-

import os, sys
import math

import jieba
jieba.set_dictionary("dict.txt")
jieba.initialize()

#导入tkinter模块
from tkinter import *
from PIL import ImageTk,Image
import os
from tkinter import filedialog
root = Tk()
root.title('查看文件')
root.geometry('1000x750')  #tkinter基本设置


ABSPATH = os.path.abspath(sys.argv[0])
ABSPATH=os.path.dirname(ABSPATH) + '/'
print(ABSPATH)


def getPofClass(index, word_list):
    #输入类index的贝叶斯训练结果文件
    index_training_path = ABSPATH + 'bayes_training_outcome/' + str(index) + '_bayestraining.txt'
    file_index_training = open(index_training_path, 'r',encoding='UTF-8')
    dic_training = {}   #存储 index_bayestraining.txt 中的 (单词：P)
    training_word_p_list = file_index_training.readlines()
    allwords_fre_allwords_num = training_word_p_list[0].strip() #index_bayestraining.txt的第一行
    allwords_fre = int(allwords_fre_allwords_num[1])    #所有样本的所有单词的词频
    allwords_num = int(allwords_fre_allwords_num[0])    #所有样本的所有单词个数
    for i in range(1, len(training_word_p_list)):
        word_p = training_word_p_list[i].strip().split(',')
        dic_training[word_p[0]] = float(word_p[1])

    #遍历测试样本的wordlist，求每个Word的p
    p_list = []
    for word in word_list:
        word = word.strip()
        if word in dic_training:
            p_list.append(str(dic_training[word]))
        else:
            p_list.append(str(1.0 / (allwords_fre + allwords_num)))
    #计算P
    p_index = 0
    for p in p_list:
        p = math.log(float(p), 2)
        p_index = p_index + p
    return -p_index


def bayes(text):
    #rightIndex = int(filename.split('_')[0])
    #分词
    text = text.replace('腾讯科技', '')
    text = text.replace('腾讯财经', '')
    text = text.replace('腾讯体育', '')
    text = text.replace('腾讯汽车', '')
    text = text.replace('腾讯娱乐', '')
    text = text.replace('腾讯房产', '')
    text = text.replace('人民网', '')
    text = text.replace('新华网', '')
    text = text.replace('中新网', '')
    text = text.replace(' ', '')
    text = "".join(text.split())
    word_list = jieba.cut(text, cut_all=False)
    
    #停用词
    stopword_path = ABSPATH + 'data/stop.txt'
    file_stopword = open(stopword_path, 'r',encoding='UTF-8')
    stopword_list = file_stopword.readlines()
    for i in range(0, len(stopword_list)):
        word = stopword_list[i].strip()
        stopword_list[i] = word

    #去停用词
    word_list_nostop = []
    for word in word_list:
        word = word.strip()
        if word in stopword_list:
            pass
        else:
            word_list_nostop.append(word)



    #print(word_list_nostop)
    #求每个类index的p
    max = 0
    maxIndex = 0
    for index in range(1, 8):
        y = getPofClass(index, word_list_nostop)
        #print str(index) + ':' + str(y)
        if y != float("inf") and y > max:
            max = y
            maxIndex = index
    return maxIndex


#从本地文件获取文本内容
def getTextFromNative(filepath):
    #输入测试样本
    test_file_path = filepath
    file_test = open(test_file_path, 'r',encoding='UTF-8')
    text = file_test.read()
    return text


#测试本地文件
def nativeTest():

    dir_path = 'data/test/'
    #dir_path = os.path.join(os.path.dirname())
    file_list = os.listdir(dir_path)
    all_count = 0
    right_count = 0
    index_all_count = 0
    index_right_count = 0
    file_outcome = open(ABSPATH + 'outcome/outcome_native.txt', 'w',encoding='UTF-8')
    for filename in file_list:
        #去除隐藏文件
        a = filename.split('.')
        if a[1] == 'txt':
            all_count = all_count + 1
            index_all_count = index_all_count + 1
            b = filename.split('_')
            rightIndex = int(b[0])
            text = getTextFromNative(filename)
            getIndex = bayes(text)
            if getIndex == rightIndex:
                print(filename + '----' + str(getIndex) + ' : right')
                right_count = right_count + 1
                index_right_count = index_right_count + 1
            else:
                print(filename + '----' + str(getIndex) + ' : error')

            if index_all_count == 100:
                string = str(index_right_count) + ' / ' + str(index_all_count) + ' = ' + str(float(index_right_count) / index_all_count)
                print(string)
                file_outcome.write(string + '\n')
                index_all_count = 0
                index_right_count = 0

    string = str(right_count) + ' / ' + str(all_count) + ' = ' + str(float(right_count) / all_count)
    print(string)
    file_outcome.write(string)
    file_outcome.close()


#tkinter框架
fm1 = Frame(root)
fm2 = Frame(root)
fm3 = Frame(root)
fm4 = Frame(root)
fm5 = Frame(root)
#框架放置
fm1.pack()
fm2.pack(anchor='w',pady=20)
fm3.pack(anchor='w',pady=20)
fm4.pack(anchor='w',pady=20)
fm5.pack(anchor='w',pady=20)
#标签图片1
img = Image.open('BGP.png')
photo = ImageTk.PhotoImage(img)
thelabel = Label(fm1,image=photo)
thelabel.pack()

#浏览文件 查看路径
def file_select():
    global file_path
    file_path = filedialog.askopenfilename()
    thetext1.delete(1.0,'end')
    thetext1.insert(1.0,file_path)

b1 = Button(fm2,text='选择文件',width=20,height=2,command=file_select,bg='lightgreen',fg='white')
b1.pack(side='left',padx=100)
thetext1 = Text(fm2,font=('Fixedsys',15),width=40,height=3,bg='lightblue')
thetext1.pack(side='left',padx=50)

#分类
def detect_oneTime(filepath):
    return bayes(getTextFromNative(filepath))

#分类结果
def classify_res():
    num1 = detect_oneTime(file_path)
    if num1 == 1:
        return '财经'
    elif num1 == 2:
        return '科技'
    elif num1 == 3:
        return '汽车'
    elif num1 == 4:
        return '房产'
    elif num1 == 5:
        return '体育'
    elif num1 == 6:
        return '娱乐'
    else:
        return '其他'

var1 = StringVar() #分类结果
var2 = StringVar() #保存结果
var3 = StringVar() #删除结果
var1.set('  ')
var2.set('  ')
var3.set('  ')
def classify_insert():
    str = classify_res()
    var1.set('该新闻的分类为: ' + str +'类')

b2 = Button(fm3,text='分类结果',width=20,height=2,command=classify_insert,bg='lightgreen',fg='white')
b2.pack(side='left',padx=100)
thelabel2 = Label(fm3,textvariable=var1,width=20,height=2,bg='lightblue')
thelabel2.pack(side='left',padx=50)

#记录结果
def file_check():
    f = open('information_path.txt', 'r',encoding='UTF-8')
    text = f.readlines()
    s = []
    for line in text:
        s.append(line[0:-6])
    #print(s)
    if file_path in s:
        #print('存在')
        return False
    else:
        #print('不存在')
        return True
    f.close()

def file_save():
    num2 = detect_oneTime(file_path)
    res = file_check()
    #print(res)
    if res == False:
        var2.set('结果已存在')
    elif res == True:
        f = open('information_path.txt','a',encoding='UTF-8')
        f.write(file_path + ' :  ' + str(num2) + '\n')
        var2.set('完成')
        f.close()

b3 = Button(fm4,text='保存结果',width=20,height=2,command=file_save,bg='lightgreen',fg='white')
b3.pack(side='left',padx=100)
thelabel3 = Label(fm4,textvariable=var2,width=20,height=2,bg='lightblue')
thelabel3.pack(side='left',padx=50)

#显示分类结果

#删除
def file_del():
    res = file_check()
    #print(res)
    if res == True:
        var3.set('结果不存在')
    elif res == False:
        f = open('information_path.txt','r',encoding='UTF-8')
        text = f.readlines()
        #print(text)
        for i in range(len(text)):
            if text[i][0:-6] == file_path:
                del text[i]
                break
        f.close()
        f = open('information_path.txt','w',encoding='UTF-8')
        for i in range(len(text)):
            f.write(text[i])
        f.close()
        var3.set('完成')

b4 = Button(fm5,text='删除结果',width=20,height=2,command=file_del,bg='lightgreen',fg='white')
b4.pack(side='left',padx=100)
thelabel4 = Label(fm5,textvariable=var3,width=20,height=2,bg='lightblue')
thelabel4.pack(side='left',padx=50)




mainloop()




