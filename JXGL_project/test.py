import tkinter
import tkinter.messagebox








# window = tkinter.Tk()
# window.title('My Window')
# # 宽x高
# window.geometry('500x500')

# 变量
# var = tkinter.StringVar()

# 标签
# l = tkinter.Label(window, textvariable=var, bg='green', font=('Arial', 12), width=30, height=2)
# l.pack()
# on_hit = False
# def hit_me():
#     global on_hit
#     if on_hit == False:
#         on_hit = True
#         var.set('you hit me')
#     else:
#         on_hit = False
#         var.set('')

# 按钮
# b = tkinter.Button(window, text='hit me', font=('Arial', 12), width=10, height=1, command=hit_me)
# b.pack()

# 输入框
# e1 = tkinter.Entry(window, show='*', font=('Arial', 14))   # 显示成密文形式
# e2 = tkinter.Entry(window, show=None, font=('Arial', 14))  # 显示成明文形式
# e1.pack()
# e2.pack()

# Text窗口部件
# e = tkinter.Entry(window, show=None)#显示成明文形式
# t = tkinter.Text(window, height=3)
# e.pack()
# def insert_point(): # 在鼠标焦点处插入输入内容
#     var = e.get()
#     t.insert('insert', var)
# def insert_end():   # 在文本框内容最后接着插入输入内容
#     var = e.get()
#     t.insert('end', var)
# b1 = tkinter.Button(window, text='insert point', width=10,
#                height=2, command=insert_point)
# b1.pack()
# b2 = tkinter.Button(window, text='insert end', width=10,
#                height=2, command=insert_end)
# b2.pack()
# t.pack()

# Listbox窗口部件
# var1 = tkinter.StringVar()  # 创建变量，用var1用来接收鼠标点击具体选项的内容
# l = tkinter.Label(window, bg='green', fg='yellow', font=('Arial', 12), width=10, textvariable=var1)
# l.pack()
# # 第6步，创建一个方法用于按钮的点击事件
# def print_selection():
#     value = lb.get(lb.curselection())  # 获取当前选中的文本
#     var1.set(value)  # 为label设置值
# # 第5步，创建一个按钮并放置，点击按钮调用print_selection函数
# b1 = tkinter.Button(window, text='print selection', width=15, height=2, command=print_selection)
# b1.pack()
# # 第7步，创建Listbox并为其添加内容
# # var2 = tkinter.StringVar()
# # var2.set((1, 2, 3, 4))  # 为变量var2设置值
# # var2 = (1, 2, 3, 4)  # 不行
# # 创建Listbox
# lb = tkinter.Listbox(window, listvariable=var2)  # 将var2的值赋给Listbox
# # 创建一个list并将值循环添加到Listbox控件中
# list_items = [11, 22, 33, 44]
# for item in list_items:
#     lb.insert('end', item)  # 从最后一个位置开始加入值
# lb.insert(1, 'first')  # 在第一个位置加入'first'字符
# lb.insert(2, 'second')  # 在第二个位置加入'second'字符
# lb.delete(2)  # 删除第二个位置的字符
# lb.pack()

# Radiobutton窗口部件
# var = tkinter.StringVar()  # 定义一个var用来将radiobutton的值和Label的值联系在一起.
# l = tkinter.Label(window, bg='yellow', width=20, text='empty')
# l.pack()
# # 第6步，定义选项触发函数功能
# def print_selection():
#     l.config(text='you have selected ' + var.get())
# # 第5步，创建三个radiobutton选项，其中variable=var, value='A'的意思就是，当我们鼠标选中了其中一个选项，把value的值A放到变量var中，然后赋值给variable
# r1 = tkinter.Radiobutton(window, text='Option A', variable=var, value='A', command=print_selection)
# r1.pack()
# r2 = tkinter.Radiobutton(window, text='Option B', variable=var, value='B', command=print_selection)
# r2.pack()
# r3 = tkinter.Radiobutton(window, text='Option C', variable=var, value='C', command=print_selection)
# r3.pack()

