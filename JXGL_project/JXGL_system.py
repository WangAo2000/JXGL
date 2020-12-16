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
            tkinter.messagebox.showerror(title='����', message='������')
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
        # ��ȡ�˺š����롢���
        student_id = student_id_input.get()
        password = password_input.get()
        chosen_status = login_status()
        # �ж����
        if chosen_status == 'ѧ��':
            # ��������
            with ConnectDatabase() as cursor:
                sql = "select sno,password from student where sno='%s'" % student_id
                cursor.execute(sql)
                data = cursor.fetchone()
            # �ж������Ƿ����
            if data is not None:
                valid_student_id, valid_password = data
                valid_student_id = valid_student_id.strip()
                valid_password = valid_password.strip()
                # ��֤����
                if student_id == valid_student_id and password == valid_password:
                    print('��¼�ɹ�')
                    login_window.destroy()
                    create_student_index_window(valid_student_id)
                else:
                    tkinter.messagebox.showerror(title='����', message='������˺Ų���ȷ')
                    password_input.set('')
            else:
                tkinter.messagebox.showerror(title='����', message='������˺Ų���ȷ')
                password_input.set('')
        if chosen_status == '��ʦ':
            # ��������
            with ConnectDatabase() as cursor:
                sql = "select tno,password from teacher where tno='%s'" % student_id
                cursor.execute(sql)
                data = cursor.fetchone()
            # �ж������Ƿ����
            if data is not None:
                valid_teacher_id, valid_password = data
                # ȥ������Ŀո�
                valid_teacher_id = valid_teacher_id.strip()
                valid_password = valid_password.strip()
                # ��֤����
                if student_id == valid_teacher_id and password == valid_password:
                    print('��¼�ɹ�')
                    login_window.destroy()
                    create_teacher_index_window(valid_teacher_id)
                else:
                    tkinter.messagebox.showerror(title='����', message='������˺Ų���ȷ')
                    password_input.set('')
            else:
                tkinter.messagebox.showerror(title='����', message='������˺Ų���ȷ')
                password_input.set('')

    def login_status():
        return status.get()

    # ������¼����
    login_window = tkinter.Tk()
    login_window.geometry('400x250')
    # ����ı���
    student_id_input = tkinter.StringVar()
    password_input = tkinter.StringVar()
    # ��¼�����
    status = tkinter.StringVar()
    # Ĭ��ѧ��
    status.set('ѧ��')
    # ����
    title = tkinter.Label(login_window, text='�������ϵͳ��¼', font=('����', 12))
    # ������ŵ�����
    f = tkinter.Frame(login_window)
    # ��ǩ
    student_id_label = tkinter.Label(f, text='�˺ţ�')
    password_label = tkinter.Label(f, text='���룺')
    # �����
    student_id_entry = tkinter.Entry(f, textvariable=student_id_input)
    password_entry = tkinter.Entry(f, show='*', textvariable=password_input)
    # ��¼��ť
    login_button = tkinter.Button(f, text='��¼', command=login)
    # ��ѡ��
    student = tkinter.Radiobutton(f, text='ѧ��', variable=status, value='ѧ��', command=login_status)
    teacher = tkinter.Radiobutton(f, text='��ʦ', variable=status, value='��ʦ', command=login_status)

    # ����ڷ�
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

    # չʾ�γ���Ϣ
    def show_info(x):
        cno = cv[x].get()
        create_course_window(cno)

    # ȡ���γ�
    def delete_course(x):
        cno = cv[x].get()
        with ConnectDatabase() as cursor:
            sql = "delete from student_course where sno={} and cno={}".format(student_id, cno)
            cursor.execute(sql)
        index_window.destroy()
        create_student_index_window(student_id)

    # ��ȡѧ������
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

    # ѧ����Ϣ
    info_frame = tkinter.Frame(index_window)
    info_title = tkinter.Label(info_frame, text='ѧ����Ϣ')
    student_id_label = tkinter.Label(info_frame, text="ѧ�ţ�" + student_id)
    student_name_label = tkinter.Label(info_frame, text="������" + student_name)
    sex_label = tkinter.Label(info_frame, text="�Ա�" + sex)
    professional_label = tkinter.Label(info_frame, text="רҵ��" + professional)
    birthday_label = tkinter.Label(info_frame, text="�������ڣ�" + birthday)
    update_button = tkinter.Button(info_frame, text='�޸���Ϣ', command=update_info)

    # ѧ����Ϣ�Ĳ���
    info_frame.place(x=30, y=50)
    info_title.grid(row=0, column=0, sticky=tkinter.W, padx=50)
    student_id_label.grid(row=1, column=0, sticky=tkinter.W, padx=50)
    student_name_label.grid(row=2, column=0, sticky=tkinter.W, padx=50)
    sex_label.grid(row=3, column=0, sticky=tkinter.W, padx=50)
    professional_label.grid(row=1, column=1, sticky=tkinter.W, padx=50)
    birthday_label.grid(row=2, column=1, sticky=tkinter.W, padx=50)
    update_button.grid(row=3, column=2, sticky=tkinter.W, padx=50)

    # �������н�ʦ�Ŀγ�
    with ConnectDatabase() as cursor:
        sql = "select * from course where tno is not NULL " \
              "and cno not in (select cno from student_course where sno='%s')" % student_id
        cursor.execute(sql)
        data_list = cursor.fetchall()
    # ѧ��ѡ�ο�
    choose_course_frame = tkinter.Frame(index_window)
    choose_course_title = tkinter.Label(choose_course_frame, text='��ѡ�γ̣�')
    choose_course_frame.place(x=80, y=200)
    choose_course_title.grid(row=0, column=0, sticky=tkinter.W)
    # �ж���û�пγ�ѡ��
    if len(data_list) != 0:
        # ����ѹ�ѡ�Ŀγ�
        c_set = set()
        # ��¼�����Լ�i������
        i = 0
        # ��Ŷ������
        v = [None] * len(data_list)
        for data in data_list:
            cno = data[0].strip()
            cname = data[1].strip()
            tno = data[2].strip()
            v[i] = tkinter.StringVar()
            # Ĭ�ϲ���ѡ
            v[i].set('0')
            cb = tkinter.Checkbutton(choose_course_frame, text=cname, variable=v[i], onvalue=cno,
                                     offvalue='d%s' % cno, command=lambda x=i: choose_course(x))
            # ѧ��ѡ�β���
            cb.grid(row=1, column=i, sticky=tkinter.W)
            i += 1
        choose_course_button = tkinter.Button(choose_course_frame, text='ѡ��γ�', command=lambda: add_course(student_id))
        choose_course_button.grid(row=2, column=0, sticky=tkinter.W)
    else:
        none_lable = tkinter.Label(choose_course_frame, text='��')
        none_lable.grid(row=1, column=0)

    # ��ѯ��ѡ�γ�
    with ConnectDatabase() as cursor:
        sql = "select course.cno,cname from student_course join course on course.cno=student_course.cno where student_course.sno={} ".format(
            student_id)
        cursor.execute(sql)
        course_list = cursor.fetchall()
        print(course_list)

    # ��ѡ�γ̵Ĳ��
    course_frame = tkinter.Frame(index_window)
    course_title = tkinter.Label(course_frame, text='��ѡ�γ�:')
    course_frame.place(x=30, y=300)
    course_title.grid(row=0, column=0, sticky=tkinter.W, padx=50)
    course_name = tkinter.Label(course_frame, text='�γ���')
    count = tkinter.Label(course_frame, text='����')
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
            # ���ҿγ�����
            with ConnectDatabase() as cursor:
                sql = "select count(sno) from student_course where cno={}".format(cno)
                cursor.execute(sql)
                course_count = cursor.fetchone()[0]
            # �γ���Ϣ��
            course_name_label = tkinter.Label(course_frame, text=course_name)
            course_count_label = tkinter.Label(course_frame, text=course_count)
            course_info_button = tkinter.Button(course_frame, text='�γ���Ϣ', command=lambda x=j: show_info(x))
            cancel_button = tkinter.Button(course_frame, text='ȡ���γ�', command=lambda x=j: delete_course(x))
            # �γ���Ϣ����
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

    # չʾ�γ���Ϣ
    def show_info(x):
        cno = cv[x].get()
        create_course_window(cno)

    # ȡ���γ�
    def delete_course(x):
        cno = cv[x].get()
        with ConnectDatabase() as cursor:
            sql = "update course set tno=null where cno={};".format(cno)
            cursor.execute(sql)
        index_window.destroy()
        create_teacher_index_window(teacher_id)

    # ��ȡ��ʦ����
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
    # ��ʦ��Ϣ
    info_frame = tkinter.Frame(index_window)
    info_title = tkinter.Label(info_frame, text='��ʦ��Ϣ')
    student_id_label = tkinter.Label(info_frame, text="��ʦ�ţ�" + teacher_id)
    student_name_label = tkinter.Label(info_frame, text="������" + teacher_name)
    sex_label = tkinter.Label(info_frame, text="�Ա�" + sex)
    professional_label = tkinter.Label(info_frame, text="רҵ��" + professional)
    birthday_label = tkinter.Label(info_frame, text="�������ڣ�" + birthday)
    prof_label = tkinter.Label(info_frame, text='ְ�ƣ�' + prof)
    update_button = tkinter.Button(info_frame, text='�޸���Ϣ', command=update_info)

    # ѧ����Ϣ�Ĳ���
    info_frame.place(x=30, y=50)
    info_title.grid(row=0, column=0, sticky=tkinter.W, padx=50)
    student_id_label.grid(row=1, column=0, sticky=tkinter.W, padx=50)
    professional_label.grid(row=1, column=1, sticky=tkinter.W, padx=50)
    student_name_label.grid(row=2, column=0, sticky=tkinter.W, padx=50)
    birthday_label.grid(row=2, column=1, sticky=tkinter.W, padx=50)
    sex_label.grid(row=3, column=0, sticky=tkinter.W, padx=50)
    prof_label.grid(row=3, column=1, sticky=tkinter.W, padx=50)
    update_button.grid(row=3, column=2, sticky=tkinter.W, padx=50)

    # ����û�н�ʦ�Ŀγ�
    with ConnectDatabase() as cursor:
        sql = "select * from course where tno is null"
        cursor.execute(sql)
        data_list = cursor.fetchall()
    # ѧ��ѡ�ο�
    choose_course_frame = tkinter.Frame(index_window)
    choose_course_title = tkinter.Label(choose_course_frame, text='��ѡ�γ̣�')
    choose_course_frame.place(x=80, y=200)
    choose_course_title.grid(row=0, column=0, sticky=tkinter.W)
    # �ж���û�пγ�ѡ��
    if len(data_list) != 0:
        # ����ѹ�ѡ�Ŀγ�
        c_set = set()
        # ��¼�����Լ�i������
        i = 0
        # ��Ŷ������
        v = [None] * len(data_list)
        for data in data_list:
            cno = data[0].strip()
            cname = data[1].strip()
            v[i] = tkinter.StringVar()
            # Ĭ�ϲ���ѡ
            v[i].set('0')
            cb = tkinter.Checkbutton(choose_course_frame, text=cname, variable=v[i], onvalue=cno,
                                     offvalue='d%s' % cno, command=lambda x=i: choose_course(x))
            # ��ʦѡ�β���
            cb.grid(row=1, column=i, sticky=tkinter.W)
            i += 1
        choose_course_button = tkinter.Button(choose_course_frame, text='ѡ��γ�', command=lambda: add_course())
        choose_course_button.grid(row=2, column=0, sticky=tkinter.W)
    else:
        none_lable = tkinter.Label(choose_course_frame, text='��')
        none_lable.grid(row=1, column=0)

    # ��ѯ��ѡ�γ�
    with ConnectDatabase() as cursor:
        sql = "select cno,cname from course where tno={};".format(teacher_id)
        cursor.execute(sql)
        course_list = cursor.fetchall()
        print(course_list)

    # ��ѡ�γ̵Ĳ��
    course_frame = tkinter.Frame(index_window)
    course_title = tkinter.Label(course_frame, text='��ѡ�γ�:')
    course_frame.place(x=30, y=300)
    course_title.grid(row=0, column=0, sticky=tkinter.W, padx=50)
    course_name = tkinter.Label(course_frame, text='�γ���')
    count = tkinter.Label(course_frame, text='����')
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
            # ���ҿγ�����
            with ConnectDatabase() as cursor:
                sql = "select count(sno) from student_course where cno={}".format(cno)
                cursor.execute(sql)
                course_count = cursor.fetchone()[0]
            # �γ���Ϣ��
            course_name_label = tkinter.Label(course_frame, text=course_name)
            course_count_label = tkinter.Label(course_frame, text=course_count)
            course_info_button = tkinter.Button(course_frame, text='�γ���Ϣ', command=lambda x=j: show_info(x))
            cancel_button = tkinter.Button(course_frame, text='ȡ���γ�', command=lambda x=j: delete_course(x))
            # �γ���Ϣ����
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
        # ��ȡ�γ���
        sql = "select cname from course where cno={}".format(cno)
        cursor.execute(sql)
        course_name = cursor.fetchone()[0]
        # ��ȡ��ʦ��
        sql = "select tname from course join teacher on course.tno=teacher.tno where cno={};".format(cno)
        cursor.execute(sql)
        teacher_name = cursor.fetchone()[0]
        # ��ȡ����ѧ����Ϣ
        sql = "select student.sno,sname,sdept from student join student_course on student.sno=student_course.sno where cno={};".format(
            cno)
        cursor.execute(sql)
        student_list = cursor.fetchall()
        print(student_list)

    course_name_label = tkinter.Label(course_window, text='�γ����ƣ�' + course_name)
    course_teacher_label = tkinter.Label(course_window, text='�ڿν�ʦ��' + teacher_name)
    course_frame = tkinter.Frame(course_window)
    course_info_label = tkinter.Label(course_frame, text='ѧ����Ϣ')
    course_name_label.place(x=70, y=50)
    course_teacher_label.place(x=70, y=100)
    course_frame.place(x=20, y=180)
    course_info_label.grid(row=0, column=0, sticky=tkinter.W, padx=50)
    id_label = tkinter.Label(course_frame, text='ѧ��')
    name_label = tkinter.Label(course_frame, text='����')
    p_label = tkinter.Label(course_frame, text='רҵ')
    id_label.grid(row=1, column=0, sticky=tkinter.W, padx=50)
    name_label.grid(row=1, column=1, sticky=tkinter.W, padx=50)
    p_label.grid(row=1, column=2, sticky=tkinter.W, padx=50)
    # չʾѧ��
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
        is_update = tkinter.messagebox.askyesno(title='��ʾ', message='ȷ���޸���')
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
    # ��ѯ������Ϣ
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

    # �������
    student_id_input = tkinter.StringVar()
    student_name_input = tkinter.StringVar()
    sex_input = tkinter.StringVar()
    professional_input = tkinter.StringVar()
    birthday_input = tkinter.StringVar()
    password_input = tkinter.StringVar()

    # ����ԭ����Ϣ
    student_id_input.set(student_id)
    student_name_input.set(student_name)
    sex_input.set(sex)
    professional_input.set(professional)
    birthday_input.set(birthday)
    password_input.set(password)

    # ���
    info_frame = tkinter.Frame(update_window)
    info_title = tkinter.Label(info_frame, text='ѧ����Ϣ')
    student_id_label = tkinter.Label(info_frame, text="ѧ�ţ�")
    student_id_entry = tkinter.Entry(info_frame, textvariable=student_id_input, state="disabled")
    student_name_label = tkinter.Label(info_frame, text="������")
    student_name_entry = tkinter.Entry(info_frame, textvariable=student_name_input, state="disabled")
    sex_label = tkinter.Label(info_frame, text="�Ա�")
    sex_entry = tkinter.Entry(info_frame, textvariable=sex_input)
    professional_label = tkinter.Label(info_frame, text="רҵ��")
    professional_entry = tkinter.Entry(info_frame, textvariable=professional_input)
    birthday_label = tkinter.Label(info_frame, text="�������ڣ�")
    birthday_entry = tkinter.Entry(info_frame, textvariable=birthday_input)
    password_label = tkinter.Label(info_frame, text='���룺')
    password_entry = tkinter.Entry(info_frame, textvariable=password_input)
    update_button = tkinter.Button(info_frame, text='�޸���Ϣ', command=update_info)

    # ����
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
        is_update = tkinter.messagebox.askyesno(title='��ʾ', message='ȷ���޸���')
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
    # ��ѯ������Ϣ
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

    # �������
    teacher_id_input = tkinter.StringVar()
    teacher_name_input = tkinter.StringVar()
    sex_input = tkinter.StringVar()
    professional_input = tkinter.StringVar()
    birthday_input = tkinter.StringVar()
    password_input = tkinter.StringVar()
    prof_input = tkinter.StringVar()

    # ����ԭ����Ϣ
    teacher_id_input.set(teacher_id)
    teacher_name_input.set(teacher_name)
    sex_input.set(sex)
    professional_input.set(professional)
    birthday_input.set(birthday)
    password_input.set(password)
    prof_input.set(prof)

    # ���
    info_frame = tkinter.Frame(update_window)
    info_title = tkinter.Label(info_frame, text='ѧ����Ϣ')
    student_id_label = tkinter.Label(info_frame, text="ѧ�ţ�")
    student_id_entry = tkinter.Entry(info_frame, textvariable=teacher_id_input, state="disabled")
    student_name_label = tkinter.Label(info_frame, text="������")
    student_name_entry = tkinter.Entry(info_frame, textvariable=teacher_name_input, state="disabled")
    sex_label = tkinter.Label(info_frame, text="�Ա�")
    sex_entry = tkinter.Entry(info_frame, textvariable=sex_input)
    professional_label = tkinter.Label(info_frame, text="רҵ��")
    professional_entry = tkinter.Entry(info_frame, textvariable=professional_input)
    birthday_label = tkinter.Label(info_frame, text="�������ڣ�")
    birthday_entry = tkinter.Entry(info_frame, textvariable=birthday_input)
    password_label = tkinter.Label(info_frame, text='���룺')
    password_entry = tkinter.Entry(info_frame, textvariable=password_input)
    prof_label = tkinter.Label(info_frame, text='��ְ��')
    prof_entry = tkinter.Entry(info_frame, textvariable=prof_input)
    update_button = tkinter.Button(info_frame, text='�޸���Ϣ', command=update_info)

    # ����
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
