from flask import Flask, render_template, request
from createDB_v5 import DB
import sqlite3 as It
import os

from reportlab.pdfgen import canvas
app = Flask(__name__)

import sqlite3 as It
evaluate = It.connect("evaluate.db")
evaluatecur = evaluate.cursor()
#student = It.connect("student_v2.db")
#evaluatecur = student.cursor()
test = It.connect("databaseall.db")
testcur = test.cursor()
#evaluatecur.execute("create table studentnormal(ID text,Name text,Surname text,Department text,Branch text,Degree text,Level text,Idnum text,Grade text,Email text,Tel text,Subject text,AccountNum text,Attribute text,Status text)")
#test.execute("create table timesheet(ID text,Username text,Subject text,DayMonthYear text,Timecome text,Timeback text,whatdo text,StatusTa text,StatusAj text,StatusAdmin text,Comment text)")
#evaluatecur.execute("create table teacher(Username text,Password text,TypeUser text,Name text,Surname text,Tel text,Subject text,Comment text)")
#testcur.execute("create table teacherwant(Username text,Subject text,Numwant text,Level text,Grade text,Attribute text)")

#testcur.execute("create table evaluate(One1 text,One2 text,One3 text,Two1 text,Two2 text,Two3 text,Three1 text,Three2 text,Three3 text,Comment text)")
testcur.execute("INSERT INTO student(Username,Password,TypeUser,Subject) VALUES(?,?,?,?)",('FRA231US1','1234','student','FRA231'))
testcur.execute("INSERT INTO student(Username,Password,TypeUser,Subject) VALUES(?,?,?,?)",('FRA241US1','1234','student','FRA241'))
testcur.execute("INSERT INTO student(Username,Password,TypeUser,Subject) VALUES(?,?,?,?)",('FRA261US1','1234','student','FRA261'))
testcur.execute("INSERT INTO student(Username,Password,TypeUser,Subject) VALUES(?,?,?,?)",('FRA321US1','1234','student','FRA321'))
testcur.execute("INSERT INTO student(Username,Password,TypeUser,Subject) VALUES(?,?,?,?)",('FRA331US1','1234','student','FRA331'))
testcur.execute("INSERT INTO student(Username,Password,TypeUser,Subject) VALUES(?,?,?,?)",('FRA332US1','1234','student','FRA332'))
testcur.execute("INSERT INTO student(Username,Password,TypeUser,Subject) VALUES(?,?,?,?)",('FRA341US1','1234','student','FRA341'))
testcur.execute("INSERT INTO student(Username,Password,TypeUser,Subject) VALUES(?,?,?,?)",('FRA451US1','1234','student','FRA451'))
testcur.execute("INSERT INTO student(Username,Password,TypeUser,Subject) VALUES(?,?,?,?)",('FRA452US1','1234','student','FRA452'))


#testcur.execute("INSERT INTO student(Username,Password,TypeUser,Subject) VALUES(?,?,?,?)",('FRA221US1','1234','student','FRA221'))
#testcur.execute("INSERT INTO student(Username,Password,TypeUser) VALUES(?,?,?)",('FRA122US1','1234','student'))

#testcur.execute("INSERT INTO teacher(Username,Password,TypeUser) VALUES(?,?,?)",('Admin1','1234','admin'))
test.commit()

