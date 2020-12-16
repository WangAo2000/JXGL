# -*- coding: GBK -*-
import tkinter
import tkinter.messagebox
import pymssql


class ConnectDatabase(object):
    def __init__(self, host='localhost', database='JXGL_system', charset='GBK'):
        self.conn = pymssql.connect(host=host, database=database, charset=charset)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            tkinter.messagebox.showerror(title='错误', message='出错了')
            self.conn.rollback()
        try:
            self.conn.commit()
        except Exception:
            self.conn.rollback()
        finally:
            self.cursor.close()
            self.conn.close()


def create_login_window():
    def login():
        # 获取账号、密码、身份
        student_id = student_id_input.get()
        password = password_input.get()
        chosen_status = login_status()
        # 判断身份
        if chosen_status == '学生':
            # 查找数据
            with ConnectDatabase() as cursor:
                sql = "select sno,password from student where sno='%s'" % student_id
                cursor.execute(sql)
                data = cursor.fetchone()
            # 判断数据是否存在
            if data is not None:
                valid_student_id, valid_password = data
                valid_student_id = valid_student_id.strip()
                valid_password = valid_password.strip()
                # 验证密码
                if student_id == valid_student_id and password == valid_password:
                    print('登录成功')
                    login_window.destroy()
                    create_student_index_window(valid_student_id)
                else:
                    tkinter.messagebox.showerror(title='错误', message='密码或账号不正确')
                    password_input.set('')
            else:
                tkinter.messagebox.showerror(title='错误', message='密码或账号不正确')
                password_input.set('')
        if chosen_status == '教师':
            # 查找数据
            with ConnectDatabase() as cursor:
                sql = "select tno,password from teacher where tno='%s'" % student_id
                cursor.execute(sql)
                data = cursor.fetchone()
            # 判断数据是否存在
            if data is not None:
                valid_teacher_id, valid_password = data
                # 去掉多余的空格
                valid_teacher_id = valid_teacher_id.strip()
                valid_password = valid_password.strip()
                # 验证密码
                if student_id == valid_teacher_id and password == valid_password:
                    print('登录成功')
                    login_window.destroy()
                    create_teacher_index_window(valid_teacher_id)
                else:
                    tkinter.messagebox.showerror(title='错误', message='密码或账号不正确')
                    password_input.set('')
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


