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
#evaluatecur.execute("create table timesheet(ID text,Username text,DayMonthYear text,Timecome text,Timeback text,whatdo text,Status text,Comment text)")
#evaluatecur.execute("create table teacher(Username text,Password text,TypeUser text,Name text,Surname text,Tel text,Subject text,Comment text)")
#evaluatecur.execute("create table teacherwant(Username text,Subject text,Numwant text,Level text,Grade text,Attribute text)")

#evaluatecur.execute("create table evaluate(One1 text,One2 text,One3 text,Two1 text,Two2 text,Two3 text,Three1 text,Three2 text,Three3 text,Comment text)")


test.execute("INSERT INTO teacher(Username,Password,TypeUser,Subject) VALUES(?,?,?,?)",
                     ('Teacher1', 1234, 'teacher', 'FRA121'))
test.commit()

