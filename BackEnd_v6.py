from flask import Flask, render_template, request,redirect,url_for
from time import gmtime, strftime

from createDB_v5 import DB
import sqlite3 as It
import os

from reportlab.pdfgen import canvas
app = Flask(__name__)

class self_username:
    def __init__(self, name="" , type_user =None):
        self.username = name
        self.type_user = type_user
#*************username = a.username*****************
#System know typeuser when you call a.typeuser
a = self_username()
#a.type_user = ''
#a.type_user = 'student'
#a.type_user = 'teacher'
#a.type_user = 'admin'

@app.route('/')
def index():
    #return render_template('web_sfs_v3/index.html')
    if(a.type_user == None):
        return render_template('Po/first page_po.html')
    if(a.type_user == 'student'):
        return render_template('TA/first page_ta.html')
    if (a.type_user == 'teacher'):
        return render_template('Aj/first page_aj.html')
    if (a.type_user == 'admin'):
        return render_template('Admin/first page_admin.html')

@app.route('/home')
def home():
    return(index())
@app.route('/printingfrom')
def printpdf():
    datawork = It.connect("databaseall.db")
    dataworkcur = datawork.cursor()
    username=a.username


    dataworkcur.execute("SELECT DayMonthYear FROM timesheet WHERE Username='%s'" % username)
    daymonthyear = []
    for pdfrow in dataworkcur.fetchall():
        for i in pdfrow:
            daymonthyear.append(i)

    dataworkcur.execute("SELECT TimeCome FROM timesheet WHERE Username='%s'" % username)
    timecome = []
    for pdfrow in dataworkcur.fetchall():
        for i in pdfrow:
            timecome.append(i)
    print(timecome)
    dataworkcur.execute("SELECT TimeBack FROM timesheet WHERE Username='%s'" % username)
    timeback = []
    for pdfrow in dataworkcur.fetchall():
        for i in pdfrow:
            timeback.append(i)
    print(timeback)
    dataworkcur.execute("SELECT whatdo FROM timesheet WHERE Username='%s'" % username)
    whatdo = []
    for pdfrow in dataworkcur.fetchall():
        for i in pdfrow:
            whatdo.append(i)
    dataworkcur.execute("SELECT Comment FROM timesheet WHERE Username='%s' and ID='1'" % username)
    comment = []
    for pdfrow in dataworkcur.fetchall():
        for i in pdfrow:
            comment.append(i)
    dataworkcur.execute("SELECT StatusAj FROM timesheet WHERE Username='%s' and ID='1'" % username)
    statusaj = []
    for pdfrow in dataworkcur.fetchall():
        for i in pdfrow:
            statusaj.append(i)
    dataworkcur.execute("SELECT StatusAdmin FROM timesheet WHERE Username='%s' and ID='1'" % username)
    statusad = []
    for pdfrow in dataworkcur.fetchall():
        for i in pdfrow:
            statusad.append(i)
    print(statusaj[0])
    print(statusad[0])

    if (statusaj[0]=='0' and statusad[0] != 'x') or (statusad[0]=='0' and statusaj[0] != 'x'):
        warn = []
        warn.append('กรุณารออาจารย์/แอดมินตรวจ')
    elif statusaj[0] == 'x' or statusad[0] == 'x':
        warn = []
        warn.append('แบบฟอร์มไม่ผ่านกรุณากดแก้ไขอีกครั้ง')
        print('kkkkkkkkkkkkkkkkfjsdklf')


    elif statusaj[0]=='1' and statusad[0]=='1':
        warn=[]
        warn.append('แบบฟอร์มผ่าน สามารถพิมพ์แบบฟอร์มได้')
    return (render_template('TA/printingFrom_TA.html', daymonthyear=daymonthyear,timecome=timecome, timeback=timeback, whatdo=whatdo,comment=comment[0],warn=warn[0]))

@app.route('/printworkta', methods=["POST"])
def printworkta():
    datawork = It.connect("databaseall.db")
    dataworkcur = datawork.cursor()
    x = dict(request.form.items())
    do=[]
    for i in x:
        do.append(i)
        print(i)
    print(do[2])
    username=a.username
    dataworkcur.execute("SELECT StatusAj,StatusAdmin FROM timesheet WHERE Username='%s' and ID = '1'"% username)
    status = []
    for pdfrow in dataworkcur.fetchall():
        for i in pdfrow:
            status.append(i)
    print(status[0])

    if do[2]=='edit':
        return render_template('TA/WorkingForm_TA_v3_ta.html')
    if do[2] == 'print'and status[0]=='1' and status[1]=='1':
        date=strftime("%d%b%Y%S", gmtime())
        print(date)
        student = It.connect("databaseall.db")
        cur = student.cursor()
        cur.execute("SELECT Name,Surname,Subject,Department,Level,Grade,Tel,Email FROM student WHERE Username='%s'" % username)
        pdf = []
        for pdfrow in cur.fetchall():
            pdflist = []
            for i in pdfrow:
                pdflist.append(i)
            pdf.append(pdflist)
        timesheets = It.connect("databaseall.db")
        timesheetcur = timesheets.cursor()
        timesheetcur.execute(
            "SELECT DayMonthYear ,Timecome,Timeback, StatusAj ,whatdo FROM timesheet WHERE Username='%s'" % username)
        pdfwork = []
        for pdfrow in timesheetcur.fetchall():
            pdflist = []
            for i in pdfrow:
                pdflist.append(i)
            pdfwork.append(pdflist)
        namepdf=str(username)+str(date)
        print(namepdf)
        print(type(namepdf))
        pdfcreate = canvas.Canvas('%s.pdf' % namepdf)
        pdfcreate.drawString(100, 800, 'INSTITUTE OF FIELD ROBOTICS STUDENT WORKING HOUR FORM ')
        pdfcreate.drawString(210, 770, 'SEMESTER : 1  YEAR : 2560')
        pdfcreate.drawString(130, 740, 'KING MONGKUT UNIVERSITY OF TECHNOLOGY THONBURI')
        pdfcreate.drawString(80, 710, '==============================================================')
        pdfcreate.drawString(50, 680, 'Name :')

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

        pdfcreate.drawString(450, 590, 'Workingdata')

        pdfcreate.drawString(50, 560, 'Day/Month/Year :')
        pdfcreate.drawString(200, 560, pdfwork[0][0])
        pdfcreate.drawString(350, 560, 'Timecome :')
        pdfcreate.drawString(420, 560, pdfwork[0][1])
        pdfcreate.drawString(450, 560, 'Timeback :')
        pdfcreate.drawString(520, 560, pdfwork[0][2])
        pdfcreate.drawString(50, 530, 'Day/Month/Year :')
        pdfcreate.drawString(200, 530, pdfwork[1][0])
        pdfcreate.drawString(350, 530, 'Timecome :')
        pdfcreate.drawString(420, 530, pdfwork[1][1])
        pdfcreate.drawString(450, 530, 'Timeback :')
        pdfcreate.drawString(520, 530, pdfwork[1][2])
        pdfcreate.drawString(50, 500, 'Day/Month/Year :')
        pdfcreate.drawString(200, 500, pdfwork[2][0])
        pdfcreate.drawString(350, 500, 'Timecome :')
        pdfcreate.drawString(420, 500, pdfwork[2][1])
        pdfcreate.drawString(450, 500, 'Timeback :')
        pdfcreate.drawString(520, 500, pdfwork[2][2])
        pdfcreate.drawString(50, 470, 'Day/Month/Year :')
        pdfcreate.drawString(200, 470, pdfwork[3][0])
        pdfcreate.drawString(350, 470, 'Timecome :')
        pdfcreate.drawString(420, 470, pdfwork[3][1])
        pdfcreate.drawString(450, 470, 'Timeback :')
        pdfcreate.drawString(520, 470, pdfwork[3][2])
        pdfcreate.drawString(50, 440, 'Day/Month/Year :')
        pdfcreate.drawString(200, 440, pdfwork[4][0])
        pdfcreate.drawString(350, 440, 'Timecome :')
        pdfcreate.drawString(420, 440, pdfwork[4][1])
        pdfcreate.drawString(450, 440, 'Timeback :')
        pdfcreate.drawString(520, 440, pdfwork[4][2])
        pdfcreate.drawString(50, 410, 'Day/Month/Year :')
        pdfcreate.drawString(200, 410, pdfwork[5][0])
        pdfcreate.drawString(350, 410, 'Timecome :')
        pdfcreate.drawString(420, 410, pdfwork[5][1])
        pdfcreate.drawString(450, 410, 'Timeback :')
        pdfcreate.drawString(520, 410, pdfwork[5][2])
        pdfcreate.drawString(50, 380, 'Day/Month/Year :')
        pdfcreate.drawString(200, 380, pdfwork[6][0])
        pdfcreate.drawString(350, 380, 'Timecome :')
        pdfcreate.drawString(420, 380, pdfwork[6][1])
        pdfcreate.drawString(450, 380, 'Timeback :')
        pdfcreate.drawString(520, 380, pdfwork[6][2])
        pdfcreate.drawString(50, 350, 'Day/Month/Year :')
        pdfcreate.drawString(200, 350, pdfwork[7][0])
        pdfcreate.drawString(350, 350, 'Timecome :')
        pdfcreate.drawString(420, 350, pdfwork[7][1])
        pdfcreate.drawString(450, 350, 'Timeback :')
        pdfcreate.drawString(520, 350, pdfwork[7][2])
        pdfcreate.drawString(400, 320, '.......................')
        pdfcreate.save()

        pdfcreate2 = canvas.Canvas('%sP2.pdf' % namepdf)
        pdfcreate2.drawString(100, 800, 'Job Description ')
        pdfcreate2.drawString(50, 770, pdfwork[0][0])
        pdfcreate2.drawString(200, 770, pdfwork[0][4])
        pdfcreate2.drawString(50, 740, pdfwork[1][0])
        pdfcreate2.drawString(200, 740, pdfwork[1][4])
        pdfcreate2.drawString(50, 710, pdfwork[2][0])
        pdfcreate2.drawString(200, 710, pdfwork[2][4])
        pdfcreate2.drawString(50, 680, pdfwork[3][0])
        pdfcreate2.drawString(200, 680, pdfwork[3][4])
        pdfcreate2.drawString(50, 650, pdfwork[4][0])
        pdfcreate2.drawString(200, 650, pdfwork[4][4])
        pdfcreate2.drawString(50, 620, pdfwork[5][0])
        pdfcreate2.drawString(200, 620, pdfwork[5][4])
        pdfcreate2.drawString(50, 590, pdfwork[6][0])
        pdfcreate2.drawString(200, 590, pdfwork[6][4])
        pdfcreate2.drawString(50, 560, pdfwork[7][0])
        pdfcreate2.drawString(200, 560, pdfwork[7][4])
        pdfcreate2.save()

        timesheets = It.connect("databaseall.db")
        timesheetcur = timesheets.cursor()
        timesheetcur.execute("UPDATE timesheet SET StatusTa = '0' WHERE Username = '%s'and ID = '1'" % (username))
        timesheetcur.execute("UPDATE timesheet SET StatusAdmin = '0' WHERE Username = '%s'and ID = '1'" % (username))
        timesheetcur.execute(
            "UPDATE timesheet SET StatusAj = '0' WHERE Username = '%s'and ID = '1'" % (username))
        timesheets.commit()

        os.startfile('%s.pdf' % namepdf)
        os.startfile('%sP2.pdf' % namepdf)
        return (home())
    if do[2] == 'print':
        if status[0]=='x'or status[1]=='x':
            return redirect(url_for('printpdf'))
    return (home())