def create_student_index_window(student_id):
    def update_info():
        index_window.destroy()
        create_student_update_window(student_id)

    def choose_course(x):
        var = v[x].get()
        if var.startswith('d'):
            c_set.remove(var[1:])
        else:
            c_set.add(var)

    def add_course(student_id):
        print(student_id)
        if len(c_set) != 0:
            for cno in c_set:
                with ConnectDatabase() as cursor:
                    sql = "insert student_course values('%s','%s')" % (student_id, cno)
                    cursor.execute(sql)
        index_window.destroy()
        create_student_index_window(student_id)

    # 展示课程信息
    def show_info(x):
        cno = cv[x].get()
        create_course_window(cno)

    # 取消课程
    def delete_course(x):
        cno = cv[x].get()
        with ConnectDatabase() as cursor:
            sql = "delete from student_course where sno={} and cno={}".format(student_id, cno)
            cursor.execute(sql)
        index_window.destroy()
        create_student_index_window(student_id)

    # 获取学生数据
    with ConnectDatabase() as cursor:
        sql = "select * from student where sno='%s'" % student_id
        cursor.execute(sql)
        data = cursor.fetchone()
    student_id = data[0].strip()
    student_name = data[1].strip()
    password = data[2].strip()
    sex = data[3].strip()
    birthday = data[4].strip()
    professional = data[5].strip()
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

    # 学生信息的布局
    info_frame.place(x=30, y=50)
    info_title.grid(row=0, column=0, sticky=tkinter.W, padx=50)
    student_id_label.grid(row=1, column=0, sticky=tkinter.W, padx=50)
    student_name_label.grid(row=2, column=0, sticky=tkinter.W, padx=50)
    sex_label.grid(row=3, column=0, sticky=tkinter.W, padx=50)
    professional_label.grid(row=1, column=1, sticky=tkinter.W, padx=50)
    birthday_label.grid(row=2, column=1, sticky=tkinter.W, padx=50)
    update_button.grid(row=3, column=2, sticky=tkinter.W, padx=50)

    # 查找已有教师的课程
    with ConnectDatabase() as cursor:
        sql = "select * from course where tno is not NULL " \
              "and cno not in (select cno from student_course where sno='%s')" % student_id
        cursor.execute(sql)
        data_list = cursor.fetchall()
    # 学生选课框
    choose_course_frame = tkinter.Frame(index_window)
    choose_course_title = tkinter.Label(choose_course_frame, text='可选课程：')
    choose_course_frame.place(x=80, y=200)
    choose_course_title.grid(row=0, column=0, sticky=tkinter.W)
    # 判断有没有课程选择
    if len(data_list) != 0:
        # 存放已勾选的课程
        c_set = set()
        # 记录次数以及i个变量
        i = 0
        # 存放多个变量
        v = [None] * len(data_list)
        for data in data_list:
            cno = data[0].strip()
            cname = data[1].strip()
            tno = data[2].strip()
            v[i] = tkinter.StringVar()
            # 默认不勾选
            v[i].set('0')
            cb = tkinter.Checkbutton(choose_course_frame, text=cname, variable=v[i], onvalue=cno,
                                     offvalue='d%s' % cno, command=lambda x=i: choose_course(x))
            # 学生选课布局
            cb.grid(row=1, column=i, sticky=tkinter.W)
            i += 1
        choose_course_button = tkinter.Button(choose_course_frame, text='选择课程', command=lambda: add_course(student_id))
        choose_course_button.grid(row=2, column=0, sticky=tkinter.W)
    else:
        none_lable = tkinter.Label(choose_course_frame, text='无')
        none_lable.grid(row=1, column=0)

    # 查询已选课程
    with ConnectDatabase() as cursor:
        sql = "select course.cno,cname from student_course join course on course.cno=student_course.cno where student_course.sno={} ".format(
            student_id)
        cursor.execute(sql)
        course_list = cursor.fetchall()
        print(course_list)

    # 已选课程的插件
    course_frame = tkinter.Frame(index_window)
    course_title = tkinter.Label(course_frame, text='已选课程:')
    course_frame.place(x=30, y=300)
    course_title.grid(row=0, column=0, sticky=tkinter.W, padx=50)
    course_name = tkinter.Label(course_frame, text='课程名')
    count = tkinter.Label(course_frame, text='人数')
    course_name.grid(row=1, column=0, sticky=tkinter.W, padx=50)
    count.grid(row=1, column=1, sticky=tkinter.W, padx=50)

    if len(course_list) != 0:
        j = 0
        cv = [None] * len(course_list)
        for course in course_list:
            cno = course[0].strip()
            course_name = course[1].strip()
            cv[j] = tkinter.StringVar()
            cv[j].set(cno)
            # 查找课程人数
            with ConnectDatabase() as cursor:
                sql = "select count(sno) from student_course where cno={}".format(cno)
                cursor.execute(sql)
                course_count = cursor.fetchone()[0]
            # 课程信息框
            course_name_label = tkinter.Label(course_frame, text=course_name)
            course_count_label = tkinter.Label(course_frame, text=course_count)
            course_info_button = tkinter.Button(course_frame, text='课程信息', command=lambda x=j: show_info(x))
            cancel_button = tkinter.Button(course_frame, text='取消课程', command=lambda x=j: delete_course(x))
            # 课程信息布局
            course_name_label.grid(row=j + 2, column=0, sticky=tkinter.W, padx=50)
            course_count_label.grid(row=j + 2, column=1, sticky=tkinter.W, padx=50)
            course_info_button.grid(row=j + 2, column=2, sticky=tkinter.W, padx=50)
            cancel_button.grid(row=j + 2, column=3, sticky=tkinter.W)
            j += 1

    index_window.mainloop()


