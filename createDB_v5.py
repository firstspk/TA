from reportlab.pdfgen import canvas
import sqlite3 as It
import os

from flask import send_file

"""
student = It.connect("student.db")
with student:
    cur = student.cursor()
    name = "Name"
    surname = "SURNAME"
    subject = "FRA121"
    department = "FIBO"
    level = "2"
    grade = "2.00"
    tel = "1150"
    email = "email"
    accountNum = "11112"
    # cur.execute("INSERT INTO student(Name,Surname,Subject,Department,Level,Grade,Tel,Email,AccountNum) VALUES(?,?,?,?,?,?,?,?,?)",(name,surname,subject,department,level,grade,tel,email,accountNum))
    # cur.execute("create table student(Username text,Password text,TypeUser text,Name text,Surname text,Level text,Department text,Grade text,Tel text,Email text,AccountNum text,Subject text,Day text,Month text,Year text,TimeCome text,TimeBack text)")

teacher = It.connect("teacher.db")
with teacher:
    cur2 = teacher.cursor()
    # cur2.execute("create table teacher(Username text,Password text,TypeUser text,Name text,Surname text,Tel text,Subject text,NumWant text,Level text,Grade text,Attribute text)")
    name = "AJ"
    surname = "TON"
    subject = "FRA131"
    # cur2.execute("INSERT INTO teacher(Name,Surname,Subject) VALUES(?,?,?)",(name,surname,subject))
    teacher.commit()
teacher.close()
student.close()
"""