@app.route('/recruitment')
def recruitment():
    if(a.type_user == None):
        return (render_template('Po/Vacancy Announcement_po.html'))
    if(a.type_user == 'student'):
        return (render_template('TA/Vacancy Announcement_ta.html'))
    if (a.type_user == 'teacher'):
        return (render_template('Aj/Vacancy Announcement_aj.html'))
    if (a.type_user == 'admin'):
        return (render_template('Admin/Vacancy Announcement_admin.html'))

@app.route('/pass_audition')
def pass_audition():
    if (a.type_user == None):
        return render_template('Po/choose_ta_or_Employment_Announce_po.html')
    if (a.type_user == 'student'):
        return render_template('TA/choose_ta_or_Employment_Announce_ta.html')
    if (a.type_user == 'teacher'):
        return render_template('Aj/choose_ta_or_Employment_Announce_aj.html')
    if (a.type_user == 'admin'):
        return render_template('Admin/choose_ta_or_Employment_Announce_admin.html')

@app.route('/pass_audition_TA')
def pass_audition_TA():
    if (a.type_user == None):
        return render_template('Po/Vacancy Announcement_TA_po.html')
    if (a.type_user == 'student'):
        return render_template('TA/Vacancy Announcement_TA_ta.html')
    if (a.type_user == 'teacher'):
        return render_template('Aj/Vacancy Announcement_TA_aj.html')
    if (a.type_user == 'admin'):
        return render_template('Admin/Vacancy Announcement_TA_admin.html')

@app.route('/pass_audition_employment')
def pass_audition_TA_employment():
    if (a.type_user == None):
        return render_template('Po/Vacancy Announcement_employment_po.html')
    if (a.type_user == 'student'):
        return render_template('TA/Vacancy Announcement_employment_ta.html')
    if (a.type_user == 'teacher'):
        return render_template('Aj/Vacancy Announcement_employment_aj.html')
    if (a.type_user == 'admin'):
        return render_template('Admin/Vacancy Announcement_employment_admin.html')


@app.route('/EX_TA_form')
def Ex_TA_form():
    if (a.type_user == None):
        return render_template('Po/examplefrom_1_po.html')
    if (a.type_user == 'student'):
        return render_template('TA/examplefrom_1_ta.html')
    if (a.type_user == 'teacher'):
        return render_template('Aj/examplefrom_1_aj.html')
    if (a.type_user == 'admin'):
        return render_template('Admin/examplefrom_1_admin.html')

@app.route('/EX_TA_form2')
def Ex_TA_form2():
    if (a.type_user == None):
        return render_template('Po/examplefrom_2_po.html')
    if (a.type_user == 'student'):
        return render_template('TA/examplefrom_2_ta.html')
    if (a.type_user == 'teacher'):
        return render_template('Aj/examplefrom_2_aj.html')
    if (a.type_user == 'admin'):
        return render_template('Admin/examplefrom_2_admin.html')

@app.route('/subject_detail')
def subject_detail():
    if (a.type_user == None):
        return render_template('Po/subject_1_po.html')
    if (a.type_user == 'student'):
        return render_template('TA/subject_1_ta.html')
    if (a.type_user == 'teacher'):
        return render_template('Aj/subject_1_aj.html')
    if (a.type_user == 'admin'):
        return render_template('Admin/subject_1_admin.html')

@app.route('/contact')
def contact():
    if (a.type_user == None):
        return render_template('Po/connect_po.html')
    if (a.type_user == 'student'):
        return render_template('TA/connect_ta.html')
    if (a.type_user == 'teacher'):
        return render_template('Aj/connect_aj.html')
    if (a.type_user == 'admin'):
        return render_template('Admin/connect_admin.html')

@app.route('/profile')
def profile():
    if (a.type_user == 'student'):
        return render_template('TA/Ta_data_ta.html')
    if (a.type_user == 'teacher'):
        return render_template('Aj/Ta_data_aj.html')
    if (a.type_user == 'admin'):
        return render_template('Admin/Ta_data_admin.html')

@app.route('/edit_profile')
def edit_profile():
    if (a.type_user == 'student'):
        return render_template('TA/dataTA_ta2.html')
    if (a.type_user == 'teacher'):
        return render_template('Aj/Ta_data_edit_aj.html')
    if (a.type_user == 'admin'):
        return render_template('Admin/Ta_data_edit_admin.html')
    else:
        return ("System error Personal")

@app.route('/evaluation')
def evaluation():
    if(a.type_user == 'student'):
        return(render_template('TA/FromTest.html'))
    if(a.type_user == 'admin'):
        data = It.connect("databaseall.db")
        datacur = data.cursor()
        datacur.execute("SELECT One1 FROM evaluate")
        one1 = []
        for row1 in datacur.fetchall():
            list = []
            for i in row1:
                list.append(i)
            one1.append(list)
        datacur.execute("SELECT One2 FROM evaluate")
        one2 = []
        for row1 in datacur.fetchall():
            list = []
            for i in row1:
                list.append(i)
            one2.append(list)
        datacur.execute("SELECT One3 FROM evaluate")
        one3 = []
        for row1 in datacur.fetchall():
            list = []
            for i in row1:
                list.append(i)
            one3.append(list)
        datacur.execute("SELECT Two1 FROM evaluate")
        two1 = []
        for row1 in datacur.fetchall():
            list = []
            for i in row1:
                list.append(i)
            two1.append(list)
        datacur.execute("SELECT Two2 FROM evaluate")
        two2 = []
        for row1 in datacur.fetchall():
            list = []
            for i in row1:
                list.append(i)
            two2.append(list)
        datacur.execute("SELECT Two3 FROM evaluate")
        two3 = []
        for row1 in datacur.fetchall():
            list = []
            for i in row1:
                list.append(i)
            two3.append(list)
        datacur.execute("SELECT Three1 FROM evaluate")
        three1 = []
        for row1 in datacur.fetchall():
            list = []
            for i in row1:
                list.append(i)
            three1.append(list)
        datacur.execute("SELECT Three2 FROM evaluate")
        three2 = []
        for row1 in datacur.fetchall():
            list = []
            for i in row1:
                list.append(i)
            three2.append(list)
        datacur.execute("SELECT Three3 FROM evaluate")
        three3 = []
        for row1 in datacur.fetchall():
            list = []
            for i in row1:
                list.append(i)
            three3.append(list)
        datacur.execute("SELECT Comment FROM evaluate")
        comment = []
        for row1 in datacur.fetchall():
            list = []
            for i in row1:
                list.append(i)
            comment.append(list)

        return(render_template('Admin/evaluate show.html',one1=one1,one2=one2,one3=one3,two1=two1,two2=two2,two3=two3,three1=three1,three2=three2,three3=three3,comment=comment))
    else:
        return(home())


@app.route('/editupdate')
def editupdate():
    if (a.type_user == 'admin'):
        return (render_template('Admin/edit_postNews.html'))


@app.route("/Aj_needing")
def Aj_needing():
    teacher = It.connect("databaseall.db")
    cur2 = teacher.cursor()
    cur2.execute("SELECT Subject FROM teacher WHERE Username = '%s'" % a.username)
    subject = []
    for row1 in cur2.fetchall():
        list = []
        for i in row1:
            list.append(i)
            subject.append(list)
    print("Aj_needing")
    return render_template('Aj/Need_Aj3_aj.html',subject =subject)

@app.route("/Need_Aj5_aj" , methods=["POST"] )
def Need_Aj5_aj():
    x = dict(request.form.items())
    subject =x['subject']
    numwant = x['numwant']
    grade = x['grade']
    level = x['level']
    attribute =x['attribute']
    teacher = It.connect("databaseall.db")
    cur2 = teacher.cursor()
    cur2.execute("UPDATE teacher SET Numwant = '%s' WHERE Subject = '%s'" % (numwant, subject))
    cur2.execute("UPDATE teacher SET Level = '%s' WHERE Subject = '%s'" % (level, subject))
    cur2.execute("UPDATE teacher SET Grade = '%s' WHERE Subject = '%s'" % (grade, subject))
    cur2.execute("UPDATE teacher SET Attribute = '%s' WHERE Subject = '%s'" % (attribute, subject))
    teacher.commit()
    teacher.close()
    return("wwwwww")

@app.route("/Need_Aj4_aj")
def Need_Aj4_aj():
    teacher = It.connect("databaseall.db")
    cur2 = teacher.cursor()
    cur2.execute("SELECT Subject FROM teacher WHERE Username = '%s'" % a.username)
    subject = []
    for row1 in cur2.fetchall():
        list = []
        for i in row1:
            list.append(i)
            subject.append(list)
    print(subject)
    for i in subject:
        cur5 = teacher.cursor()
        cur5.execute("SELECT Numwant FROM teacherwant WHERE Subject = '%s'" % i)
        Num = []
        for row1 in cur5.fetchall():
            list = []
            for i in row1:
                list.append(i)
                Num.append(list)
        print (Num)

        cur6 = teacher.cursor()
        cur6.execute("SELECT Level FROM teacherwant WHERE Subject = '%s'" % i)
        Level = []
        for row1 in cur6.fetchall():
            list = []
            for i in row1:
                list.append(i)
                Level.append(list)
        print (Level)

        cur7 = teacher.cursor()
        cur7.execute("SELECT Grade FROM teacherwant WHERE Subject = '%s'" % i)
        Grade = []
        for row1 in cur7.fetchall():
            list = []
            for i in row1:
                list.append(i)
                Grade.append(list)
        print (Grade)

        cur8 = teacher.cursor()
        cur8.execute("SELECT Attribute FROM teacherwant WHERE Subject = '%s'" % i)
        Attri = []
        for row1 in cur8.fetchall():
            list = []
            for i in row1:
                list.append(i)
                Attri.append(list)
        print(Attri)

        cur9 = teacher.cursor()
        cur9.execute("SELECT Syllabus FROM teacherwant ")
        Syllabus = []
        for row1 in cur9.fetchall():
            list = []
            for i in row1:
                list.append(i)
                Syllabus.append(list)
        print (Syllabus)
    return (render_template('Admin/Show_Teacherwant_Aj.html', Subject=Subject, Num=Num, Level=Level, Grade=Grade,Attri=Attri,Syllabus =Syllabus))

@app.route('/Show_register_Ad')
def Show_register_Ad():
    print("Show regis")
    return render_template("Admin/Show_register1_admin.html")