def create_teacher_index_window(teacher_id):
    def update_info():
        index_window.destroy()
        create_teacher_update_window(teacher_id)

    def choose_course(x):
        var = v[x].get()
        if var.startswith('d'):
            c_set.remove(var[1:])
        else:
            c_set.add(var)

    def add_course():
        if len(c_set) != 0:
            for cno in c_set:
                with ConnectDatabase() as cursor:
                    sql = "update course set tno={} where cno={};".format(teacher_id, cno)
                    cursor.execute(sql)
        index_window.destroy()
        create_teacher_index_window(teacher_id)

    # 展示课程信息
    def show_info(x):
        cno = cv[x].get()
        create_course_window(cno)

    # 取消课程
    def delete_course(x):
        cno = cv[x].get()
        with ConnectDatabase() as cursor:
            sql = "update course set tno=null where cno={};".format(cno)
            cursor.execute(sql)
        index_window.destroy()
        create_teacher_index_window(teacher_id)

    # 获取教师数据
    with ConnectDatabase() as cursor:
        sql = "select * from teacher where tno='%s'" % teacher_id
        cursor.execute(sql)
        data = cursor.fetchone()
        print(data)
    teacher_id = data[0].strip()
    teacher_name = data[1].strip()
    password = data[2].strip()
    sex = data[3].strip()
    birthday = data[4].strip()
    professional = data[5].strip()
    prof = data[6].strip()
    index_window = tkinter.Tk()
    index_window.geometry('600x600')
    # 教师信息
    info_frame = tkinter.Frame(index_window)
    info_title = tkinter.Label(info_frame, text='教师信息')
    student_id_label = tkinter.Label(info_frame, text="教师号：" + teacher_id)
    student_name_label = tkinter.Label(info_frame, text="姓名：" + teacher_name)
    sex_label = tkinter.Label(info_frame, text="性别：" + sex)
    professional_label = tkinter.Label(info_frame, text="专业：" + professional)
    birthday_label = tkinter.Label(info_frame, text="出生日期：" + birthday)
    prof_label = tkinter.Label(info_frame, text='职称：' + prof)
    update_button = tkinter.Button(info_frame, text='修改信息', command=update_info)

    # 学生信息的布局
    info_frame.place(x=30, y=50)
    info_title.grid(row=0, column=0, sticky=tkinter.W, padx=50)
    student_id_label.grid(row=1, column=0, sticky=tkinter.W, padx=50)
    professional_label.grid(row=1, column=1, sticky=tkinter.W, padx=50)
    student_name_label.grid(row=2, column=0, sticky=tkinter.W, padx=50)
    birthday_label.grid(row=2, column=1, sticky=tkinter.W, padx=50)
    sex_label.grid(row=3, column=0, sticky=tkinter.W, padx=50)
    prof_label.grid(row=3, column=1, sticky=tkinter.W, padx=50)
    update_button.grid(row=3, column=2, sticky=tkinter.W, padx=50)

    # 查找没有教师的课程
    with ConnectDatabase() as cursor:
        sql = "select * from course where tno is null"
        cursor.execute(sql)
        data_list = cursor.fetchall()
    # 学生选课框
    choose_course_frame = tkinter.Frame(index_window)
    choose_course_title = tkinter.Label(choose_course_frame, text='可选课程：')
    choose_course_frame.place(x=80, y=200)
    choose_course_title.grid(row=0, column=0, sticky=tkinter.W)
    # 判断有没有课程选择
    if len(data_list) != 0:
        # 存放已勾选的课程
        c_set = set()
        # 记录次数以及i个变量
        i = 0
        # 存放多个变量
        v = [None] * len(data_list)
        for data in data_list:
            cno = data[0].strip()
            cname = data[1].strip()
            v[i] = tkinter.StringVar()
            # 默认不勾选
            v[i].set('0')
            cb = tkinter.Checkbutton(choose_course_frame, text=cname, variable=v[i], onvalue=cno,
                                     offvalue='d%s' % cno, command=lambda x=i: choose_course(x))
            # 教师选课布局
            cb.grid(row=1, column=i, sticky=tkinter.W)
            i += 1
        choose_course_button = tkinter.Button(choose_course_frame, text='选择课程', command=lambda: add_course())
        choose_course_button.grid(row=2, column=0, sticky=tkinter.W)
    else:
        none_lable = tkinter.Label(choose_course_frame, text='无')
        none_lable.grid(row=1, column=0)

    # 查询已选课程
    with ConnectDatabase() as cursor:
        sql = "select cno,cname from course where tno={};".format(teacher_id)
        cursor.execute(sql)
        course_list = cursor.fetchall()
        print(course_list)

    # 已选课程的插件
    course_frame = tkinter.Frame(index_window)
    course_title = tkinter.Label(course_frame, text='已选课程:')
    course_frame.place(x=30, y=300)
    course_title.grid(row=0, column=0, sticky=tkinter.W, padx=50)
    course_name = tkinter.Label(course_frame, text='课程名')
    count = tkinter.Label(course_frame, text='人数')
    course_name.grid(row=1, column=0, sticky=tkinter.W, padx=50)
    count.grid(row=1, column=1, sticky=tkinter.W, padx=50)

    if len(course_list) != 0:
        j = 0
        cv = [None] * len(course_list)
        for course in course_list:
            cno = course[0].strip()
            course_name = course[1].strip()
            cv[j] = tkinter.StringVar()
            cv[j].set(cno)
            # 查找课程人数
            with ConnectDatabase() as cursor:
                sql = "select count(sno) from student_course where cno={}".format(cno)
                cursor.execute(sql)
                course_count = cursor.fetchone()[0]
            # 课程信息框
            course_name_label = tkinter.Label(course_frame, text=course_name)
            course_count_label = tkinter.Label(course_frame, text=course_count)
            course_info_button = tkinter.Button(course_frame, text='课程信息', command=lambda x=j: show_info(x))
            cancel_button = tkinter.Button(course_frame, text='取消课程', command=lambda x=j: delete_course(x))
            # 课程信息布局
            course_name_label.grid(row=j + 2, column=0, sticky=tkinter.W, padx=50)
            course_count_label.grid(row=j + 2, column=1, sticky=tkinter.W, padx=50)
            course_info_button.grid(row=j + 2, column=2, sticky=tkinter.W, padx=50)
            cancel_button.grid(row=j + 2, column=3, sticky=tkinter.W)
            j += 1

    index_window.mainloop()


