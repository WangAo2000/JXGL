import tkinter
import tkinter.messagebox



def create_login_window():
    def login():
        # 获取账号、密码、身份
        student_id = student_id_input.get()
        password = password_input.get()
        choosed_status = login_status()
        # 判断身份
        if choosed_status == '学生':
            # 验证密码
            if student_id == '1' and password == '123456':
                print('登录成功')
                login_window.destroy()
                create_student_index_window()
            else:
                tkinter.messagebox.showerror(title='错误', message='密码或账号不正确')
                password_input.set('')
        if choosed_status == '教师':
            if student_id == '1' and password == '123456':
                print('登录成功')
                login_window.destroy()
                create_teacher_index_window()
            else:
                tkinter.messagebox.showerror(title='错误', message='密码或账号不正确')
                password_input.set('')

    def login_status():
        return status.get()

    # 创建登录窗口
    login_window = tkinter.Tk()
    login_window.geometry('400x250')
    # 输入的变量
    student_id_input = tkinter.StringVar()
    password_input = tkinter.StringVar()
    # 登录的身份
    status = tkinter.StringVar()
    # 默认学生
    status.set('学生')
    # 标题
    title = tkinter.Label(login_window, text='教务管理系统登录', font=('宋体', 12))
    # 创建存放的容器
    f = tkinter.Frame(login_window)
    # 标签
    student_id_label = tkinter.Label(f, text='账号：')
    password_label = tkinter.Label(f, text='密码：')
    # 输入框
    student_id_entry = tkinter.Entry(f, textvariable=student_id_input)
    password_entry = tkinter.Entry(f, show='*', textvariable=password_input)
    # 登录按钮
    login_button = tkinter.Button(f, text='登录', command=login)
    # 单选框
    student = tkinter.Radiobutton(f, text='学生', variable=status, value='学生', command=login_status)
    teacher = tkinter.Radiobutton(f, text='教师', variable=status, value='教师', command=login_status)

    # 组件摆放
    title.place(x=140, y=30)
    f.place(x=100, y=70)
    student_id_label.grid(row=0, column=0)
    password_label.grid(row=2, column=0)
    student_id_entry.grid(row=0, column=1)
    password_entry.grid(row=2, column=1)
    student.grid(row=4, column=0, sticky=tkinter.N + tkinter.S)
    teacher.grid(row=4, column=1)
    login_button.grid(row=6, column=0, columnspan=2)

    login_window.mainloop()


def create_student_index_window():
    def update_info():
        pass

    def choose_course():
        print(is_check1.get())

    def add_course():
        pass

    def show_info():
        pass

    student_id = '1'
    student_name = '小明'
    sex = '男'
    professional = '信息管理与信息系统'
    birthday = '2000-9-23'
    index_window = tkinter.Tk()
    index_window.geometry('600x600')

    # 学生信息
    info_frame = tkinter.Frame(index_window)
    info_title = tkinter.Label(info_frame, text='学生信息')
    student_id_label = tkinter.Label(info_frame, text="学号：" + student_id)
    student_name_label = tkinter.Label(info_frame, text="姓名：" + student_name)
    sex_label = tkinter.Label(info_frame, text="性别：" + sex)
    professional_label = tkinter.Label(info_frame, text="专业：" + professional)
    birthday_label = tkinter.Label(info_frame, text="出生日期：" + birthday)
    update_button = tkinter.Button(info_frame, text='修改信息', command=update_info)

    # 学生选课框
    is_check1 = tkinter.StringVar()
    is_check2 = tkinter.StringVar()
    is_check3 = tkinter.StringVar()
    is_check1.set('0')
    is_check2.set('0')
    is_check3.set('0')
    choose_course_frame = tkinter.Frame(index_window)
    choose_course_title = tkinter.Label(choose_course_frame, text='可选课程：')
    cb1 = tkinter.Checkbutton(choose_course_frame, text='高等数学', variable=is_check1, onvalue='高等数学',
                              command=choose_course)
    cb2 = tkinter.Checkbutton(choose_course_frame, text='高等数学', variable=is_check2, onvalue='高等数学',
                              command=choose_course)
    cb3 = tkinter.Checkbutton(choose_course_frame, text='高等数学', variable=is_check3, onvalue='高等数学',
                              command=choose_course)
    choose_course_button = tkinter.Button(choose_course_frame, text='选择课程', command=add_course)

    # 课程信息框
    course_frame = tkinter.Frame(index_window)
    course_title = tkinter.Label(course_frame, text='已选课程')
    course_name = tkinter.Label(course_frame, text='高等数学')
    course_count = tkinter.Label(course_frame, text='60人')
    course_info_button = tkinter.Button(course_frame, text='课程信息', command=show_info)

    # 课程信息布局
    course_frame.place(x=30, y=300)
    course_title.grid(row=0, column=0, sticky=tkinter.W, padx=50)
    course_name.grid(row=1, column=0, sticky=tkinter.W, padx=50)
    course_count.grid(row=1, column=1, sticky=tkinter.W, padx=50)
    course_info_button.grid(row=1, column=2, sticky=tkinter.W, padx=50)

    # 学生信息的布局
    info_frame.place(x=30, y=50)
    info_title.grid(row=0, column=0, sticky=tkinter.W, padx=50)
    student_id_label.grid(row=1, column=0, sticky=tkinter.W, padx=50)
    student_name_label.grid(row=2, column=0, sticky=tkinter.W, padx=50)
    sex_label.grid(row=3, column=0, sticky=tkinter.W, padx=50)
    professional_label.grid(row=1, column=1, sticky=tkinter.W, padx=50)
    birthday_label.grid(row=2, column=1, sticky=tkinter.W, padx=50)
    update_button.grid(row=3, column=2, sticky=tkinter.W, padx=50)

    # 学生选课布局
    choose_course_frame.place(x=80, y=200)
    choose_course_title.grid(row=0, column=0, sticky=tkinter.W)
    cb1.grid(row=1, column=0, sticky=tkinter.W)
    cb2.grid(row=1, column=1, sticky=tkinter.W)
    cb3.grid(row=1, column=2, sticky=tkinter.W)
    choose_course_button.grid(row=1, column=3, sticky=tkinter.W)

    index_window.mainloop()


