#Coding by Lishuzheng.

import os
import time
import socket
import tkinter
import random
import threading
import hashlib
import tkinter.filedialog

#发送模块
def sending(cli):
    try:
        send_data =  T_input.get("1.0","end")
        send_addr = send_data.split("@",1)[0]#地址部分
        send_msg = send_data.split("@",1)[1].replace("\n", "")#消息部分
        send_ip = send_addr.split(":")[0]#ip地址
        send_port = send_addr.split(":")[1]#端口地址
        send_name = socket.gethostbyaddr(send_ip)#将接收ip -> 主机名
        nowtime = "[" + time.strftime('%H:%M:%S', time.localtime()) + "]"
        cli.sendto(send_msg.encode("gbk"), (send_ip, int(send_port)))
        send_output = nowtime + "本机" + " > " + str(send_name[0]) + "：" + send_msg + "\n"
        history.append(send_output)
        T_show.config(state = "normal")
        T_show.insert("end", send_output)
        T_show.yview_moveto(1)
        T_show.update()
        T_show.config(state = "disabled")
    except socket.gaierror:
        T_show.config(state = "normal")
        T_show.insert("end", "错误：地址错误或不存在(0x01)\n")
        T_show.yview_moveto(1)
        T_show.update()
        T_show.config(state = "disabled")
    except IndexError:
        T_show.config(state = "normal")
        T_show.insert("end", "错误：输入不完整(0x02)\n")
        T_show.yview_moveto(1)
        T_show.update()
        T_show.config(state = "disabled")
    except socket.herror:
        T_show.config(state = "normal")
        T_show.insert("end", "错误：远程主机没有响应(0x03)\n")
        T_show.yview_moveto(1)
        T_show.update()
        T_show.config(state = "disabled")
    
#接收模块（后台进程）
def recvfrom(cli):
    while True:
        time.sleep(1)
        recv_data = cli.recvfrom(1024)#接收总信息
        recv_msg = recv_data[0].decode("gbk")#消息解码
        recv_name = socket.gethostbyaddr(recv_data[1][0])[0]#发送ip -> 主机名
        nowtime = "[" + time.strftime('%H:%M:%S', time.localtime()) + "]"
        recv_output = nowtime + recv_name + " > " + "本机" + "：" + str(recv_msg) + "\n"
        history.append(recv_output)
        T_show.config(state = "normal")
        T_show.insert("end", recv_output)
        T_show.yview_moveto(1)
        T_show.update()
        T_show.config(state = "disabled")

#清空T_show
def clear():
    T_input.delete("1.0", "end")

#保存历史
def savehistory():
    filew = tkinter.filedialog.asksaveasfilename(title = '保存', initialfile = '', filetypes = [('文本文件', '*.txt')])
    print(filew)
    if os.path.exists(filew + ".txt"):
        os.remove(filew)
    if os.path.exists(filew + ".md5"):
        os.remove()
    with open(filew + ".txt", "a") as f:
        f.write("日期：" + nowdate + "\n")
        f.write("用户名：" + myself_name)
        for i in history:
            f.write(i)
    with open(filew + ".txt", 'rb') as fs:
        data = fs.read()
    md5 = hashlib.md5(data).hexdigest()
    with open(filew + ".md5", "a") as fm:
        fm.write(md5)

#tkinter窗口
root = tkinter.Tk()
root.title("LANCOM")
root.geometry("300x240")
root.wm_attributes('-topmost', 1)
root.resizable(0, 0)
#组件：两个按钮, 一个文本框, 一个菜单栏
B1 = tkinter.Button(root, text ="     发送    ", height = 2, bd = 0, bg = "white", command = lambda: sending(cli))
B1.place(x = 215, y = 151)
B2 = tkinter.Button(root, text ="     清空    ", height = 2, bd = 0, bg = "white", command = clear)
B2.place(x = 215, y = 195)
T_show = tkinter.Text(root, width = 43, height = 11, bd = 3)
T_show.pack()
T_input = tkinter.Text(root, width = 30, height = 6, bd = 4)
T_input.place(x = 0, y = 151)
#绑定滚动条
scroll = tkinter.Scrollbar()
scroll.pack(side=tkinter.RIGHT,fill=tkinter.Y)
scroll.config(command = T_show.yview)
T_show.config(yscrollcommand=scroll.set, state = "disabled")
#菜单栏
menubar = tkinter.Menu(root)
menubar.add_command(label='历史记录', command = savehistory)
menubar.add_command(label='退出', command = root.quit)
root.config(menu=menubar)

#定义接收ip, 端口, 日期, 历史记录，socket接口
myself_name = socket.gethostname()
recv_ip =  socket.gethostbyname(myself_name)
recv_port = random.randrange(1025,65536)
nowdate = time.strftime("%Y-%m-%d", time.localtime())
history = []
cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cli.bind(('', recv_port))

#显示初始化信息
T_show.config(state = "normal")
T_show.insert("end", 41*"-" + "LANCOM 网络通讯框架\n版本号：v1.1.13_Beta" + "\n时间：" + nowdate + "\nipv4地址：" + recv_ip + "\n端口号：" + str(recv_port) + "\n格式：ipv4地址:端口号@发送内容\n" + 41*"-" + "\n")
T_show.config(state = "disabled")

#接收进程
recv_threading = threading.Thread(target=recvfrom,args=(cli,))
recv_threading.daemon = True
recv_threading.start()

#保持窗口
root.mainloop()