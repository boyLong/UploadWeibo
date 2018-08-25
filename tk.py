from tkinter import *
from confing import Config
from main import run
from utlis.utils import log
import traceback


class App:
    def __init__(self, master, ):
        self.conf = Config()
        self.config = self.conf.config
        self.fm1 = Frame(master)
        self.type_id = 0
        self.account = Entry(self.fm1,width=30)
        self.account_msg = "已经有的账号\n"+self.conf.read_account()
        self.account.grid(row=1, column=0, sticky=W)
        self.account_add = Button(self.fm1, text='添加账号和密码，请按照竖线分割', command=self.account_add_write).grid(
            row=1, column=1, sticky=W)
        s1 = Scrollbar(self.fm1)
        s1.grid(row=1, column=2, ipady=0, rowspan=2, sticky=NS,),
        self.type_label = Label(self.fm1, text="双击选择视频分类")
        self.type_label.grid(row=0, column=0,)
        self.account_msg_text = Text(self.fm1, yscrollcommand=s1.set, width=60, height=10,)
        self.account_msg_text.grid(row=2, column=0, sticky=W, columnspan=2)
        s1.config(command=self.account_msg_text.yview)
        self.account_msg_text.insert(END, self.account_msg)
        self.type_dict = eval(self.config["type"]["type"])

        self.listbox = Listbox(root)
        self.type_list = list(self.type_dict.keys())
        for i in self.type_list:
            self.listbox.insert(END, i)
        s2 = Scrollbar(self.fm1)
        s2.grid(row=4, column=2, ipady=0, rowspan=2, sticky=NS,),
        self.listbox.pack(fill=X, side=TOP)
        self.listbox.bind('<Double-Button-1>', self.print_list)
        self.status_msg_text = Text(self.fm1,width=60)
        self.status_msg_text.grid(row=4, column=0, sticky=N, columnspan=2)
        self.time = Entry(self.fm1, width=30)
        self.time.grid( row=5, column=0, sticky=W)
        self.type_label = Label(self.fm1, text="输入间隔时间（数字，默认30秒，）")
        self.type_label.grid(row=5, column=1, )
        self.run = Button(self.fm1, text='开始运行', command=self.run_main).grid(
            row=6, column=1, sticky=W)

        self.fm1.pack(side=LEFT, fill=BOTH, expand=YES)

    def print_list(self, event):
        index = self.listbox.curselection()[0]
        self.type_id = self.type_dict[self.type_list[index]]
        self.status_msg_text.insert(END, "选择\t"+self.type_list[index]+"\t类型"+'\n')

    def account_add_write(self):

        account = self.account.get()
        self.conf.write_account(account, type_='a')
        if not account:
            return
        self.account_msg_text.insert(END, account+'\t添加成功' + '\n')
        Scrollbar(self.fm1, orient=HORIZONTAL, command=self.account_msg_text.xview)

    def run_main(self):
        if not self.type_id:
            self.status_msg_text.insert(END, '请双击视频分类\n')
            return
        if self.time.get():

            try:
                time_ = int(self.time.get())
            except:
                self.status_msg_text.insert(END, '请输入数字')
                self.status_msg_text.update()
                return
        else:
            time_ = 30
        try:
            run(self.conf.read_account(type_=False), self.type_id, self.status_msg_text,time_)
        except Exception as e:
            log("error", traceback.format_exc())


if __name__ == '__main__':

    try:
        root = Tk()
        root.title("Pack - Example")
        display = App(root)
        root.mainloop()
    except Exception as e:
        log("error", traceback.format_exc())