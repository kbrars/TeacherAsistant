from flask import Flask, request, jsonify, session, redirect, url_for,send_file
from flask_session import Session
import psycopg2
from flask_cors import CORS 
import io
import cv2
import numpy as np
import base64
from geminiApi import geminiApiResult
from DatabaseConnect import Database

class ProjectFunction:
    def __init__(self):
        self.db = Database()

    def login(self,username,password):  
        if not username or not password:
            return jsonify({"status": False, "message": "Username and password are required"}), 400
        try:
            self.conn,self.cur = self.db.get_db_connection()
            sql = "SELECT * FROM users WHERE username=%s AND password=%s"
            self.cur.execute(sql, (username, password))
            record = self.cur.fetchone()
            
            if record is not None:
                session['user_id'] = record[0]
                session['user_name'] = record[1]
                session['sys_role'] = record[3]
                return jsonify({"status": True, "sys_role": session['sys_role'], "session": session['user_id'], "session_username": session['user_name']})
            else:
                return jsonify({"status": False, "message": "Invalid username or password"}), 401         
        except Exception as e:
            return jsonify({"status": False, "message": str(e)}), 500
        
        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                self.db.connClose()
        

    def getTeacherData(self,username):
        try:
            sql = "SELECT * FROM users WHERE username = %s"
            self.conn,self.cur = self.db.get_db_connection()
            self.cur.execute(sql, (username,))
            operators = self.cur.fetchall()
            self.db.conn.commit()
            return jsonify(operators)
        except (psycopg2.Error, Exception) as error:
             return jsonify({'error': str(error)})
        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                self.db.connClose()

    def updateTeacherData(self,data):
        firstName = data.get("firstName")
        lastName = data.get("lastName")
        username = data.get("username")
        real_username = data.get("real_username")
        email = data.get("email")
        address = data.get("address")
        phone = data.get("phone")

        if not all([firstName, lastName, username, real_username, email, address]):
            return jsonify({"status": False, "message": "All fields are required"}), 400
        try:
            self.conn,self.cur = self.db.get_db_connection()
            sql = "SELECT username, email FROM users WHERE username = %s"
            self.cur.execute(sql, (real_username,))
            existing_user = self.cur.fetchone()
            if not existing_user:
                return jsonify({"status": False, "message": "No user found with the given username"}), 404

            existing_username, existing_email = existing_user
             # Yeni kullanıcı adı veya e-posta mevcut mu kontrol et
            if username != existing_username:
                sql = "SELECT 1 FROM users WHERE username = %s"
                self.cur.execute(sql, (username,))
                if self.cur.fetchone():
                    return jsonify({"status": False, "message": "Username already exists"}), 409
            if email != existing_email:
                sql = "SELECT 1 FROM users WHERE email = %s"
                self.cur.execute(sql, (email,))
                if self.ur.fetchone():
                    return jsonify({"status": False, "message": "Email already exists"}), 409

             # Kullanıcı bilgilerini güncelle
            sql = """
            UPDATE users SET firstname = %s, lastname = %s, username = %s, email = %s, address = %s, phone=%s
            WHERE username = %s
            """
            self.cur.execute(sql, (firstName, lastName, username, email, address,phone, real_username))
            self.db.conn.commit()

            response = {"status": True, "message": "User data updated successfully", "logout":False}

            # Kullanıcı adı veya e-posta değişmişse oturumu sonlandır ve özel bir durum döndür
            if username != existing_username or email != existing_email:
                session.clear()
                return jsonify({"logout":True})  

            return jsonify(response), 200

        except Exception as e:
            return jsonify({"status": False, "message": str(e)}), 500


    def verify_password(self,data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"status": False, "message": "Username and password are required"}), 400
        try : 
            self.conn,self.cur = self.db.get_db_connection()
            sql = "SELECT * FROM users WHERE username = %s AND password = %s"
            self.cur.execute(sql, (username, password))
            user = self.cur.fetchone()
            if user:
                return jsonify({"status": True, "message": "Password verified"}), 200
            else:
                return jsonify({"status": False, "message": "Invalid password"}), 401

        except Exception as e:
            return jsonify({"status": False, "message": str(e)}), 500
        
        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                self.db.connClose()
        
    def change_password(self,data):
        username = data.get('username')
        new_password = data.get('new_password')
        if not username or not new_password:
            return jsonify({"status": False, "message": "Username and new password are required"}), 400
        try:
            self.conn,self.cur = self.db.get_db_connection()
            sql = "UPDATE users SET password = %s WHERE username = %s"
            self.cur.execute(sql, (new_password, username))
            self.db.conn.commit()

            if self.cur.rowcount == 0:
                return jsonify({"status": False, "message": "User not found"}), 404
            return jsonify({"status": True, "message": "Password updated successfully"}), 200

        except Exception as e:
            return jsonify({"status": False, "message": str(e)}), 500
        finally:
                if self.cur:
                    self.cur.close()
                if self.conn:
                    self.db.connClose()

    #resim donusturme
    def convert_frame_from_bytes(self,frame_bytes):
        # Byte array to numpy array
        frame_np = np.frombuffer(frame_bytes, dtype=np.uint8)
        # Numpy array to image
        frame = cv2.imdecode(frame_np, flags=cv2.IMREAD_COLOR)
        _, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        return frame_base64

    def get_teacher_lessons(self,data):
        user_name = data.get('username')
            
        try:
            self.conn,self.cur = self.db.get_db_connection()
            # Öğretmenin ID'sini al
            sql_user_id = "SELECT id FROM users WHERE username = %s"
            self.cur.execute(sql_user_id, (user_name,))
            teacher = self.cur.fetchone()

            if teacher is None:
                return jsonify({'error': 'Öğretmen bulunamadı.'}), 404

            teacher_id = teacher[0]

            # Öğretmenin derslerini seç
            sql_lessons = """
            SELECT lessons.id, lessons.lesson_name,lessons.image_data,lessons.image_name
            FROM lessons
            JOIN teachers_lessons ON lessons.id = teachers_lessons.lesson_id
            WHERE teachers_lessons.teacher_id = %s
            """
            self.cur.execute(sql_lessons, (teacher_id,))
            lessons_data = self.cur.fetchall()

            # Sonuçları JSON formatına çevirme
            lessons_list = []
            for row in lessons_data:
                lessons_list.append({
                    "id": row[0],
                    "lesson_name": row[1],
                    "image":self.convert_frame_from_bytes(row[2])
                }) 
            return lessons_list
        except (psycopg2.Error, Exception) as error:
            return jsonify({'error': str(error)}), 500
        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                self.db.connClose()
        

    def get_SubjectData(self,lesson_id):
        try:
            self.conn,self.cur = self.db.get_db_connection()
            sql = "SELECT subject_name FROM subjects WHERE lesson_id = %s"
            self.cur.execute(sql, (lesson_id,))
            subjects = self.cur.fetchall()
            self.db.conn.commit()
            return subjects
        except (psycopg2.Error, Exception) as error:
            return jsonify({'error': str(error)})
        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                self.db.connClose()

    def createQuestions(self,data):
        selected_subjects = ', '.join(data.get("selected_subjects"))
        total_Question = data.get("total_questions")
        promt = f"{selected_subjects} konularından toplamda {total_Question} soru oluştur.Soru seviyesi orta olsun. Sadece sorular ve cevapları olsun . Ek bilgi olmasın. Konu başlıkları olmasın. Not yazma."
        result= geminiApiResult(promt)
        return jsonify({"questions": result})
    
    def getTeacherLessons_Subjects(self):
        data = {"username": "karslann"}
        user_name = data.get('username')
        lessons = self.get_teacher_lessons(data)
        return lessons
    
    def createMeterial(self,data):
        subject = data.get("subject_name")
        lesson_name = data.get("lesson_name")
        promt = f"{lesson_name} dersinde konu olan {subject} konusundan ders materyali hazırlar mısın. Materyal dışında herhangi bir şey yazma."
        result= geminiApiResult(promt)
        return jsonify({"material": result})
            
        

        