from flask import Flask, request, jsonify, session, redirect, url_for,send_file
from flask_session import Session
import psycopg2
from flask_cors import CORS 
import io
import cv2
import numpy as np
import base64
from geminiApi import geminiApiResult
from ProjectFunctions import ProjectFunction 
app = Flask(__name__)
CORS(app) 

# Oturum için gizli anahtar ayarlayın
app.config['SECRET_KEY'] = 'GSAJK5673554b5s#wadd1.VDKK5'

# Oturum verilerini saklamak için Flask-Session'ı yapılandırın
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

pfunc = ProjectFunction()

def is_json_empty(json_data):
    return len(json_data) == 0

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# Authentication
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password') 
    return pfunc.login(username,password)


#Çıkış işlemi
@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    
    return jsonify({"logout": True,})

#Öğretmen bilgilerini getirme
@app.route("/api/getTeacherData", methods=["POST"])
def getTeacherData():
    data = request.json
    username = data.get('username')
    return pfunc.getTeacherData(username)

#Öğretmen bilgilerini güncelleme
@app.route("/api/updateTeacherData", methods=["POST"])
def updateTeacherData():
    data = request.json
    return pfunc.updateTeacherData(data)

#Şifre doğrulama
@app.route("/api/verifyPassword", methods=["POST"])
def verify_password():
    data = request.json
    return pfunc.verify_password(data) 

#Şifre güncelleme
@app.route("/api/changePassword", methods=["POST"])
def change_password():
    data = request.json
    return pfunc.change_password(data)




# Öğretmenin derslerini getirme
@app.route("/api/getTeacherLessons", methods=["POST"])
def get_teacher_lessons():
    data = request.json
    return pfunc.get_teacher_lessons(data)
  
#Ders konuarını getirme (Modala)
@app.route("/api/getSubjects", methods=["POST"])
def get_SubjectData():
    data = request.json
    lesson_id = data.get('id')
    return pfunc.get_SubjectData(lesson_id)

#Ders konuarını getirme (Modala)
@app.route("/api/createQuestions", methods=["POST"])
def createQuestions():
    data = request.json
    return pfunc.createQuestions(data)

#Materyal sayfası için dersler ve konuları
@app.route("/api/getTeacherLessons_Subjects", methods=["POST"])
def getTeacherLessons_Subjects():
    data = request.json
    #return pfunc.getTeacherLessons_Subjects()
    lessons= pfunc.get_teacher_lessons(data)
    lessons_and_subjects = []
    for k in range(0,len(lessons)):
        s = []
        subjects = pfunc.get_SubjectData(lessons[k]["id"])
        for i in range(0,len(subjects)):
            s.append(subjects[i][0])
        lessons_and_subjects.append({"id":lessons[k]["id"], "subjects":subjects,"image":lessons[k]["image"],"lesson_name":lessons[k]["lesson_name"]})    
    return jsonify({"s":lessons_and_subjects})