def create_course_window(cno):
    course_window = tkinter.Tk()
    course_window.geometry('600x600')
    with ConnectDatabase() as cursor:
        # 获取课程名
        sql = "select cname from course where cno={}".format(cno)
        cursor.execute(sql)
        course_name = cursor.fetchone()[0]
        # 获取教师名
        sql = "select tname from course join teacher on course.tno=teacher.tno where cno={};".format(cno)
        cursor.execute(sql)
        teacher_name = cursor.fetchone()[0]
        # 获取所有学生信息
        sql = "select student.sno,sname,sdept from student join student_course on student.sno=student_course.sno where cno={};".format(
            cno)
        cursor.execute(sql)
        student_list = cursor.fetchall()
        print(student_list)

    course_name_label = tkinter.Label(course_window, text='课程名称：' + course_name)
    course_teacher_label = tkinter.Label(course_window, text='授课教师：' + teacher_name)
    course_frame = tkinter.Frame(course_window)
    course_info_label = tkinter.Label(course_frame, text='学生信息')
    course_name_label.place(x=70, y=50)
    course_teacher_label.place(x=70, y=100)
    course_frame.place(x=20, y=180)
    course_info_label.grid(row=0, column=0, sticky=tkinter.W, padx=50)
    id_label = tkinter.Label(course_frame, text='学号')
    name_label = tkinter.Label(course_frame, text='姓名')
    p_label = tkinter.Label(course_frame, text='专业')
    id_label.grid(row=1, column=0, sticky=tkinter.W, padx=50)
    name_label.grid(row=1, column=1, sticky=tkinter.W, padx=50)
    p_label.grid(row=1, column=2, sticky=tkinter.W, padx=50)
    # 展示学生
    if len(student_list) != 0:
        row = 2
        for student_info in student_list:
            student_id = student_info[0].strip()
            student_name = student_info[1].strip()
            professional = student_info[2].strip()

            student_id_label = tkinter.Label(course_frame, text=student_id)
            student_name_label = tkinter.Label(course_frame, text=student_name)
            professional_label = tkinter.Label(course_frame, text=professional)
            student_id_label.grid(row=row, column=0, sticky=tkinter.W, padx=50)
            student_name_label.grid(row=row, column=1, sticky=tkinter.W, padx=50)
            professional_label.grid(row=row, column=2, sticky=tkinter.W, padx=50)
            row += 1

    course_window.mainloop()