class DB:
    def regis_teacher(self, username, password, typeuser, name, surname, subject):
        teacher = It.connect("databaseall.db")
        cur2 = teacher.cursor()
        cur2.execute("INSERT INTO teacher(Username,Password,TypeUser,Name,Surname,Subject) VALUES(?,?,?,?,?,?)",
                     (username, password, typeuser, name, surname, subject))
        teacher.commit()
        teacher.close

    def read_teacher_want(username):
        teacher = It.connect("databaseall.db")
        cur2 = teacher.cursor()
        #cur2.execute("SELECT Name,Surname,Subject FROM teacher WHERE Surname='TON'")
        cur2.execute("SELECT Name,Surname,Subject FROM teacher WHERE Username='%s'"%username)
        data = []
        for row in cur2.fetchall():
            k = []
            for i in row:
                k.append(i)
            data.append(k)
        teacher.close()
        return data
    def app_annouce(self,subjectID,url1,url2,url3):
        admin = It.connect("admin_v2.db")
        cur3 = admin.cursor()
        cur3.execute("UPDATE admin SET Recruitment = '%s' WHERE ID = '%s'"%(url1,subjectID))
        cur3.execute("UPDATE admin SET Course_Syllabus = '%s' WHERE ID = '%s'" % (url2, subjectID))
        cur3.execute("UPDATE admin SET Accept = '%s' WHERE ID = '%s'" % (url3, subjectID))
        admin.close()

    def insert_teacherwant(subject,num_want,level,grade,attribute):
        teacher = It.connect("databaseall.db")
        cur2 = teacher.cursor()
        cur2.execute("UPDATE teacher SET Numwant = '%s' WHERE Subject = '%s'"%(num_want,subject))
        cur2.execute("UPDATE teacher SET Level = '%s' WHERE Subject = '%s'" % (level, subject))
        cur2.execute("UPDATE teacher SET Grade = '%s' WHERE Subject = '%s'" % (grade, subject))
        cur2.execute("UPDATE teacher SET Attribute = '%s' WHERE Subject = '%s'" % (attribute, subject))
        teacher.commit()
        teacher.close()
    def class_subject(subject):
        student = It.connect("databaseall.db")
        cur1 = student.cursor()
        cur1.execute("SELECT Name,Surname,Subject,Department,Level,Grade,Tel,Email,AccountNum FROM student WHERE Subject='%s'" % subject)
        list = []
        for row1 in cur1.fetchall():
            a = []
            for i in row1:
                a.append(i)
            list.append(a)
        student.close()
        return list
    def user_name(username,password,type_user):
        student = It.connect("databaseall.db")
        cur1 = student.cursor()
        cur1.execute("INSERT INTO student(Username,Password,TypeUser) VALUES(?,?,?)",(username,password,type_user))
        student.commit()
        student.close()

    def login(input_username):
        student = It.connect("databaseall.db")
        teacher = It.connect("databaseall.db")
        cur1 = student.cursor()
        cur2 = teacher.cursor()
        cur1.execute("SELECT Username, Password, TypeUser FROM student")
        cur2.execute("SELECT Username, Password, TypeUser FROM teacher")
        list = []
        for row1 in cur1.fetchall(): list.append(row1)
        for row2 in cur2.fetchall(): list.append(row2)
        #print(list)
        student.close()
        teacher.close()
        return list #list be All username, password, TypeUser in students&teachers.db

    def register(username,name,surname,level,department,grade,tel,email,accountnum,subject):
        student = It.connect("databaseall.db")
        cur1 = student.cursor()
        cur1.execute("UPDATE student SET Name= '%s' WHERE Username = '%s'" % (name, username))
        cur1.execute("UPDATE student SET Surname = '%s' WHERE Username = '%s'" % (surname, username))
        cur1.execute("UPDATE student SET Level = '%s' WHERE Username = '%s'" % (level, username))
        cur1.execute("UPDATE student SET Department = '%s' WHERE Username = '%s'" % (department, username))
        cur1.execute("UPDATE student SET Grade = '%s' WHERE Username = '%s'" % (grade, username))
        cur1.execute("UPDATE student SET Tel = '%s' WHERE Username = '%s'" % (tel, username))
        cur1.execute("UPDATE student SET Email = '%s' WHERE Username = '%s'" % (email, username))
        cur1.execute("UPDATE student SET AccountNum = '%s' WHERE Username = '%s'" % (accountnum, username))
        cur1.execute("UPDATE student SET Subject = '%s' WHERE Username = '%s'" % (subject, username))
        student.commit()
        student.close()

    def working_time(self,username,day,month,year,timecome,timeback):
        student = It.connect("databaseall.db")
        cur = student.cursor()
        cur.execute("SELECT Day,Month,Year ,TimeCome,TimeBack FROM student WHERE Username='%s'"%username)
        pdf = []
        for pdfrow in cur.fetchall():
            pdflist = []
            for i in pdfrow:
                pdflist.append(i)
            pdf.append(pdflist)
        if pdf[0][0] == None:
            print ('kkkkkk')
            cur.execute("UPDATE student SET Day= '%s' WHERE Username = '%s'" % (day, username))
            cur.execute("UPDATE student SET Month = '%s' WHERE Username = '%s'" % (month, username))
            cur.execute("UPDATE student SET Year = '%s' WHERE Username = '%s'" % (year, username))
            cur.execute("UPDATE student SET TimeCome = '%s' WHERE Username = '%s'" % (timecome, username))
            cur.execute("UPDATE student SET TimeBack = '%s' WHERE Username = '%s'" % (timeback, username))
            student.commit()
        else:
            cur.execute("SELECT Username,Password,TypeUser,Name,Surname,Subject,IDNUMBER,Department,Level,Grade,Tel,Email,AccountNum FROM student WHERE Username='%s'" % username)
            data = []
            for pdfrow in cur.fetchall():
                datalist = []
                for i in pdfrow:
                    datalist.append(i)
                data.append(datalist)
            print ('>1')
            cur.execute("INSERT INTO student(Username,Password,TypeUser,Name,Surname,Subject,IDNUMBER,Department,Level,Grade,Tel,Email,AccountNum,Day,Month,Year ,TimeCome,TimeBack ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(data[0][0],data[0][1],data[0][2],data[0][3],data[0][4],data[0][5],data[0][6],data[0][7],data[0][8],data[0][9],data[0][10],data[0][11],data[0][12],day,month,year,timecome,timeback))
            student.commit()
        student.close()

    def download(username):
        return os.startfile('%s.pdf'%username)

    def pdf(self,username):
        student = It.connect("student_v2.db")
        cur1 = student.cursor()
        cur1.execute("SELECT Name,Surname,Subject,Department,Level,Grade,Tel,Email,Day,Month,YEAR ,Timecome,Timeback FROM student WHERE Username='%s'"%username)
        pdf = []
        for pdfrow in cur1.fetchall():
            pdflist = []
            for i in pdfrow:
                pdflist.append(i)
            pdf.append(pdflist)
        print(pdf)
        pdfcreate = canvas.Canvas('%s.pdf'%username)
        pdfcreate.drawString(100, 800, 'INSTITUTE OF FIELD ROBOTICS STUDENT WORKING HOUR FORM ')
        pdfcreate.drawString(210, 770, 'SEMESTER : 1  YEAR : 2560')
        pdfcreate.drawString(130, 740, 'KING MONGKUT UNIVERSITY OF TECHNOLOGY THONBURI')
        pdfcreate.drawString(80, 710, '==============================================================')
        pdfcreate.drawString(50, 680,'Name :')
        pdfcreate.drawString(120, 680, pdf[0][0])
        pdfcreate.drawString(220, 680, 'Surname :')
        pdfcreate.drawString(300, 680, pdf[0][1])
        pdfcreate.drawString(400, 680, 'Subject :')
        pdfcreate.drawString(480, 680, pdf[0][2])
        pdfcreate.drawString(50, 650, 'Department :')
        pdfcreate.drawString(120, 650, pdf[0][3])
        pdfcreate.drawString(220, 650, 'Level :')
        pdfcreate.drawString(300, 650, pdf[0][4])
        pdfcreate.drawString(400, 650, 'Grade :')
        pdfcreate.drawString(480, 650, pdf[0][5])
        pdfcreate.drawString(50, 620, 'Tel :')
        pdfcreate.drawString(120, 620, pdf[0][6])
        pdfcreate.drawString(220, 620, 'Email :')
        pdfcreate.drawString(300, 620, pdf[0][7])
        pdfcreate.drawString(50, 520, 'Day :')
        pdfcreate.drawString(100, 520, pdf[0][8])
        pdfcreate.drawString(150, 520, 'Month :')
        pdfcreate.drawString(200, 520, pdf[0][9])
        pdfcreate.drawString(250, 520, 'Year :')
        pdfcreate.drawString(300, 520, pdf[0][10])
        pdfcreate.drawString(350, 520, 'Timecome :')
        pdfcreate.drawString(420, 520, pdf[0][11])
        pdfcreate.drawString(450, 520, 'Timeback :')
        pdfcreate.drawString(520, 520, pdf[0][11])
        pdfcreate.drawString(50, 490, 'Day :')
        pdfcreate.drawString(100,490, pdf[0][8])
        pdfcreate.drawString(150, 490, 'Month :')
        pdfcreate.drawString(200, 490, pdf[0][9])
        pdfcreate.drawString(250, 490, 'Year :')
        pdfcreate.drawString(300, 490, pdf[0][10])
        pdfcreate.drawString(350, 490, 'Timecome :')
        pdfcreate.drawString(420, 490, pdf[0][11])
        pdfcreate.drawString(450, 490, 'Timeback :')
        pdfcreate.drawString(520, 490, pdf[0][11])
        pdfcreate.save()
        print(pdf[0][0])
        student.close()

    def student_email(self):
        data = It.connect("databaseall.db")
        datacur = data.cursor()
        datacur.execute("SELECT Email, Name, Surname FROM student")
        list = []
        for row1 in datacur.fetchall():
            print(row1)
            if(row1[0] != None):
                #print(row1[0])
                list.append(row1)
        datacur.close()
        return(list)
    def teacher_email(self):
        data = It.connect("databaseall.db")
        datacur = data.cursor()
        datacur.execute("SELECT Email, Name, Surname FROM teacher")
        list = []
        for row1 in datacur.fetchall():
            print(row1)
            if(row1[0] != None):
                #print(row1[0])
                list.append(row1)
        datacur.close()
        return(list)

#won=DB()
#DB.download('US1')
#DB.register("US1","John","Williem","1","KMUTT","4.00","1150","Johnza555@mail","1112","FRA121")
#print(readteacherwant("PI"))
#print (classsubject("FRA121"))
#userName("US3","P@ssw0rd","student")
#userName("US4","P@ssw0rd","student")
#won.regis_teacher("Teacher1",1234,"teacher",None,None,"FRA122")
#won.insertteacherwant("FRA131","10","12","4","ksdfkk")

#classsubject("TON")
