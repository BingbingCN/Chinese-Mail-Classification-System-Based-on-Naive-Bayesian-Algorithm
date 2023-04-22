from tkinter import *
import threading
import random
import os
import ttss as bc
class Control():
    def __init__(self,master,start_train,single,data_read):
        self.parent = master
        self.parent.title('贝叶斯文本分类器')
        # self.parent.geometry('1000x1000')
        self.title = Label(self.parent,text='贝叶斯文本分类器',font=20)
        self.title.pack()
        self.frame = Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=3,pady=20)
        self.parent.resizable(width=False, height=False)

        self.var2 = StringVar()
        self.var2.set('训练状态:未训练')
        self.labelb2 = Label(self.frame, textvariable=self.var2)
        self.labelb2.grid(row=0,rowspan=1, column=1, sticky=W + E)

        self.var = StringVar()
        self.var.set('随机读取')
        self.stBtn = Button(self.frame, textvariable=self.var, width=10,command=data_read)
        self.stBtn.grid(row=0, rowspan=1,column=2, sticky=N+S)
        self.label3 = Label(self.frame, text="邮件信息")
        self.label3.grid(row=2, column=0, sticky=E)
        self.text = Text(self.frame, width=60, height=10,font=('Arial',10))
        self.text.grid(row=2, column=1, columnspan=3,sticky=W)



        self.stBtn1 = Button(self.frame, text='开始训练', width=10, height = 2,command=start_train)
        self.stBtn1.grid(row=0, rowspan=1, column=0, sticky=N+S)

        self.var1 = StringVar()
        self.var1.set('邮件类别')
        self.labelb1 = Label(self.frame,textvariable=self.var1)
        self.labelb1.grid(row=3,rowspan=2,column=1,sticky=W+E)
        self.stBtn2 = Button(self.frame, text='邮件分类', width=10, command=single)
        self.stBtn2.grid(row=3, rowspan=1, column=0, sticky=N + S)


class ThreadClient():
    def __init__(self, master):
        self.master = master
        self.gui = Control(master,self.start_train,
                   self.single,self.data_read)  # 将我们定义的GUI类赋给服务类的属性，将执行的功能函数作为参数传入

    def start_train(self):
        bc.train()
        self.gui.var2.set('训练状态:已训练')

    def single(self):
        data = self.gui.text.get(1.0,END)
        with open("temp", "w") as f:  # 打开文件
            f.write(data)
        res = bc.single_test()
        if res == 1:
            self.gui.var1.set('垃圾邮件')
        else:
            self.gui.var1.set('正常邮件')

    def data_read(self):
        self.gui.text.delete(1.0, END)
        dirs = os.listdir("../data/test")
        file_len = len(dirs)
        rand_int = random.randint(1, file_len)
        with open("../data/test/"+str(dirs[rand_int]), "r") as f:  # 打开文件
            data = f.readlines()  # 读取文件
            for line in data:
                self.gui.text.insert('end',line)


    # 为方法开一个单独的线程
    def starting(self):
        self.thread = threading.Thread(target=self.data_read)
        self.thread.start()


if __name__ == '__main__':
    root = Tk()
    ThreadClient(root)# 注意这句
    mainloop()



