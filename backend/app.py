from flask import Flask, request, jsonify, session, redirect, url_for
from flask_session import Session
import psycopg2
from flask_cors import CORS 

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


@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"logout": True,})