def create_teacher_index_window():
    def update_info():
        pass

    def choose_course():
        print(is_check1.get())

    def add_course():
        pass

    def show_info():
        create_course_window()

    teacher_id = '1'
    teacher_name = '小明'
    sex = '男'
    professional = '信息管理与信息系统'
    birthday = '2000-9-23'
    index_window = tkinter.Tk()
    index_window.geometry('600x600')

    # 学生信息
    info_frame = tkinter.Frame(index_window)
    info_title = tkinter.Label(info_frame, text='教师信息')
    student_id_label = tkinter.Label(info_frame, text="学号：" + teacher_id)
    student_name_label = tkinter.Label(info_frame, text="姓名：" + teacher_name)
    sex_label = tkinter.Label(info_frame, text="性别：" + sex)
    professional_label = tkinter.Label(info_frame, text="专业：" + professional)
    birthday_label = tkinter.Label(info_frame, text="出生日期：" + birthday)
    update_button = tkinter.Button(info_frame, text='修改信息', command=update_info)

    # 学生选课框
    is_check1 = tkinter.StringVar()
    is_check2 = tkinter.StringVar()
    is_check3 = tkinter.StringVar()
    is_check1.set('0')
    is_check2.set('0')
    is_check3.set('0')
    choose_course_frame = tkinter.Frame(index_window)
    choose_course_title = tkinter.Label(choose_course_frame, text='可选课程：')
    cb1 = tkinter.Checkbutton(choose_course_frame, text='高等数学', variable=is_check1, onvalue='高等数学',
                              command=choose_course)
    cb2 = tkinter.Checkbutton(choose_course_frame, text='高等数学', variable=is_check2, onvalue='高等数学',
                              command=choose_course)
    cb3 = tkinter.Checkbutton(choose_course_frame, text='高等数学', variable=is_check3, onvalue='高等数学',
                              command=choose_course)
    choose_course_button = tkinter.Button(choose_course_frame, text='选择课程', command=add_course)

    # 课程信息框
    course_frame = tkinter.Frame(index_window)
    course_title = tkinter.Label(course_frame, text='已选课程')
    course_name = tkinter.Label(course_frame, text='高等数学')
    course_count = tkinter.Label(course_frame, text='60人')
    course_info_button = tkinter.Button(course_frame, text='课程信息', command=show_info)

    # 课程信息布局
    course_frame.place(x=30, y=300)
    course_title.grid(row=0, column=0, sticky=tkinter.W, padx=50)
    course_name.grid(row=1, column=0, sticky=tkinter.W, padx=50)
    course_count.grid(row=1, column=1, sticky=tkinter.W, padx=50)
    course_info_button.grid(row=1, column=2, sticky=tkinter.W, padx=50)

    # 学生信息的布局
    info_frame.place(x=30, y=50)
    info_title.grid(row=0, column=0, sticky=tkinter.W, padx=50)
    student_id_label.grid(row=1, column=0, sticky=tkinter.W, padx=50)
    student_name_label.grid(row=2, column=0, sticky=tkinter.W, padx=50)
    sex_label.grid(row=3, column=0, sticky=tkinter.W, padx=50)
    professional_label.grid(row=1, column=1, sticky=tkinter.W, padx=50)
    birthday_label.grid(row=2, column=1, sticky=tkinter.W, padx=50)
    update_button.grid(row=3, column=2, sticky=tkinter.W, padx=50)

    # 学生选课布局
    choose_course_frame.place(x=80, y=200)
    choose_course_title.grid(row=0, column=0, sticky=tkinter.W)
    cb1.grid(row=1, column=0, sticky=tkinter.W)
    cb2.grid(row=1, column=1, sticky=tkinter.W)
    cb3.grid(row=1, column=2, sticky=tkinter.W)
    choose_course_button.grid(row=1, column=3, sticky=tkinter.W)

    index_window.mainloop()


def create_course_window():
    course_window = tkinter.Tk()
    course_window.geometry('600x600')
    course_name = tkinter.Label(course_window, text='课程名称：高等数学')
    course_teacher = tkinter.Label(course_window, text='授课教师：小明')
    course_frame = tkinter.Frame(course_window)
    course_info = tkinter.Label(course_frame, text='课程信息')
    student_id = tkinter.Label(course_frame, text='1')
    student_name = tkinter.Label(course_frame, text='小明')
    professional = tkinter.Label(course_frame, text='信息管理与信息系统')

    course_name.place(x=70, y=50)
    course_teacher.place(x=70, y=100)
    course_frame.place(x=20, y=200)
    course_info.grid(row=0, column=0, sticky=tkinter.W, padx=50)
    student_id.grid(row=1, column=0, sticky=tkinter.W, padx=50)
    student_name.grid(row=1, column=1, sticky=tkinter.W, padx=50)
    professional.grid(row=1, column=2, sticky=tkinter.W, padx=50)

    course_window.mainloop()


if __name__ == '__main__':
    create_login_window()