# Checkbutton窗口部件
# l = tkinter.Label(window, bg='yellow', width=20, text='empty')
# l.pack()
# # 第6步，定义触发函数功能
# def print_selection():
#     if (var1.get() == 1) & (var2.get() == 0):  # 如果选中第一个选项，未选中第二个选项
#         l.config(text='I love only Python ')
#     elif (var1.get() == 0) & (var2.get() == 1):  # 如果选中第二个选项，未选中第一个选项
#         l.config(text='I love only C++')
#     elif (var1.get() == 0) & (var2.get() == 0):  # 如果两个选项都未选中
#         l.config(text='I do not love either')
#     else:
#         l.config(text='I love both')  # 如果两个选项都选中
# # 第5步，定义两个Checkbutton选项并放置
# var1 = tkinter.IntVar()  # 定义var1和var2整型变量用来存放选择行为返回值
# var2 = tkinter.IntVar()
# c1 = tkinter.Checkbutton(window, text='Python', variable=var1, onvalue=1, offvalue=0,
#                     command=print_selection)  # 传值原理类似于radiobutton部件
# c1.pack()
# c2 = tkinter.Checkbutton(window, text='C++', variable=var2, onvalue=1, offvalue=0, command=print_selection)
# c2.pack()

# Frame 窗口部件
# tkinter.Label(window, text='on the window', bg='red', font=('Arial', 16)).pack()  # 和前面部件分开创建和放置不同，其实可以创建和放置一步完成
# # 第5步，创建一个主frame，长在主window窗口上
# frame = tkinter.Frame(window)
# frame.pack()
# # 第6步，创建第二层框架frame，长在主框架frame上面
# frame_l = tkinter.Frame(frame)  # 第二层frame，左frame，长在主frame上
# frame_r = tkinter.Frame(frame)  # 第二层frame，右frame，长在主frame上
# frame_l.pack(side='left')
# frame_r.pack(side='right')
# # 第7步，创建三组标签，为第二层frame上面的内容，分为左区域和右区域，用不同颜色标识
# tkinter.Label(frame_l, text='on the frame_l1', bg='green').pack()
# tkinter.Label(frame_l, text='on the frame_l2', bg='green').pack()
# tkinter.Label(frame_l, text='on the frame_l3', bg='green').pack()
# tkinter.Label(frame_r, text='on the frame_r1', bg='yellow').pack()
# tkinter.Label(frame_r, text='on the frame_r2', bg='yellow').pack()
# tkinter.Label(frame_r, text='on the frame_r3', bg='yellow').pack()

# messageBox窗口部件
# def hit_me():
#     tkinter.messagebox.showinfo(title='Hi', message='你好！')  # 提示信息对话窗
#     # tkinter.messagebox.showwarning(title='Hi', message='有警告！')       # 提出警告对话窗
#     # tkinter.messagebox.showerror(title='Hi', message='出错了！')         # 提出错误对话窗
#     # print(tkinter.messagebox.askquestion(title='Hi', message='你好！'))  # 询问选择对话窗return 'yes', 'no'
#     # print(tkinter.messagebox.askyesno(title='Hi', message='你好！'))     # return 'True', 'False'
#     # print(tkinter.messagebox.askokcancel(title='Hi', message='你好！'))  # return 'True', 'False'
# # 第4步，在图形界面上创建一个标签用以显示内容并放置
# tkinter.Button(window, text='hit me', bg='green', font=('Arial', 14), command=hit_me).pack()

# 窗口部件三种放置方式pack/grid/place
# 1. Grid
# for i in range(3):
#     for j in range(3):
#         tkinter.Label(window, text=1).grid(row=i, column=j, padx=10, pady=10, ipadx=10, ipady=10)

# 2. Pack
# tkinter.Label(window, text='P', fg='red', bg='red').pack(side='top')    # 上
# tkinter.Label(window, text='P', fg='red', bg='red').pack(side='bottom') # 下
# tkinter.Label(window, text='P', fg='red', bg='red').pack(side='left')   # 左
# tkinter.Label(window, text='P', fg='red', bg='red').pack(side='right')  # 右

# 3. Place
# tkinter.Label(window, text='Pl', font=('Arial', 20), ).place(x=50, y=100, anchor='nw')
# window.destroy()
# t1=tkinter.Toplevel(window)
# t1.title("Top窗口")
# t1.geometry("100x100")
# label=tkinter.Label(t1,text="用户名:")
# label.pack()
# slider=tkinter.Scale(window,from_=0,to=100)
# slider.pack()
# scrollbar = tkinter.Scrollbar()
# scrollbar.pack(side='right')
# window.mainloop()