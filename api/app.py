from flask import Flask, request, jsonify
import sqlite3
import pickle
import subprocess
import hashlib
import os
import logging

app = Flask(__name__)

API_KEY = "API-KEY-123456"

logging.basicConfig(level=logging.DEBUG)

@app.route("/auth", methods=["POST"])
def auth():
    username = request.json.get("username")
    password = request.json.get("password")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    if user:
        return jsonify({"message": "Success"})
    return jsonify({"message": "Failed"}), 401

@app.route("/exec", methods=["POST"])
def execute():
    cmd = request.json.get("command")
    output = subprocess.check_output(cmd, shell=True)
    return output

@app.route("/deserialize", methods=["POST"])
def deserialize():
    data = request.data
    obj = pickle.loads(data)
    return str(obj)

@app.route("/encrypt", methods=["POST"])
def encrypt():
    text = request.json.get("text")
    m = hashlib.md5()
    m.update(text.encode())
    return m.hexdigest()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)