@app.route('/Show_register1')
def Show_register1():
    print("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
    input = dict(request.form.items())
    if (input == "name1"):
        print("name1")
        register1 = It.connect("databaseall.db")
        cur1 = register1.cursor()
        cur1.execute("SELECT Name FROM studentnormal ")
        Name =  []
        for row1 in cur1.fetchall():
            list = []
            for i in row1:
                list.append(i)
                Name.append(list)
        print (Name)

        cur2 = register1.cursor()
        cur2.execute("SELECT Surname FROM studentnormal ")
        surname = []
        for row1 in cur2.fetchall():
            list = []
            for i in row1:
                list.append(i)
                surname.append(list)
        print(surname)

        cur3 = register1.cursor()
        cur3.execute("SELECT Department FROM studentnormal ")
        department = []
        for row1 in cur3.fetchall():
            list = []
            for i in row1:
                list.append(i)
                department.append(list)
        print (department)

        cur4 = register1.cursor()
        cur4.execute("SELECT Branch FROM studentnormal ")
        branch = []
        for row1 in cur4.fetchall():
            list = []
            for i in row1:
                list.append(i)
                branch.append(list)
        print (branch)

        cur5 = register1.cursor()
        cur5.execute("SELECT Degree FROM studentnormal ")
        degree = []
        for row1 in cur5.fetchall():
            list = []
            for i in row1:
                list.append(i)
                degree.append(list)
        print (degree)

        cur6 = register1.cursor()
        cur6.execute("SELECT Level FROM studentnormal ")
        level = []
        for row1 in cur6.fetchall():
            list = []
            for i in row1:
                list.append(i)
                Name.append(list)
        print (Name)

        cur7 = register1.cursor()
        cur7.execute("SELECT Idnum FROM studentnormal ")
        idnum = []
        for row1 in cur7.fetchall():
            list = []
            for i in row1:
                list.append(i)
                idnum.append(list)
        print (idnum)

        cur8 = register1.cursor()
        cur8.execute("SELECT Grade FROM studentnormal ")
        grade = []
        for row1 in cur8.fetchall():
            list = []
            for i in row1:
                list.append(i)
                grade.append(list)
        print (grade)

        cur9 = register1.cursor()
        cur9.execute("SELECT Email FROM studentnormal ")
        email = []
        for row1 in cur9.fetchall():
            list = []
            for i in row1:
                list.append(i)
                email.append(list)
        print (email)

        cur10 = register1.cursor()
        cur10.execute("SELECT Tel FROM studentnormal ")
        tel= []
        for row1 in cur10.fetchall():
            list = []
            for i in row1:
                list.append(i)
                tel.append(list)
        print (tel)

        cur11 = register1.cursor()
        cur11.execute("SELECT Subject FROM studentnormal ")
        subject = []
        for row1 in cur11.fetchall():
            list = []
            for i in row1:
                list.append(i)
                subject.append(list)
        print (subject)

        cur12 = register1.cursor()
        cur12.execute("SELECT AccountNum FROM studentnormal ")
        Accnum = []
        for row1 in cur12.fetchall():
            list = []
            for i in row1:
                list.append(i)
                Accum.append(list)
        print (Accnum)

        cur13 = register1.cursor()
        cur13.execute("SELECT Attribute FROM studentnormal ")
        Attri = []
        for row1 in cur13.fetchall():
            list = []
            for i in row1:
                list.append(i)
                Attri.append(list)
        print (Attri)
        return (render_template('Admin/Show_register2_admin.html',name = Name,surname = surname,department = department , branch = branch ,degree = degree ,level = level ,idnum = idnum ,grade = grade,email = email ,tel = tel ,subject = subject , Accnum = Accnum,Attri=Attri))

    if (input == "name2"):
        print("name2")
        i =1
        register1 = It.connect("databaseall.db")
        cur1 = register1.cursor()
        cur1.execute("SELECT Name FROM studentnormal  WHERE Status = '%s'" % i )
        Name = []
        for row1 in cur1.fetchall():
            list = []
            for i in row1:
                list.append(i)
                Name.append(list)
        print(Name)

        cur2 = register1.cursor()
        cur2.execute("SELECT Surname FROM studentnormal WHERE Status = '%s'" % i)
        surname = []
        for row1 in cur2.fetchall():
            list = []
            for i in row1:
                list.append(i)
                surname.append(list)
        print(surname)

        cur3 = register1.cursor()
        cur3.execute("SELECT Department FROM studentnormal  WHERE Status = '%s'" % i)
        department = []
        for row1 in cur3.fetchall():
            list = []
            for i in row1:
                list.append(i)
                department.append(list)
        print(department)

        cur4 = register1.cursor()
        cur4.execute("SELECT Branch FROM studentnormal  WHERE Status = '%s'" % i)
        branch = []
        for row1 in cur4.fetchall():
            list = []
            for i in row1:
                list.append(i)
                branch.append(list)
        print(branch)

        cur5 = register1.cursor()
        cur5.execute("SELECT Degree FROM studentnormal  WHERE Status = '%s'" % i)
        degree = []
        for row1 in cur5.fetchall():
            list = []
            for i in row1:
                list.append(i)
                degree.append(list)
        print(degree)

        cur6 = register1.cursor()
        cur6.execute("SELECT Level FROM studentnormal  WHERE Status = '%s'" % i)
        level = []
        for row1 in cur6.fetchall():
            list = []
            for i in row1:
                list.append(i)
                Name.append(list)
        print(Name)

        cur7 = register1.cursor()
        cur7.execute("SELECT Idnum FROM studentnormal  WHERE Status = '%s'" % i)
        idnum = []
        for row1 in cur7.fetchall():
            list = []
            for i in row1:
                list.append(i)
                idnum.append(list)
        print(idnum)

        cur8 = register1.cursor()
        cur8.execute("SELECT Grade FROM studentnormal  WHERE Status = '%s'" % i)
        grade = []
        for row1 in cur8.fetchall():
            list = []
            for i in row1:
                list.append(i)
                grade.append(list)
        print(grade)

        cur9 = register1.cursor()
        cur9.execute("SELECT Email FROM studentnormal  WHERE Status = '%s'" % i)
        email = []
        for row1 in cur9.fetchall():
            list = []
            for i in row1:
                list.append(i)
                email.append(list)
        print(email)

        cur10 = register1.cursor()
        cur10.execute("SELECT Tel FROM studentnormal  WHERE Status = '%s'" % i)
        tel = []
        for row1 in cur10.fetchall():
            list = []
            for i in row1:
                list.append(i)
                tel.append(list)
        print(tel)

        cur11 = register1.cursor()
        cur11.execute("SELECT Subject FROM studentnormal  WHERE Status = '%s'" % i)
        subject = []
        for row1 in cur11.fetchall():
            list = []
            for i in row1:
                list.append(i)
                subject.append(list)
        print(subject)

        cur12 = register1.cursor()
        cur12.execute("SELECT AccountNum FROM studentnormal  WHERE Status = '%s'" % i)
        Accnum = []
        for row1 in cur12.fetchall():
            list = []
            for i in row1:
                list.append(i)
                Accum.append(list)
        print(Accnum)

        cur13 = register1.cursor()
        cur13.execute("SELECT Attribute FROM studentnormal  WHERE Status = '%s'" % i)
        Attri = []
        for row1 in cur13.fetchall():
            list = []
            for i in row1:
                list.append(i)
                Attri.append(list)
        print(Attri)

        return (render_template('Admin/Show_register3_admin.html',name = Name,surname = surname,department = department , branch = branch ,degree = degree ,level = level ,idnum = idnum ,grade = grade,email = email ,tel = tel ,subject = subject , Accnum = Accnum,Attri=Attri))

@app.route('/Show_Teacherwant_Admin')
def Show_Teacherwant_Admin():
    input = dict(request.form.items())
    print(input)
    #print ('kkkkkkk')
    teacher = It.connect("databaseall.db")
    cur4 = teacher.cursor()
    cur4.execute("SELECT Subject FROM teacherwant ")
    Subject = []
    for row1 in cur4.fetchall():
        list = []
        for i in row1:
            list.append(i)
            Subject.append(list)
    print (Subject)

    cur5 = teacher.cursor()
    cur5.execute("SELECT Numwant FROM teacherwant ")
    Num = []
    for row1 in cur5.fetchall():
        list = []
        for i in row1:
            list.append(i)
            Num.append(list)
    print (Num)

    cur6 = teacher.cursor()
    cur6.execute("SELECT Level FROM teacherwant ")
    Level = []
    for row1 in cur6.fetchall():
        list = []
        for i in row1:
            list.append(i)
            Level.append(list)
    print (Level)

    cur7 = teacher.cursor()
    cur7.execute("SELECT Grade FROM teacherwant ")
    Grade = []
    for row1 in cur7.fetchall():
        list = []
        for i in row1:
            list.append(i)
            Grade.append(list)
    print (Grade)

    cur8 = teacher.cursor()
    cur8.execute("SELECT Attribute FROM teacherwant ")
    Attri = []
    for row1 in cur8.fetchall():
        list = []
        for i in row1:
            list.append(i)
            Attri.append(list)
    print(Attri)

    cur9 = teacher.cursor()
    cur9.execute("SELECT Syllabus FROM teacherwant ")
    Syllabus = []
    for row1 in cur9.fetchall():
        list = []
        for i in row1:
            list.append(i)
            Syllabus.append(list)
    print (Syllabus)

    return (render_template('Admin/Show_Teacherwant_Ad.html',Subject =Subject,Num=Num,Level=Level,Grade=Grade,Attri = Attri,Syllabus = Syllabus))

@app.route('/Show_inforTA_Teacher')
def Show_inforTA_Teacher():
    teacher = It.connect("databaseall.db")
    cur2 = teacher.cursor()
    cur2.execute("SELECT Subject FROM teacher WHERE Username = '%s'" % a.username)
    subject =[]
    for row1 in cur2.fetchall():
        list = []
        for i in row1:
            list.append(i)
            subject.append(list)
    print(subject)
    for j in subject:
        for i in j :
            student = It.connect("databaseall.db")
            cur3 = student.cursor()
            cur3.execute("SELECT Name FROM student WHERE Subject = '%s'" % i)
            name =[]
            for row1 in cur3.fetchall():
                list = []
                for i in row1:
                    list.append(i)
                    name.append(list)
            print (name)

            cur4 = teacher.cursor()
            cur4.execute("SELECT Surname FROM student WHERE Subject = '%s'" % i)
            surname =[]
            for row1 in cur4.fetchall():
                list = []
                for i in row1:
                    list.append(i)
                    surname.append(list)
            print (surname)

            cur5 = teacher.cursor()
            cur5.execute("SELECT IDNUMBER FROM student WHERE Subject = '%s'" % i)
            IDnumber =[]
            for row1 in cur5.fetchall():
                list = []
                for i in row1:
                    list.append(i)
                    IDnumber.append(list)
            print (IDnumber)

            cur6 = teacher.cursor()
            cur6.execute("SELECT Level FROM student WHERE Subject = '%s'" % i)
            level=[]
            for row1 in cur6.fetchall():
                list = []
                for i in row1:
                    list.append(i)
                    level.append(list)
            print (level)

            cur7 = teacher.cursor()
            cur7.execute("SELECT Department FROM student WHERE Subject = '%s'" % i)
            departmant =[]
            for row1 in cur7.fetchall():
                list = []
                for i in row1:
                    list.append(i)
                    departmant.append(list)
            print(departmant)

            cur8 = teacher.cursor()
            cur8.execute("SELECT Grade FROM student WHERE Subject = '%s'" % i)
            grade =[]
            for row1 in cur8.fetchall():
                list = []
                for i in row1:
                    list.append(i)
                    grade.append(list)
            print(grade)

            cur9 = teacher.cursor()
            cur9.execute("SELECT Tel FROM student WHERE Subject = '%s'" % i)
            tel =[]
            for row1 in cur9.fetchall():
                list = []
                for i in row1:
                    list.append(i)
                    tel.append(list)
            print(tel)

            cur10 = teacher.cursor()
            cur10.execute("SELECT Email FROM student WHERE Subject = '%s'" % i)
            email =[]
            for row1 in cur10.fetchall():
                list = []
                for i in row1:
                    list.append(i)
                    email.append(list)
            print(email)
    return (render_template("Aj/Show_inforTA.html",subject = subject ,name = name,surname = surname , IDnumber = IDnumber , level = level , department = departmant ,grade = grade,tel = tel,email = email))

@app.route('/TA_working_form')
def TA_working_form_TA():
    if(a.type_user == 'student'):
        return(render_template('TA/WorkingForm_TA_v4_ta.html'))
    if(a.type_user == 'teacher'):
        timesheets = It.connect("databaseall.db")
        timesheetcur = timesheets.cursor()
        subject = It.connect("databaseall.db")
        subjectcur = subject.cursor()
        subjectcur.execute("SELECT Subject FROM teacher WHERE Username='%s'" % a.username)
        print(a.username)
        subjectteacher = []

        for pdfrow in subjectcur.fetchall():
            pdflist = []
            for i in pdfrow:
                pdflist.append(i)
                subjectteacher.append(i)
        name = []
        for i in subjectteacher:
            timesheetcur.execute("SELECT Username FROM timesheet WHERE ID ='1'and Subject ='%s' and StatusAj!='1'" % i)
            for pdfrow in timesheetcur.fetchall():
                pdflist = []
                for i in pdfrow:
                    name.append(i)
        print(name)
        return (render_template('Aj/choose_workingForm1.html', name=name))
    if (a.type_user == 'admin'):
        timesheets = It.connect("databaseall.db")
        timesheetcur = timesheets.cursor()
        nameFRA121 = []
        timesheetcur.execute("SELECT Username FROM timesheet WHERE ID ='1'and Subject='FRA121' and StatusAdmin='0' and StatusTa='1'")
        for pdfrow in timesheetcur.fetchall():
            for i in pdfrow:
                nameFRA121.append(i)
        timesheets = It.connect("databaseall.db")
        timesheetcur = timesheets.cursor()
        nameFRA161 = []
        timesheetcur.execute("SELECT Username FROM timesheet WHERE ID ='1'and Subject='FRA161'and StatusAdmin='0' and StatusTa='1'")
        for pdfrow in timesheetcur.fetchall():
            for i in pdfrow:
                nameFRA161.append(i)
        nameFRA221 = []
        timesheetcur.execute("SELECT Username FROM timesheet WHERE ID ='1'and Subject='FRA221'and StatusAdmin='0' and StatusTa='1'")
        for pdfrow in timesheetcur.fetchall():
            for i in pdfrow:
                nameFRA221.append(i)
        nameFRA222 = []
        timesheetcur.execute("SELECT Username FROM timesheet WHERE ID ='1'and Subject='FRA221'and StatusAdmin='0' and StatusTa='1'")
        for pdfrow in timesheetcur.fetchall():
            for i in pdfrow:
                nameFRA222.append(i)
        return (render_template('Admin/adminchooseworkform1.html', nameFRA161=nameFRA161, nameFRA121=nameFRA121,
                                nameFRA221=nameFRA222, nameFRA222=nameFRA222))
        nameFRA231 = []
        timesheetcur.execute("SELECT Username FROM timesheet WHERE ID ='1'and StatusAdmin='0' and StatusTa='1'")
        for pdfrow in timesheetcur.fetchall():
            for i in pdfrow:
                nameFRA231.append(i)
        return (render_template('Admin/adminchooseworkform1.html', nameFRA161=nameFRA161, nameFRA121=nameFRA121,
                                nameFRA221=nameFRA222, nameFRA222=nameFRA222, nameFRA231=nameFRA231))
        nameFRA241 = []
        timesheetcur.execute("SELECT Username FROM timesheet WHERE ID ='1'and Subject='FRA221'and StatusAdmin='0' and StatusTa='1'")
        for pdfrow in timesheetcur.fetchall():
            for i in pdfrow:
                nameFRA241.append(i)
        return (render_template('Admin/adminchooseworkform1.html', nameFRA161=nameFRA161, nameFRA121=nameFRA121,
                                nameFRA221=nameFRA222, nameFRA222=nameFRA222, nameFRA231=nameFRA231,
                                nameFRA241=nameFRA241))
        nameFRA261 = []
        timesheetcur.execute("SELECT Username FROM timesheet WHERE ID ='1'and Subject='FRA221'and StatusAdmin='0' and StatusTa='1'")
        for pdfrow in timesheetcur.fetchall():
            for i in pdfrow:
                nameFRA261.append(i)
        return (render_template('Admin/adminchooseworkform1.html', nameFRA161=nameFRA161, nameFRA121=nameFRA121,
                                nameFRA221=nameFRA222, nameFRA222=nameFRA222, nameFRA231=nameFRA231,
                                nameFRA241=nameFRA241, nameFRA261=nameFRA261))
        nameFRA321 = []
        timesheetcur.execute("SELECT Username FROM timesheet WHERE ID ='1'and Subject='FRA221'and StatusAdmin='0' and StatusTa='1'")
        for pdfrow in timesheetcur.fetchall():
            for i in pdfrow:
                nameFRA321.append(i)
        return (render_template('Admin/adminchooseworkform1.html', nameFRA161=nameFRA161, nameFRA121=nameFRA121,
                                nameFRA221=nameFRA222, nameFRA222=nameFRA222, nameFRA231=nameFRA231,
                                nameFRA241=nameFRA241, nameFRA261=nameFRA261, nameFRA321=nameFRA321))
        nameFRA331 = []
        timesheetcur.execute("SELECT Username FROM timesheet WHERE ID ='1'and Subject='FRA221'and StatusAdmin='0' and StatusTa='1'")
        for pdfrow in timesheetcur.fetchall():
            for i in pdfrow:
                nameFRA331.append(i)
        return (render_template('Admin/adminchooseworkform1.html', nameFRA161=nameFRA161, nameFRA121=nameFRA121,
                                nameFRA221=nameFRA222, nameFRA222=nameFRA222, nameFRA231=nameFRA231,
                                nameFRA241=nameFRA241, nameFRA261=nameFRA261, nameFRA321=nameFRA321,
                                nameFRA331=nameFRA331))
        nameFRA332 = []
        timesheetcur.execute("SELECT Username FROM timesheet WHERE ID ='1'and Subject='FRA221'and StatusAdmin='0' and StatusTa='1'")
        for pdfrow in timesheetcur.fetchall():
            for i in pdfrow:
                nameFRA332.append(i)
        return (render_template('Admin/adminchooseworkform1.html', nameFRA161=nameFRA161, nameFRA121=nameFRA121,
                                nameFRA221=nameFRA222, nameFRA222=nameFRA222, nameFRA231=nameFRA231,
                                nameFRA241=nameFRA241, nameFRA261=nameFRA261, nameFRA321=nameFRA321,
                                nameFRA331=nameFRA331, nameFRA332=nameFRA332))
        nameFRA341 = []
        timesheetcur.execute("SELECT Username FROM timesheet WHERE ID ='1'and Subject='FRA221'and StatusAdmin='0' and StatusTa='1'")
        for pdfrow in timesheetcur.fetchall():
            for i in pdfrow:
                nameFRA341.append(i)
        return (render_template('Admin/adminchooseworkform1.html', nameFRA161=nameFRA161, nameFRA121=nameFRA121,
                                nameFRA221=nameFRA222, nameFRA222=nameFRA222, nameFRA231=nameFRA231,
                                nameFRA241=nameFRA241, nameFRA261=nameFRA261, nameFRA321=nameFRA321,
                                nameFRA331=nameFRA331, nameFRA332=nameFRA332, nameFRA341=nameFRA341))
        nameFRA451 = []
        timesheetcur.execute("SELECT Username FROM timesheet WHERE ID ='1'and Subject='FRA221'and StatusAdmin='0' and StatusTa='1'")
        for pdfrow in timesheetcur.fetchall():
            for i in pdfrow:
                nameFRA451.append(i)
        return (render_template('Admin/adminchooseworkform1.html', nameFRA161=nameFRA161, nameFRA121=nameFRA121,
                                nameFRA221=nameFRA222, nameFRA222=nameFRA222, nameFRA231=nameFRA231,
                                nameFRA241=nameFRA241, nameFRA261=nameFRA261, nameFRA321=nameFRA321,
                                nameFRA331=nameFRA331, nameFRA332=nameFRA332, nameFRA341=nameFRA341,
                                nameFRA451=nameFRA451))
        nameFRA452 = []
        timesheetcur.execute("SELECT Username FROM timesheet WHERE ID ='1'and Subject='FRA221'and StatusAdmin='0' and StatusTa='1'")
        for pdfrow in timesheetcur.fetchall():
            for i in pdfrow:
                nameFRA452.append(i)
        return (render_template('Admin/adminchooseworkform1.html', nameFRA161=nameFRA161, nameFRA121=nameFRA121,
                                nameFRA221=nameFRA222, nameFRA222=nameFRA222, nameFRA231=nameFRA231,
                                nameFRA241=nameFRA241, nameFRA261=nameFRA261, nameFRA321=nameFRA321,
                                nameFRA331=nameFRA331, nameFRA332=nameFRA332, nameFRA341=nameFRA341,
                                nameFRA451=nameFRA451, nameFRA452=nameFRA452))
        return (render_template('Admin/adminchooseworkform1.html', nameFRA161=nameFRA161,nameFRA121=nameFRA121,nameFRA221=nameFRA221))

@app.route('/notification')
def notification():
    return("notification")

@app.route('/login', methods=["POST"])
def login():
    input = dict(request.form.items())
    #print(input)
    username = input['username']
    password = input['password']
    print(username,password)
    list_username = DB.login(username)
    #print(list_username)
    type_user = False
    for i in list_username:
        if (username == i[0] and password == i[1]):
            type_user = (i[2])
            break
    if(type_user == 'teacher'):
        a.username = input['username']
        a.type_user = 'teacher'
    if(type_user == 'student'):
        a.username = input['username']
        a.type_user = 'student'
    if (type_user == 'admin'):
        a.username = input['username']
        a.type_user = 'admin'
    return(home())

@app.route('/logout')
def logout():
    a.type_user = None
    return(index())

@app.route('/forgot_password')
def forgot_password():
    return(render_template('Po/forgot password_po.html'))

@app.route('/register')
def register():
    if(a.type_user == None):
        return(render_template('Po/Register_po.html'))

@app.route("/Register")
def Register():
    return(render_template("Po/Register_po.html"))

@app.route("/Register_forTA")
def Register_forTA():
    return(render_template("TA/Register_ta.html"))

@app.route("/Register_forAJ")
def Register_forAJ():
    return(render_template("AJ/Register_aj.html"))

@app.route("/addregisnormal", methods=['POST'])
def addregisnormal():
    x = dict(request.form.items())
    name = x['name']
    surname = x['surname']
    department = x['department']
    branch = x['branch']
    degree =x['degree']
    level = x['level']
    idnumber = x['idnumber']
    email = x['email']
    tel =x['tel']
    subject = x['subject']
    accountnum = x['accountnum1'] + x['accountnum2'] + x['accountnum3']
    grade = x['grade']
    attribute=x['attribute']

    studentnormal = It.connect("databaseall.db")
    stnormalcur = studentnormal.cursor()
    stnormalcur.execute("INSERT INTO studentnormal(Name,Surname,Department,Branch,Degree,Level,Idnum,Grade,Email,Tel,Subject,AccountNum,Attribute) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", (name,surname,department,branch,degree,level,idnumber,grade,email,tel,subject,accountnum,attribute))
    studentnormal.commit()
    return home()


@app.route('/register_TA',methods=['post'])
def register_TA():
    student = It.connect("databaseall.db")
    cur = student.cursor()
    x = dict(request.form.items())
    #print(x)
    #print(a.username)
    name = x['name']
    surname = x['surname']
    department = x['department']
    level = x['level']
    idnumber = x['idnumber']
    email = x['email']
    #subject = x['subject']
    tel= x['attribute']
    accountnum = x['accountnum1']+x['accountnum2']+x['accountnum3']
    grade = x['grade']
    cur.execute("UPDATE student SET Name= '%s' WHERE Username = '%s'" % (name, a.username))
    cur.execute("UPDATE student SET Surname = '%s' WHERE Username = '%s'" % (surname, a.username))
    cur.execute("UPDATE student SET Level = '%s' WHERE Username = '%s'" % (level, a.username))
    cur.execute("UPDATE student SET IDNUMBER = '%s' WHERE Username = '%s'" % (idnumber, a.username))
    cur.execute("UPDATE student SET Department = '%s' WHERE Username = '%s'" % (department, a.username))
    cur.execute("UPDATE student SET Grade = '%s' WHERE Username = '%s'" % (grade, a.username))
    cur.execute("UPDATE student SET Tel = '%s' WHERE Username = '%s'" % (tel, a.username))
    cur.execute("UPDATE student SET Email = '%s' WHERE Username = '%s'" % (email, a.username))
    cur.execute("UPDATE student SET AccountNum = '%s' WHERE Username = '%s'" % (accountnum, a.username))
    #cur.execute("UPDATE student SET Subject = '%s' WHERE Username = '%s'" % (subject, a.username))
    student.commit()
    student.close()
    #test = DB()
    #test.printxx()
    #test.register('US1',name,surname,idnumber,level,department,grade,tel,email,accountnum,subject)
    #return "name : %s Surname : %s: Department %s: Year %s: IDnumber %s: Email %s"%(name,surname,department,level,idnumber,email)
    return(profile())

@app.route("/addworkingform", methods=['POST'])
def addworking():
    print('kkkkkk')
    username = a.username
    x = dict(request.form.items())
    #print(x)
    dmy = x['dmy']
    timecome = x['timecome']
    timeback = x['timeback']
    whatdo = x['whatdo']
    dmy2 = x['dmy2']
    timecome2 = x['timecome2']
    timeback2 = x['timeback2']
    whatdo2 = x['whatdo2']
    day3 = x['day3']
    timecome3 = x['timecome3']
    timeback3 = x['timeback3']
    whatdo3 = x['whatdo3']
    dmy4= x['dmy4']
    timecome4 = x['timecome4']
    timeback4 = x['timeback4']
    whatdo4 = x['whatdo4']
    day5 = x['day5']
    timecome5 = x['timecome5']
    timeback5 = x['timeback5']
    whatdo5 = x['whatdo5']
    dmy6 = x['dmy6']
    timecome6 = x['timecome6']
    timeback6 = x['timeback6']
    whatdo6 = x['whatdo6']
    dmy7 = x['dmy7']
    timecome7 = x['timecome7']
    timeback7 = x['timeback7']
    whatdo7 = x['whatdo7']
    dmy8 = x['dmy8']
    timecome8 = x['timecome8']
    timeback8 = x['timeback8']
    whatdo8 = x['whatdo8']
    for i in x:
        if i == 'printworkingForm':
            printworkingForm = x['printworkingForm']
            student = It.connect("databaseall.db")
            cur = student.cursor()
            cur.execute(
                "SELECT Name,Surname,Subject,Department,Level,Grade,Tel,Email FROM student WHERE Username='%s'" % username)
            pdf = []
            for pdfrow in cur.fetchall():
                pdflist = []
                for i in pdfrow:
                    pdflist.append(i)
                pdf.append(pdflist)
            timesheets = It.connect("databaseall.db")
            timesheetcur = timesheets.cursor()
            timesheetcur.execute(
                "SELECT DayMonthYear ,Timecome,Timeback, StatusAj ,whatdo FROM timesheet WHERE Username='%s'" % username)
            pdfwork = []
            for pdfrow in timesheetcur.fetchall():
                pdflist = []
                for i in pdfrow:
                    pdflist.append(i)
                pdfwork.append(pdflist)

            #pdfwork[0][3] == '0' and
            if printworkingForm == 'print'and pdfwork[0][3] == '1':
                pdfcreate = canvas.Canvas('%s.pdf' % username)
                pdfcreate.drawString(100, 800, 'INSTITUTE OF FIELD ROBOTICS STUDENT WORKING HOUR FORM ')
                pdfcreate.drawString(210, 770, 'SEMESTER : 1  YEAR : 2560')
                pdfcreate.drawString(130, 740, 'KING MONGKUT UNIVERSITY OF TECHNOLOGY THONBURI')
                pdfcreate.drawString(80, 710, '==============================================================')
                pdfcreate.drawString(50, 680, 'Name :')
                #print(username)
                #print(pdf)
                #print(pdfwork)
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

                pdfcreate.drawString(450, 590, 'Workingdata')

                pdfcreate.drawString(50, 560, 'Day/Month/Year :')
                pdfcreate.drawString(200, 560, pdfwork[0][0])
                pdfcreate.drawString(350, 560, 'Timecome :')
                pdfcreate.drawString(420, 560, pdfwork[0][1])
                pdfcreate.drawString(450, 560, 'Timeback :')
                pdfcreate.drawString(520, 560, pdfwork[0][2])
                pdfcreate.drawString(50, 530, 'Day/Month/Year :')
                pdfcreate.drawString(200, 530, pdfwork[1][0])
                pdfcreate.drawString(350, 530, 'Timecome :')
                pdfcreate.drawString(420, 530, pdfwork[1][1])
                pdfcreate.drawString(450, 530, 'Timeback :')
                pdfcreate.drawString(520, 530, pdfwork[1][2])
                pdfcreate.drawString(50, 500, 'Day/Month/Year :')
                pdfcreate.drawString(200, 500, pdfwork[2][0])
                pdfcreate.drawString(350, 500, 'Timecome :')
                pdfcreate.drawString(420, 500, pdfwork[2][1])
                pdfcreate.drawString(450, 500, 'Timeback :')
                pdfcreate.drawString(520, 500, pdfwork[2][2])
                pdfcreate.drawString(50, 470, 'Day/Month/Year :')
                pdfcreate.drawString(200, 470, pdfwork[3][0])
                pdfcreate.drawString(350, 470, 'Timecome :')
                pdfcreate.drawString(420, 470, pdfwork[3][1])
                pdfcreate.drawString(450, 470, 'Timeback :')
                pdfcreate.drawString(520, 470, pdfwork[3][2])
                pdfcreate.drawString(50, 440, 'Day/Month/Year :')
                pdfcreate.drawString(200, 440, pdfwork[4][0])
                pdfcreate.drawString(350, 440, 'Timecome :')
                pdfcreate.drawString(420, 440, pdfwork[4][1])
                pdfcreate.drawString(450, 440, 'Timeback :')
                pdfcreate.drawString(520, 440, pdfwork[4][2])
                pdfcreate.drawString(50, 410, 'Day/Month/Year :')
                pdfcreate.drawString(200, 410, pdfwork[5][0])
                pdfcreate.drawString(350, 410, 'Timecome :')
                pdfcreate.drawString(420, 410, pdfwork[5][1])
                pdfcreate.drawString(450, 410, 'Timeback :')
                pdfcreate.drawString(520, 410, pdfwork[5][2])
                pdfcreate.drawString(50, 380, 'Day/Month/Year :')
                pdfcreate.drawString(200, 380, pdfwork[6][0])
                pdfcreate.drawString(350, 380, 'Timecome :')
                pdfcreate.drawString(420, 380, pdfwork[6][1])
                pdfcreate.drawString(450, 380, 'Timeback :')
                pdfcreate.drawString(520, 380, pdfwork[6][2])
                pdfcreate.drawString(50, 350, 'Day/Month/Year :')
                pdfcreate.drawString(200, 350, pdfwork[7][0])
                pdfcreate.drawString(350, 350, 'Timecome :')
                pdfcreate.drawString(420, 350, pdfwork[7][1])
                pdfcreate.drawString(450, 350, 'Timeback :')
                pdfcreate.drawString(520, 350, pdfwork[7][2])
                pdfcreate.drawString(400, 320, '.......................')
                pdfcreate.save()

                pdfcreate2 = canvas.Canvas('%sP2.pdf' % username)
                pdfcreate2.drawString(100, 800, 'Job Description ')
                pdfcreate2.drawString(50, 770, pdfwork[0][0])
                pdfcreate2.drawString(200, 770, pdfwork[0][4])
                pdfcreate2.drawString(50, 740, pdfwork[1][0])
                pdfcreate2.drawString(200, 740, pdfwork[1][4])
                pdfcreate2.drawString(50, 710, pdfwork[2][0])
                pdfcreate2.drawString(200, 710, pdfwork[2][4])
                pdfcreate2.drawString(50, 680, pdfwork[3][0])
                pdfcreate2.drawString(200, 680, pdfwork[3][4])
                pdfcreate2.drawString(50, 650, pdfwork[4][0])
                pdfcreate2.drawString(200, 650, pdfwork[4][4])
                pdfcreate2.drawString(50, 620, pdfwork[5][0])
                pdfcreate2.drawString(200, 620, pdfwork[5][4])
                pdfcreate2.drawString(50, 590, pdfwork[6][0])
                pdfcreate2.drawString(200, 590, pdfwork[6][4])
                pdfcreate2.drawString(50, 560, pdfwork[7][0])
                pdfcreate2.drawString(200, 560, pdfwork[7][4])
                pdfcreate2.save()


                os.startfile('%s.pdf' % username)
                os.startfile('%sP2.pdf' % username)


            else:
                return 'plz wait AJ comment'


        if i == 'save_workingForm':
            timesheets = It.connect("databaseall.db")
            timesheetcur = timesheets.cursor()
            timesheetcur.execute("SELECT DayMonthYear ,TimeCome,TimeBack FROM timesheet WHERE Username='%s'" % username)
            pdf = []
            for pdfrow in timesheetcur.fetchall():
                pdflist = []
                for i in pdfrow:
                    pdflist.append(i)
                pdf.append(pdflist)
            subject = It.connect("databaseall.db")
            subjectcur = subject.cursor()
            subjectcur.execute("SELECT Subject FROM student WHERE Username='%s'" % username)
            subject = []
            for pdfrow in subjectcur.fetchall():
                pdflist = []
                for i in pdfrow:
                    pdflist.append(i)
                subject.append(pdflist)
            if len(pdf) == 0:
                timesheets = It.connect("databaseall.db")
                timesheetcur = timesheets.cursor()
                print(subject)
                print("Hi")
                timesheetcur.execute("INSERT INTO timesheet(ID,Username,DayMonthYear,TimeCome,TimeBack,Whatdo,Subject,StatusTa,StatusAdmin,StatusAj ) VALUES(?,?,?,?,?,?,?,?,?,?)",("1",username, dmy, timecome, timeback, whatdo,str(subject[0][0]),'1','0','0'))
                timesheets.commit()


                timesheetcur.execute("INSERT INTO timesheet(ID,Username,DayMonthYear,TimeCome,TimeBack,Whatdo ) VALUES(?,?,?,?,?,?)",
                                         ("2",username, dmy2, timecome2, timeback2, whatdo2))
                timesheetcur.execute("INSERT INTO timesheet(ID,Username,DayMonthYear,TimeCome,TimeBack,Whatdo ) VALUES(?,?,?,?,?,?)",
                                         ("3",username, day3, timecome3, timeback3, whatdo3))
                timesheetcur.execute("INSERT INTO timesheet(ID,Username,DayMonthYear,TimeCome,TimeBack,Whatdo ) VALUES(?,?,?,?,?,?)",
                                         ("4",username, dmy4, timecome4, timeback4, whatdo4))
                timesheetcur.execute("INSERT INTO timesheet(ID,Username,DayMonthYear,TimeCome,TimeBack,Whatdo ) VALUES(?,?,?,?,?,?)",
                                         ("5",username, day5, timecome5, timeback5, whatdo5))
                timesheetcur.execute("INSERT INTO timesheet(ID,Username,DayMonthYear,TimeCome,TimeBack,Whatdo ) VALUES(?,?,?,?,?,?)",
                                         ("6",username, dmy6, timecome6, timeback6, whatdo6))
                timesheetcur.execute("INSERT INTO timesheet(ID,Username,DayMonthYear,TimeCome,TimeBack,Whatdo ) VALUES(?,?,?,?,?,?)",
                                         ("7",username, dmy7, timecome7, timeback7, whatdo7))
                timesheetcur.execute("INSERT INTO timesheet(ID,Username,DayMonthYear,TimeCome,TimeBack,Whatdo ) VALUES(?,?,?,?,?,?)",
                                         ("8",username, dmy8, timecome8, timeback8, whatdo8))
                timesheets.commit()
            else:
                timesheetcur.execute("UPDATE timesheet SET Subject = '%s' WHERE Username = '%s'and ID = '1'" % (str(subject[0][0]), username))
                timesheetcur.execute("UPDATE timesheet SET TimeCome = '%s' WHERE Username = '%s'and ID = '1'" % (timecome, username))
                timesheetcur.execute("UPDATE timesheet SET TimeBack = '%s' WHERE Username = '%s'and ID = '1'" % (timeback, username))
                timesheetcur.execute("UPDATE timesheet SET DayMonthYear = '%s' WHERE Username = '%s'and ID = '1'" % (dmy, username))
                timesheetcur.execute("UPDATE timesheet SET Whatdo = '%s' WHERE Username = '%s'and ID = '1'" % (whatdo, username))

                timesheetcur.execute("UPDATE timesheet SET TimeCome = '%s' WHERE Username = '%s'and ID = '2'" % (timecome2, username))
                timesheetcur.execute("UPDATE timesheet SET TimeBack = '%s' WHERE Username = '%s'and ID = '2'" % (timeback2, username))
                timesheetcur.execute("UPDATE timesheet SET DayMonthYear = '%s' WHERE Username = '%s'and ID = '2'" % (dmy2, username))
                timesheetcur.execute("UPDATE timesheet SET Whatdo = '%s' WHERE Username = '%s'and ID = '2'" % (whatdo2, username))
                timesheetcur.execute("UPDATE timesheet SET TimeCome = '%s' WHERE Username = '%s'and ID = '3'" % (timecome3, username))
                timesheetcur.execute("UPDATE timesheet SET TimeBack = '%s' WHERE Username = '%s'and ID = '3'" % (timeback3, username))
                timesheetcur.execute("UPDATE timesheet SET DayMonthYear = '%s' WHERE Username = '%s'and ID = '3'" % (day3, username))
                timesheetcur.execute("UPDATE timesheet SET Whatdo = '%s' WHERE Username = '%s'and ID = '3'" % (whatdo3, username))
                timesheetcur.execute("UPDATE timesheet SET TimeCome = '%s' WHERE Username = '%s'and ID = '4'" % (timecome4, username))
                timesheetcur.execute("UPDATE timesheet SET TimeBack = '%s' WHERE Username = '%s'and ID = '4'" % (timeback4, username))
                timesheetcur.execute("UPDATE timesheet SET DayMonthYear = '%s' WHERE Username = '%s'and ID = '4'" % (dmy4, username))
                timesheetcur.execute("UPDATE timesheet SET Whatdo = '%s' WHERE Username = '%s'and ID = '4'" % (whatdo4, username))
                timesheetcur.execute(
                    "UPDATE timesheet SET TimeCome = '%s' WHERE Username = '%s'and ID = '5'" % (timecome5, username))
                timesheetcur.execute(
                    "UPDATE timesheet SET TimeBack = '%s' WHERE Username = '%s'and ID = '5'" % (timeback5, username))
                timesheetcur.execute(
                    "UPDATE timesheet SET DayMonthYear = '%s' WHERE Username = '%s'and ID = '5'" % (day5, username))
                timesheetcur.execute(
                    "UPDATE timesheet SET Whatdo = '%s' WHERE Username = '%s'and ID = '5'" % (whatdo5, username))
                timesheetcur.execute(
                    "UPDATE timesheet SET TimeCome = '%s' WHERE Username = '%s'and ID = '6'" % (timecome6, username))
                timesheetcur.execute(
                    "UPDATE timesheet SET TimeBack = '%s' WHERE Username = '%s'and ID = '6'" % (timeback6, username))
                timesheetcur.execute(
                    "UPDATE timesheet SET DayMonthYear = '%s' WHERE Username = '%s'and ID = '6'" % (dmy6, username))
                timesheetcur.execute(
                    "UPDATE timesheet SET Whatdo = '%s' WHERE Username = '%s'and ID = '6'" % (whatdo6, username))
                timesheetcur.execute(
                    "UPDATE timesheet SET TimeCome = '%s' WHERE Username = '%s'and ID = '7'" % (timecome7, username))
                timesheetcur.execute(
                    "UPDATE timesheet SET TimeBack = '%s' WHERE Username = '%s'and ID = '7'" % (timeback7, username))
                timesheetcur.execute(
                    "UPDATE timesheet SET DayMonthYear = '%s' WHERE Username = '%s'and ID = '7'" % (dmy7, username))
                timesheetcur.execute(
                    "UPDATE timesheet SET Whatdo = '%s' WHERE Username = '%s'and ID = '7'" % (whatdo7, username))
                timesheetcur.execute(
                    "UPDATE timesheet SET TimeCome = '%s' WHERE Username = '%s'and ID = '8'" % (timecome8, username))
                timesheetcur.execute(
                    "UPDATE timesheet SET TimeBack = '%s' WHERE Username = '%s'and ID = '8'" % (timeback8, username))
                timesheetcur.execute(
                    "UPDATE timesheet SET DayMonthYear = '%s' WHERE Username = '%s'and ID = '8'" % (dmy8, username))
                timesheetcur.execute(
                    "UPDATE timesheet SET Whatdo = '%s' WHERE Username = '%s'and ID = '8'" % (whatdo8, username))
                timesheetcur.execute("UPDATE timesheet SET StatusTa = '1' WHERE Username = '%s'and ID = '1'" % (username))
                timesheetcur.execute("UPDATE timesheet SET StatusAdmin = '0' WHERE Username = '%s'and ID = '1'" % (username))
                timesheetcur.execute("UPDATE timesheet SET StatusAj = '0' WHERE Username = '%s'and ID = '1'" % (username))
                timesheets.commit()

    return(home())

@app.route('/Teacherworkformnew')
def teacherworkformnew():
    timesheets = It.connect("databaseall.db")
    timesheetcur = timesheets.cursor()
    subject = It.connect("databaseall.db")
    subjectcur = subject.cursor()
    subjectcur.execute("SELECT Subject FROM teacher WHERE Username='%s'" % username)
    print(username)
    subject = []
    for pdfrow in subjectcur.fetchall():
        pdflist = []
        for i in pdfrow:
            pdflist.append(i)
        subject.append(pdflist)
    print(subject[0][0])
    timesheetcur.execute("SELECT Username FROM timesheet WHERE ID ='1'")
    name = []
    for pdfrow in timesheetcur.fetchall():
        pdflist = []
        for i in pdfrow:
            pdflist.append(i)
            name.append(pdflist)
    return (render_template("Aj/WorkingFormselectnew.html",name=name))


@app.route('/adminselectnew' , methods= ['post'])
def adselectnew():
    datawork = It.connect("databaseall.db")
    dataworkcur = datawork.cursor()
    x = dict(request.form.items())

    nameta = []
    for i in x:
        nameta.append(i)

    dataworkcur.execute("SELECT DayMonthYear FROM timesheet WHERE Username='%s'" % nameta[0])
    daymonthyear = []
    for pdfrow in dataworkcur.fetchall():
        pdflist = []
        for i in pdfrow:
            pdflist.append(i)
            daymonthyear.append(pdflist)

    dataworkcur.execute("SELECT TimeCome FROM timesheet WHERE Username='%s'" % nameta[0])
    timecome = []
    for pdfrow in dataworkcur.fetchall():
        pdflist = []
        for i in pdfrow:
            pdflist.append(i)
            timecome.append(pdflist)

    dataworkcur.execute("SELECT TimeBack FROM timesheet WHERE Username='%s'" % nameta[0])
    timeback = []
    for pdfrow in dataworkcur.fetchall():
        pdflist = []
        for i in pdfrow:
            pdflist.append(i)
            timeback.append(pdflist)

    dataworkcur.execute("SELECT whatdo FROM timesheet WHERE Username='%s'" % nameta[0])
    whatdo = []
    for pdfrow in dataworkcur.fetchall():
        pdflist = []
        for i in pdfrow:
            pdflist.append(i)
            whatdo.append(pdflist)
    print(nameta[0])
    print('testtesttest')
    nametashow = nameta[0]
    dataworkcur.execute("SELECT Name FROM student WHERE Username ='%s' " % nametashow)
    name = []
    for pdfrow in dataworkcur.fetchall():
        for i in pdfrow:
            name.append(i)
    dataworkcur.execute("SELECT Surname FROM student WHERE Username ='%s' " % nametashow)
    surname = []
    for pdfrow in dataworkcur.fetchall():
        for i in pdfrow:
            surname.append(i)
    dataworkcur.execute("SELECT IDNUMBER FROM student WHERE Username ='%s' " % nametashow)
    idnum = []
    for pdfrow in dataworkcur.fetchall():
        for i in pdfrow:
            idnum.append(i)
    dataworkcur.execute("SELECT Level FROM student WHERE Username ='%s' " % nametashow)
    level = []
    for pdfrow in dataworkcur.fetchall():
        for i in pdfrow:
            level.append(i)
    dataworkcur.execute("SELECT Department FROM student WHERE Username ='%s' " % nametashow)
    department = []
    for pdfrow in dataworkcur.fetchall():
        for i in pdfrow:
            department.append(i)
    dataworkcur.execute("SELECT Tel FROM student WHERE Username ='%s' " % nametashow)
    Tel = []
    for pdfrow in dataworkcur.fetchall():
        for i in pdfrow:
            Tel.append(i)
    dataworkcur.execute("SELECT Email FROM student WHERE Username ='%s' " % nametashow)
    Email = []
    for pdfrow in dataworkcur.fetchall():
        for i in pdfrow:
            Email.append(i)
    print(daymonthyear)
    print(name[0])
    return (render_template("Admin/showWorkingForm_Admin1.html",name=name[0],surname=surname[0],level=level[0],idnum=idnum[0],nametashow=nametashow,department=department[0],Tel=Tel[0],Email=Email[0], daymonthyear=daymonthyear,
                            timecome=timecome, timeback=timeback, whatdo=whatdo))
@app.route('/admincomment' , methods= ['get','post'])
def admincomment():
    datawork = It.connect("databaseall.db")
    dataworkcur = datawork.cursor()
    x = dict(request.form.items())
    print(x)
    listdata=[]
    for i in x:
        listdata.append(i)
    nameta=str(listdata[0])
    comment = x['%s'%(nameta)]
    passfail=str(listdata[1])
    print(nameta)
    print(comment)
    print(passfail)
    if passfail == 'pass':
        dataworkcur.execute("UPDATE timesheet SET StatusAdmin = '%s' WHERE Username = '%s'and ID ='1'" % ('1', nameta))
        dataworkcur.execute("UPDATE timesheet SET Comment = '%s' WHERE Username = '%s' and ID ='1'" % (comment,nameta))

        datawork.commit()
    if passfail == 'notpass':
        dataworkcur.execute("UPDATE timesheet SET StatusAdmin = '%s' WHERE Username = '%s' and ID ='1'" % ('x', nameta))
        dataworkcur.execute("UPDATE timesheet SET Comment = '%s' WHERE Username = '%s' and ID ='1'" % (comment,nameta))
        datawork.commit()
    return(home())

@app.route('/Teacherselectnew' , methods= ['post'])
def selectnew():
    datawork = It.connect("databaseall.db")
    dataworkcur = datawork.cursor()
    x = dict(request.form.items())

    nameta = []
    for i in x:
        nameta.append(i)

    dataworkcur.execute("SELECT DayMonthYear FROM timesheet WHERE Username='%s'" % nameta[0])
    daymonthyear = []
    for pdfrow in dataworkcur.fetchall():
        pdflist = []
        for i in pdfrow:
            pdflist.append(i)
            daymonthyear.append(pdflist)

    dataworkcur.execute("SELECT TimeCome FROM timesheet WHERE Username='%s'" % nameta[0])
    timecome = []
    for pdfrow in dataworkcur.fetchall():
        pdflist = []
        for i in pdfrow:
            pdflist.append(i)
            timecome.append(pdflist)

    dataworkcur.execute("SELECT TimeBack FROM timesheet WHERE Username='%s'" % nameta[0])
    timeback = []
    for pdfrow in dataworkcur.fetchall():
        pdflist = []
        for i in pdfrow:
            pdflist.append(i)
            timeback.append(pdflist)

    dataworkcur.execute("SELECT whatdo FROM timesheet WHERE Username='%s'" % nameta[0])
    whatdo = []
    for pdfrow in dataworkcur.fetchall():
        pdflist = []
        for i in pdfrow:
            pdflist.append(i)
            whatdo.append(pdflist)
    print(daymonthyear)
    print(timecome)
    print(timeback)
    print(whatdo)
    print(nameta[0])
    print('testtesttest')
    nametashow = nameta[0]
    dataworkcur.execute("SELECT Name FROM student WHERE Username ='%s' " % nametashow)
    name = []
    for pdfrow in dataworkcur.fetchall():
        for i in pdfrow:
            name.append(i)
    dataworkcur.execute("SELECT Surname FROM student WHERE Username ='%s' " % nametashow)
    surname = []
    for pdfrow in dataworkcur.fetchall():
        for i in pdfrow:
            surname.append(i)
    dataworkcur.execute("SELECT IDNUMBER FROM student WHERE Username ='%s' " % nametashow)
    idnum = []
    for pdfrow in dataworkcur.fetchall():
        for i in pdfrow:
            idnum.append(i)
    dataworkcur.execute("SELECT Level FROM student WHERE Username ='%s' " % nametashow)
    level = []
    for pdfrow in dataworkcur.fetchall():
        for i in pdfrow:
            level.append(i)
    dataworkcur.execute("SELECT Department FROM student WHERE Username ='%s' " % nametashow)
    Tel = []
    for pdfrow in dataworkcur.fetchall():
        for i in pdfrow:
            Tel.append(i)
    dataworkcur.execute("SELECT Email FROM student WHERE Username ='%s' " % nametashow)
    Email = []
    for pdfrow in dataworkcur.fetchall():
        for i in pdfrow:
            Email.append(i)
    dataworkcur.execute("SELECT Department FROM student WHERE Username ='%s' " % nametashow)
    department = []
    for pdfrow in dataworkcur.fetchall():
        for i in pdfrow:
            department.append(i)
    print(idnum[0])
    print(level[0])


    return (render_template("Aj/showWorkingForm_Aj1.html",name=name[0],surname=surname[0],level=level[0],idnum=idnum[0],department=department[0],nametashow=nametashow,Tel=Tel[0],Email=Email[0], daymonthyear=daymonthyear,
                            timecome=timecome, timeback=timeback, whatdo=whatdo))

@app.route('/teachercomment' , methods= ['get','post'])
def teachercomment():
    datawork = It.connect("databaseall.db")
    dataworkcur = datawork.cursor()
    x = dict(request.form.items())
    print(x)
    listdata=[]
    for i in x:
        listdata.append(i)
    nameta=str(listdata[0])
    comment = x['%s'%(nameta)]
    passfail=str(listdata[1])
    print(nameta)
    print(comment)
    print(passfail)
    if passfail == 'pass':
        dataworkcur.execute("UPDATE timesheet SET StatusAj = '%s' WHERE Username = '%s' and ID = '1'" % ('1', nameta))
        dataworkcur.execute("UPDATE timesheet SET Comment = '%s' WHERE Username = '%s' and ID = '1'" % (comment,nameta))
        datawork.commit()
    if passfail == 'notpass':
        dataworkcur.execute("UPDATE timesheet SET StatusAj = '%s' WHERE Username = '%s'and ID = '1'" % ('x', nameta))
        dataworkcur.execute("UPDATE timesheet SET Comment = '%s' WHERE Username = '%s'and ID = '1'" % (comment,nameta))
        datawork.commit()
    return(home())


'''
@app.route('/Teacherworkform')
def teacherworkform():
    timesheets = It.connect("databaseall.db")
    timesheetcur = timesheets.cursor()
    timesheetcur.execute("SELECT Username FROM timesheet WHERE ID ='1'")
    name = []
    for pdfrow in timesheetcur.fetchall():
        pdflist = []
        for i in pdfrow:
            pdflist.append(i)
            name.append(pdflist)
    print(name)
    return (render_template("Aj/WorkingFormselect.html",name=name))
@app.route('/Teacherselect' , methods= ['post'])
def select():
    x = dict(request.form.items())
    print(x)
    test = x['name']
    print(test)
    return (test)
'''

@app.route('/TA_select')
def TA_select():
    if(a.type_user == 'teacher'):
        subject = It.connect("databaseall.db")
        subjectcur = subject.cursor()
        subjectcur.execute("SELECT Subject FROM teacher WHERE Username='%s'" % a.username)
        print(a.username)
        subjectteacher = []

        for pdfrow in subjectcur.fetchall():
            pdflist = []
            for i in pdfrow:
                pdflist.append(i)
                subjectteacher.append(i)
        return(render_template("Aj/TA_select_aj.html",subjectteacher=subjectteacher))

@app.route('/TA_selectpassfail', methods= ['post'])
def TA_selectpassfail():
    x = dict(request.form.items())
    subject = []
    for i in x:
        subject.append(i)
    print(subject[0])
    return(render_template('Aj/TA_select_detail3_aj.html'))

@app.route('/TA_select_detail' , methods= ['post'])
def TA_select_detail():
    x = dict(request.form.items())
    #print(x)
    return(render_template('Aj/TA_select_detail2_aj.html',var = x['subject']))



@app.route('/evaluate')
def evalueate():
    return render_template('TA/FromTest.html')
@app.route('/evaluateadd', methods=['post'])
def evalueateadd():
    x = dict(request.form.items())
    print(x)
    one1 = x['one1']
    one2 = x['one2']
    one3 = x['one3']
    two1 = x['two1']
    two2 = x['two2']
    two3 = x['two3']
    three1 = x['three1']
    three2 = x['three2']
    three3 = x['three3']
    comment = x['comment']
    evaluate = It.connect("databaseall.db")
    evaluatecur = evaluate.cursor()
    evaluatecur.execute("INSERT INTO evaluate(One1,One2,One3,Two1,Two2,Two3,Three1,Three2,Three3,Comment) VALUES(?,?,?,?,?,?,?,?,?,?)",(one1,one2,one3,two1,two2,two3,three1,three2,three3,comment))
    evaluate.commit()

    return(home())

@app.route('/TA_profile')
def TA_profile():
    print('kkkk')
    return (render_template('Aj/TA_profile.html'))


@app.route('/TA_profile_detail', methods=['post'])
def TA_profile_detail():
    x = dict(request.form.items())
    print(x)
    student = It.connect("databaseall.db")
    cur1 = student.cursor()
    cur1.execute(
        "SELECT Name,Surname,IDNUMBER,Department,Level,Grade,Tel,Email FROM student WHERE Subject='%s'" %x['subject'])
    info = []
    for row1 in cur1.fetchall():
        for i in row1:
            info.append(i)
    student.close()
    a1 = ""
    for i in info:
        s1 = "1.Subject::" + str(i[0]) + "2.Number::" + str(i[1]) + "3.Level::" + str(
            i[2]) + "4.Grade::" + str(i[3]) + "5.Attritute::" + str(i[4])
        a1.append(s1)
    print(a1)
    return (render_template('Aj/Show_TA2_aj.html',var = a1))

@app.route('/post_TA')
def post():
    return (render_template('Admin/PDF_admin.html'))

@app.route('/post_TA_finish', methods=['post'])
def post_TA_finish():
    x = dict(request.form.items())
    #print(x['TypeSubject'],x['link_PDF'])
    ID = x['TypeSubject']
    link_pdf = x['link_PDF']
    data = It.connect("databaseall.db")
    datacur = data.cursor()
    datacur.execute("UPDATE admin SET Recruitment_TA = '%s' WHERE ID = '%s'" % (link_pdf,ID))
    data.commit()
    return(index())

""""-----FRA_141-----"""
@app.route('/FRA_TA141')
def FRA_TA141():
    ID = 'FRA141'
    type_user = 'TA'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_property141')
def FRA_TA_property141():
    ID = 'FRA141'
    type_user = 'TA'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_course141')
def FRA_TA_course141():
    ID = 'FRA141'
    type_user = 'TA'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
@app.route('/FRA_Hiring141')
def FRA_Hiring141():
    ID = 'FRA141'
    type_user = 'Hiring'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_property141')
def FRA_Hiring_property141():
    ID = 'FRA141'
    type_user = 'Hiring'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_course141')
def FRA_Hiring_course141():
    ID = 'FRA141'
    type_user = 'Hiring'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
""""-----FRA_161-----"""
@app.route('/FRA_TA161')
def FRA_TA161():
    ID = 'FRA161'
    type_user = 'TA'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_property161')
def FRA_TA_property161():
    ID = 'FRA161'
    type_user = 'TA'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_course161')
def FRA_TA_course161():
    ID = 'FRA161'
    type_user = 'TA'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
@app.route('/FRA_Hiring161')
def FRA_Hiring161():
    ID = 'FRA161'
    type_user = 'Hiring'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_property161')
def FRA_Hiring_property161():
    ID = 'FRA161'
    type_user = 'Hiring'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_course161')
def FRA_Hiring_course161():
    ID = 'FRA161'
    type_user = 'Hiring'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
""""-----FRA_221-----"""
@app.route('/FRA_TA221')
def FRA_TA221():
    ID = 'FRA221'
    type_user = 'TA'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_property221')
def FRA_TA_property221():
    ID = 'FRA221'
    type_user = 'TA'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_course221')
def FRA_TA_course221():
    ID = 'FRA221'
    type_user = 'TA'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
@app.route('/FRA_Hiring221')
def FRA_Hiring221():
    ID = 'FRA221'
    type_user = 'Hiring'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_property221')
def FRA_Hiring_property221():
    ID = 'FRA221'
    type_user = 'Hiring'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_course221')
def FRA_Hiring_course221():
    ID = 'FRA221'
    type_user = 'Hiring'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
""""-----FRA_222-----"""
@app.route('/FRA_TA222')
def FRA_TA222():
    ID = 'FRA222'
    type_user = 'TA'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_property222')
def FRA_TA_property222():
    ID = 'FRA222'
    type_user = 'TA'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_course222')
def FRA_TA_course222():
    ID = 'FRA221'
    type_user = 'TA'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
@app.route('/FRA_Hiring222')
def FRA_Hiring222():
    ID = 'FRA222'
    type_user = 'Hiring'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_property222')
def FRA_Hiring_property222():
    ID = 'FRA222'
    type_user = 'Hiring'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_course222')
def FRA_Hiring_course222():
    ID = 'FRA222'
    type_user = 'Hiring'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
""""-----FRA_231-----"""
@app.route('/FRA_TA231')
def FRA_TA231():
    ID = 'FRA231'
    type_user = 'TA'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_property231')
def FRA_TA_property231():
    ID = 'FRA231'
    type_user = 'TA'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_course231')
def FRA_TA_course231():
    ID = 'FRA231'
    type_user = 'TA'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
@app.route('/FRA_Hiring231')
def FRA_Hiring231():
    ID = 'FRA231'
    type_user = 'Hiring'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_property231')
def FRA_Hiring_property231():
    ID = 'FRA231'
    type_user = 'Hiring'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_course231')
def FRA_Hiring_course231():
    ID = 'FRA231'
    type_user = 'Hiring'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
""""-----FRA_241-----"""
@app.route('/FRA_TA241')
def FRA_TA241():
    ID = 'FRA241'
    type_user = 'TA'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_property241')
def FRA_TA_property241():
    ID = 'FRA241'
    type_user = 'TA'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_course241')
def FRA_TA_course241():
    ID = 'FRA241'
    type_user = 'TA'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
@app.route('/FRA_Hiring241')
def FRA_Hiring241():
    ID = 'FRA241'
    type_user = 'Hiring'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_property241')
def FRA_Hiring_property241():
    ID = 'FRA241'
    type_user = 'Hiring'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_course241')
def FRA_Hiring_course241():
    ID = 'FRA241'
    type_user = 'Hiring'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
""""-----FRA_261-----"""
@app.route('/FRA_TA261')
def FRA_TA261():
    ID = 'FRA261'
    type_user = 'TA'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_property261')
def FRA_TA_property261():
    ID = 'FRA261'
    type_user = 'TA'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_course261')
def FRA_TA_course261():
    ID = 'FRA261'
    type_user = 'TA'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
@app.route('/FRA_Hiring261')
def FRA_Hiring261():
    ID = 'FRA261'
    type_user = 'Hiring'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_property261')
def FRA_Hiring_property261():
    ID = 'FRA261'
    type_user = 'Hiring'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_course261')
def FRA_Hiring_course261():
    ID = 'FRA261'
    type_user = 'Hiring'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
""""-----FRA_321-----"""
@app.route('/FRA_TA321')
def FRA_TA321():
    ID = 'FRA321'
    type_user = 'TA'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_property321')
def FRA_TA_property321():
    ID = 'FRA321'
    type_user = 'TA'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_course321')
def FRA_TA_course321():
    ID = 'FRA321'
    type_user = 'TA'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
@app.route('/FRA_Hiring321')
def FRA_Hiring321():
    ID = 'FRA321'
    type_user = 'Hiring'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_property321')
def FRA_Hiring_property321():
    ID = 'FRA321'
    type_user = 'Hiring'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_course321')
def FRA_Hiring_course321():
    ID = 'FRA321'
    type_user = 'Hiring'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
""""-----FRA_331-----"""
@app.route('/FRA_TA331')
def FRA_TA331():
    ID = 'FRA331'
    type_user = 'TA'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_property331')
def FRA_TA_property331():
    ID = 'FRA331'
    type_user = 'TA'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_course331')
def FRA_TA_course331():
    ID = 'FRA331'
    type_user = 'TA'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
@app.route('/FRA_Hiring331')
def FRA_Hiring331():
    ID = 'FRA331'
    type_user = 'Hiring'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_property331')
def FRA_Hiring_property331():
    ID = 'FRA331'
    type_user = 'Hiring'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_course331')
def FRA_Hiring_course31():
    ID = 'FRA331'
    type_user = 'Hiring'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
""""-----FRA_332-----"""
@app.route('/FRA_TA332')
def FRA_TA332():
    ID = 'FRA332'
    type_user = 'TA'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_property332')
def FRA_TA_property332():
    ID = 'FRA332'
    type_user = 'TA'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_course332')
def FRA_TA_course332():
    ID = 'FRA332'
    type_user = 'TA'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
@app.route('/FRA_Hiring332')
def FRA_Hiring332():
    ID = 'FRA332'
    type_user = 'Hiring'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_property332')
def FRA_Hiring_property332():
    ID = 'FRA332'
    type_user = 'Hiring'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_course332')
def FRA_Hiring_course332():
    ID = 'FRA332'
    type_user = 'Hiring'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
""""-----FRA_341-----"""
@app.route('/FRA_TA341')
def FRA_TA341():
    ID = 'FRA341'
    type_user = 'TA'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_property341')
def FRA_TA_property341():
    ID = 'FRA341'
    type_user = 'TA'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_course341')
def FRA_TA_course341():
    ID = 'FRA341'
    type_user = 'TA'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
@app.route('/FRA_Hiring341')
def FRA_Hiring341():
    ID = 'FRA341'
    type_user = 'Hiring'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_property341')
def FRA_Hiring_property341():
    ID = 'FRA341'
    type_user = 'Hiring'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_course341')
def FRA_Hiring_course341():
    ID = 'FRA341'
    type_user = 'Hiring'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
""""-----FRA_451-----"""
@app.route('/FRA_TA451')
def FRA_TA451():
    ID = 'FRA451'
    type_user = 'TA'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_property451')
def FRA_TA_property451():
    ID = 'FRA451'
    type_user = 'TA'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_course451')
def FRA_TA_course451():
    ID = 'FRA451'
    type_user = 'TA'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
@app.route('/FRA_Hiring451')
def FRA_Hiring451():
    ID = 'FRA451'
    type_user = 'Hiring'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_property451')
def FRA_Hiring_property451():
    ID = 'FRA451'
    type_user = 'Hiring'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_course451')
def FRA_Hiring_course451():
    ID = 'FRA451'
    type_user = 'Hiring'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
""""-----FRA_452-----"""
@app.route('/FRA_TA452')
def FRA_TA452():
    ID = 'FRA452'
    type_user = 'TA'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_property452')
def FRA_TA_property452():
    ID = 'FRA452'
    type_user = 'TA'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_TA_course452')
def FRA_TA_course452():
    ID = 'FRA452'
    type_user = 'TA'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())
