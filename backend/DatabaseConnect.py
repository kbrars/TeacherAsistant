from flask import Flask, request, jsonify, session, redirect, url_for, send_file
from flask_session import Session
import psycopg2
from flask_cors import CORS
import json

class Database():
    def __init__(self): 
        # JSON dosyasını okuma
        with open("DatabaseInfo.json", "r") as file:
            data = json.load(file)
            
        self.host = data["host"]
        self.dbname = data["dbname"]
        self.port = data["port"]
        self.user = data["user"]
        self.password = data["password"]
        self.dbType = data["dbType"]


    
    def get_db_connection(self):
        # Veritabanı bağlantısı kurma
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                port=self.port
            )
            cur = self.conn.cursor()
            return self.conn,cur
        except psycopg2.OperationalError as e:
            print("Veritabanına bağlantı sağlanamadı:", e)
            return None
        

    def connClose(self):
        return self.conn.close()

