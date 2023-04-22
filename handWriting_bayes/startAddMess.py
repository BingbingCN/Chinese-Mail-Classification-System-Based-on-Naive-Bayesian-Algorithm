import jieba
import re
import socket
import threading
import time
from LoadData import *
from bayes import *


def tcplink1(sock1, addr1):
	print('22 Accept new connection from %s:%s...' % addr1)
	# addr是tuple ('127.0.0.1', 56610)
	f = open('/Users/apple/Desktop/整理/计算机视觉/代码/MailClassify/data/addMess.txt','a+')
	#追加读写模式
	if f:
		print('open addMess.txt file succeed')
	recvString1 = sock1.recv(10240)
	f.write(recvString1+'\n')
	f.close()
	#print str(m).decode('string_escape')
	print(recvString1) #显示编码，无法正确显示中文
	sock1.close()
	print('Connection from %s:%s closed.' % addr1)

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#创建TCP,IPv4的Socket
s1.bind(('0.0.0.0', 6464))
#绑定端口
s1.listen(10)
#监听端口，指定等待连接的最大数量5
print('Waiting for connection...')
while True:
	sock1, addr1 = s1.accept()
	#接收一个新连接
	t1 = threading.Thread(target=tcplink1, args=(sock1, addr1))
	#创建新线程处理TCP连接
	t1.start()