def create_student_update_window(student_id):
    def update_info():
        is_update = tkinter.messagebox.askyesno(title='提示', message='确认修改吗？')
        if is_update is True:
            new_sex = sex_input.get()
            new_professional = professional_input.get()
            new_birthday = birthday_input.get()
            new_password = password_input.get()

            with ConnectDatabase() as cursor:
                sql = "update student set sbirthday='%s',password='%s' where sno='%s'" % (
                    new_birthday, new_password, student_id)
                cursor.execute(sql)
        update_window.destroy()
        create_student_index_window(student_id)

    update_window = tkinter.Tk()
    update_window.geometry('600x400')
    # 查询基本信息
    with ConnectDatabase() as cursor:
        sql = "select * from student where sno='%s'" % student_id
        cursor.execute(sql)
        info = cursor.fetchone()
        print(info)
    student_id = info[0].strip()
    student_name = info[1].strip()
    password = info[2].strip()
    sex = info[3].strip()
    birthday = info[4].strip()
    professional = info[5].strip()

    # 定义变量
    student_id_input = tkinter.StringVar()
    student_name_input = tkinter.StringVar()
    sex_input = tkinter.StringVar()
    professional_input = tkinter.StringVar()
    birthday_input = tkinter.StringVar()
    password_input = tkinter.StringVar()

    # 设置原本信息
    student_id_input.set(student_id)
    student_name_input.set(student_name)
    sex_input.set(sex)
    professional_input.set(professional)
    birthday_input.set(birthday)
    password_input.set(password)

    # 插件
    info_frame = tkinter.Frame(update_window)
    info_title = tkinter.Label(info_frame, text='学生信息')
    student_id_label = tkinter.Label(info_frame, text="学号：")
    student_id_entry = tkinter.Entry(info_frame, textvariable=student_id_input, state="disabled")
    student_name_label = tkinter.Label(info_frame, text="姓名：")
    student_name_entry = tkinter.Entry(info_frame, textvariable=student_name_input, state="disabled")
    sex_label = tkinter.Label(info_frame, text="性别：")
    sex_entry = tkinter.Entry(info_frame, textvariable=sex_input)
    professional_label = tkinter.Label(info_frame, text="专业：")
    professional_entry = tkinter.Entry(info_frame, textvariable=professional_input)
    birthday_label = tkinter.Label(info_frame, text="出生日期：")
    birthday_entry = tkinter.Entry(info_frame, textvariable=birthday_input)
    password_label = tkinter.Label(info_frame, text='密码：')
    password_entry = tkinter.Entry(info_frame, textvariable=password_input)
    update_button = tkinter.Button(info_frame, text='修改信息', command=update_info)

    # 布局
    info_frame.place(x=10, y=50)
    info_title.grid(row=0, column=0, sticky=tkinter.W, padx=10)
    student_id_label.grid(row=1, column=0, sticky=tkinter.W, padx=10)
    student_id_entry.grid(row=1, column=1, sticky=tkinter.W, padx=10)
    professional_label.grid(row=1, column=2, sticky=tkinter.W, padx=10)
    professional_entry.grid(row=1, column=3, sticky=tkinter.W, padx=10)
    student_name_label.grid(row=2, column=0, sticky=tkinter.W, padx=10)
    student_name_entry.grid(row=2, column=1, sticky=tkinter.W, padx=10)
    birthday_label.grid(row=2, column=2, sticky=tkinter.W, padx=10)
    birthday_entry.grid(row=2, column=3, sticky=tkinter.W, padx=10)
    sex_label.grid(row=3, column=0, sticky=tkinter.W, padx=10)
    sex_entry.grid(row=3, column=1, sticky=tkinter.W, padx=10)
    password_label.grid(row=3, column=2, sticky=tkinter.W, padx=10)
    password_entry.grid(row=3, column=3, sticky=tkinter.W, padx=10)
    update_button.grid(row=4, column=0, sticky=tkinter.W, padx=10)

    update_window.mainloop()


