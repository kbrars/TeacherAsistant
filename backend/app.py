from flask import Flask, request, jsonify, session, redirect, url_for,send_file
from flask_session import Session
import psycopg2
from flask_cors import CORS 
import io
import cv2
import numpy as np
import base64
app = Flask(__name__)
CORS(app) 

# Oturum için gizli anahtar ayarlayın
app.config['SECRET_KEY'] = 'GSAJK5673554b5s#wadd1.VDKK5'

# Oturum verilerini saklamak için Flask-Session'ı yapılandırın
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

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

    if not username or not password:
        return jsonify({"status": False, "message": "Username and password are required"}), 400

    try:
        conn = psycopg2.connect("postgresql://postgres:479528@localhost/BTKHackathon")
        cur = conn.cursor()

        # Parametreli sorgu kullanarak SQL enjeksiyonunu önleme
        sql = "SELECT * FROM users WHERE username=%s AND password=%s"
        cur.execute(sql, (username, password))
        record = cur.fetchone()

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
        if cur:
            cur.close()
        if conn:
            conn.close()

#Çıkış işlemi
@app.route("/api/logout", methods=["POST"])
def logout():
  #  session.clear()
    return jsonify({"logout": True,})

#Öğretmen bilgilerini getirme
@app.route("/api/getTeacherData", methods=["POST"])
def get_superOperatorData():
    data = request.json
    username = data.get('username')
    try:
        conn = psycopg2.connect("postgresql://postgres:479528@localhost/BTKHackathon")
        cur = conn.cursor()
        sql = "SELECT * FROM users WHERE username = %s"
        cur.execute(sql, (username,))
        operators = cur.fetchall()
        conn.commit()
        return jsonify(operators)
    except (psycopg2.Error, Exception) as error:
        # Hata oluştuğunda uygun bir yanıt döndürün
        return jsonify({'error': str(error)})
    finally:
        # Bağlantıyı ve imleci kapat
        if cur:
            cur.close()
        if conn:
            conn.close()

#Öğretmen bilgilerini güncelleme
@app.route("/api/updateTeacherData", methods=["POST"])
def superOperator_update_profile():
    data = request.json
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    username = data.get('username')
    real_username = data.get("real_username")
    email = data.get('email')
    address = data.get("address")
    phone=data.get("phone")

    if not all([firstName, lastName, username, real_username, email, address]):
        return jsonify({"status": False, "message": "All fields are required"}), 400

    try:
        conn = psycopg2.connect("postgresql://postgres:479528@localhost/BTKHackathon")
        cur = conn.cursor()

        # Mevcut kullanıcı adını ve e-postayı kontrol et
        sql = "SELECT username, email FROM users WHERE username = %s"
        cur.execute(sql, (real_username,))
        existing_user = cur.fetchone()

        if not existing_user:
            return jsonify({"status": False, "message": "No user found with the given username"}), 404

        existing_username, existing_email = existing_user

        # Yeni kullanıcı adı veya e-posta mevcut mu kontrol et
        if username != existing_username:
            sql = "SELECT 1 FROM users WHERE username = %s"
            cur.execute(sql, (username,))
            if cur.fetchone():
                return jsonify({"status": False, "message": "Username already exists"}), 409

        if email != existing_email:
            sql = "SELECT 1 FROM users WHERE email = %s"
            cur.execute(sql, (email,))
            if cur.fetchone():
                return jsonify({"status": False, "message": "Email already exists"}), 409

        # Kullanıcı bilgilerini güncelle
        sql = """
        UPDATE users SET firstname = %s, lastname = %s, username = %s, email = %s, address = %s, phone=%s
        WHERE username = %s
        """
        cur.execute(sql, (firstName, lastName, username, email, address,phone, real_username))
        conn.commit()

        response = {"status": True, "message": "User data updated successfully", "logout":False}

        # Kullanıcı adı veya e-posta değişmişse oturumu sonlandır ve özel bir durum döndür
        if username != existing_username or email != existing_email:
            session.clear()
            return jsonify({"logout":True})  

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

#Şifre doğrulama
@app.route("/api/verifyPassword", methods=["POST"])
def verify_password():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": False, "message": "Username and password are required"}), 400

    try:
        conn = psycopg2.connect("postgresql://postgres:479528@localhost/BTKHackathon")
        cur = conn.cursor()

        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        cur.execute(sql, (username, password))
        user = cur.fetchone()

        if user:
            return jsonify({"status": True, "message": "Password verified"}), 200
        else:
            return jsonify({"status": False, "message": "Invalid password"}), 401

    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

#Şifre güncelleme
@app.route("/api/changePassword", methods=["POST"])
def change_password():
    data = request.json
    username = data.get('username')
    new_password = data.get('new_password')

    if not username or not new_password:
        return jsonify({"status": False, "message": "Username and new password are required"}), 400

    try:
        conn = psycopg2.connect("postgresql://postgres:479528@localhost/BTKHackathon")
        cur = conn.cursor()

        sql = "UPDATE users SET password = %s WHERE username = %s"
        cur.execute(sql, (new_password, username))
        conn.commit()

        if cur.rowcount == 0:
            return jsonify({"status": False, "message": "User not found"}), 404

        return jsonify({"status": True, "message": "Password updated successfully"}), 200

    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


#resim donusturme
def convert_frame_from_bytes(frame_bytes):
    # Byte array to numpy array
    frame_np = np.frombuffer(frame_bytes, dtype=np.uint8)
    # Numpy array to image
    frame = cv2.imdecode(frame_np, flags=cv2.IMREAD_COLOR)
    _, buffer = cv2.imencode('.jpg', frame)
    frame_base64 = base64.b64encode(buffer).decode('utf-8')
    return frame_base64

# Öğretmenin derslerini getirme
@app.route("/api/getTeacherLessons", methods=["POST"])
def get_teacher_lessons():
    data = request.json
    user_name = data.get('username')  # Öğretmenin kullanıcı adını al
    
    try:
        # Veritabanına bağlan
        conn = psycopg2.connect("postgresql://postgres:479528@localhost/BTKHackathon")
        cur = conn.cursor()
        
        # Öğretmenin ID'sini al
        sql_user_id = "SELECT id FROM users WHERE username = %s"
        cur.execute(sql_user_id, (user_name,))
        teacher = cur.fetchone()
        
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
        cur.execute(sql_lessons, (teacher_id,))
        lessons_data = cur.fetchall()

        # Sonuçları JSON formatına çevir
        lessons_list = []
        for row in lessons_data:
            lessons_list.append({
                "id": row[0],
                "lesson_name": row[1],
                "image":convert_frame_from_bytes(row[2])


            })

        return jsonify(lessons_list), 200
    except (psycopg2.Error, Exception) as error:
        return jsonify({'error': str(error)}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