@app.route('/FRA_Hiring452')
def FRA_Hiring452():
    ID = 'FRA452'
    type_user = 'Hiring'
    type = 'Result'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_property452')
def FRA_Hiring_property452():
    ID = 'FRA452'
    type_user = 'Hiring'
    type = 'Property'
    open_pdf(ID,type_user,type)
    return(index())
@app.route('/FRA_Hiring_course452')
def FRA_Hiring_course452():
    ID = 'FRA452'
    type_user = 'Hiring'
    type = 'Course'
    open_pdf(ID, type_user, type)
    return(index())

def open_pdf(ID,type_user,type):
    data = It.connect("databaseall.db")
    datacur = data.cursor()
    #print(ID)
    url = ''
    if(type_user == 'TA'):
        if(type == 'Property'):
            datacur.execute("SELECT property FROM admin_pdf_TA WHERE ID = '%s'" % (ID))
        if (type == 'Course'):
            datacur.execute("SELECT course_syllabus FROM admin_pdf_TA WHERE ID = '%s'" % (ID))
        if (type == 'Result'):
            datacur.execute("SELECT Result FROM admin_pdf_TA WHERE ID = '%s'" % (ID))
    if(type_user == 'Hiring'):
        if (type == 'Property'):
            datacur.execute("SELECT property FROM admin_pdf_Hiring WHERE ID = '%s'" % (ID))
        if (type == 'Course'):
            datacur.execute("SELECT course_syllabus FROM admin_pdf_Hiring WHERE ID = '%s'" % (ID))
        if (type == 'Result'):
            datacur.execute("SELECT Result FROM admin_pdf_Hiring WHERE ID = '%s'" % (ID))
    for row1 in datacur.fetchall():
        for i in row1:
            url = i
    data.commit()
    if(url == ''):
        return()
    webbrowser.open(url)
app.run(debug=True)