def create_teacher_update_window(teacher_id):
    def update_info():
        is_update = tkinter.messagebox.askyesno(title='提示', message='确认修改吗？')
        if is_update is True:
            new_sex = sex_input.get()
            new_professional = professional_input.get()
            new_birthday = birthday_input.get()
            new_password = password_input.get()
            new_prof = prof_input.get()

            with ConnectDatabase() as cursor:
                sql = "update teacher set tbirthday='%s',password='%s' where tno='%s'" % (
                    new_birthday, new_password, teacher_id)
                cursor.execute(sql)
        update_window.destroy()
        create_teacher_index_window(teacher_id)

    update_window = tkinter.Tk()
    update_window.geometry('600x400')
    # 查询基本信息
    with ConnectDatabase() as cursor:
        sql = "select * from teacher where tno='%s'" % teacher_id
        cursor.execute(sql)
        info = cursor.fetchone()
        print(info)
    teacher_id = info[0].strip()
    teacher_name = info[1].strip()
    password = info[2].strip()
    sex = info[3].strip()
    birthday = info[4].strip()
    professional = info[5].strip()
    prof = info[6].strip()

    # 定义变量
    teacher_id_input = tkinter.StringVar()
    teacher_name_input = tkinter.StringVar()
    sex_input = tkinter.StringVar()
    professional_input = tkinter.StringVar()
    birthday_input = tkinter.StringVar()
    password_input = tkinter.StringVar()
    prof_input = tkinter.StringVar()

    # 设置原本信息
    teacher_id_input.set(teacher_id)
    teacher_name_input.set(teacher_name)
    sex_input.set(sex)
    professional_input.set(professional)
    birthday_input.set(birthday)
    password_input.set(password)
    prof_input.set(prof)

    # 插件
    info_frame = tkinter.Frame(update_window)
    info_title = tkinter.Label(info_frame, text='学生信息')
    student_id_label = tkinter.Label(info_frame, text="学号：")
    student_id_entry = tkinter.Entry(info_frame, textvariable=teacher_id_input, state="disabled")
    student_name_label = tkinter.Label(info_frame, text="姓名：")
    student_name_entry = tkinter.Entry(info_frame, textvariable=teacher_name_input, state="disabled")
    sex_label = tkinter.Label(info_frame, text="性别：")
    sex_entry = tkinter.Entry(info_frame, textvariable=sex_input)
    professional_label = tkinter.Label(info_frame, text="专业：")
    professional_entry = tkinter.Entry(info_frame, textvariable=professional_input)
    birthday_label = tkinter.Label(info_frame, text="出生日期：")
    birthday_entry = tkinter.Entry(info_frame, textvariable=birthday_input)
    password_label = tkinter.Label(info_frame, text='密码：')
    password_entry = tkinter.Entry(info_frame, textvariable=password_input)
    prof_label = tkinter.Label(info_frame, text='称职：')
    prof_entry = tkinter.Entry(info_frame, textvariable=prof_input)
    update_button = tkinter.Button(info_frame, text='修改信息', command=update_info)

    # 布局
    info_frame.place(x=10, y=50)
    info_title.grid(row=0, column=0, sticky=tkinter.W, padx=10)
    student_id_label.grid(row=1, column=0, sticky=tkinter.W, padx=10)
    student_id_entry.grid(row=1, column=1, sticky=tkinter.W, padx=10)
    professional_label.grid(row=1, column=2, sticky=tkinter.W, padx=10)
    professional_entry.grid(row=1, column=3, sticky=tkinter.W, padx=10)
    student_name_label.grid(row=2, column=0, sticky=tkinter.W, padx=10)
    student_name_entry.grid(row=2, column=1, sticky=tkinter.W, padx=10)
    birthday_label.grid(row=2, column=2, sticky=tkinter.W, padx=10)
    birthday_entry.grid(row=2, column=3, sticky=tkinter.W, padx=10)
    sex_label.grid(row=3, column=0, sticky=tkinter.W, padx=10)
    sex_entry.grid(row=3, column=1, sticky=tkinter.W, padx=10)
    password_label.grid(row=3, column=2, sticky=tkinter.W, padx=10)
    password_entry.grid(row=3, column=3, sticky=tkinter.W, padx=10)
    prof_label.grid(row=4, column=0, sticky=tkinter.W, padx=10)
    prof_entry.grid(row=4, column=1, sticky=tkinter.W, padx=10)
    update_button.grid(row=5, column=0, sticky=tkinter.W, padx=10)

    update_window.mainloop()


if __name__ == '__main__':
    create_login_window()
