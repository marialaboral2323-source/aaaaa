import logging
import secrets
from flask import Flask, request, render_template
from flask_cors import CORS
import requests
import func as F

app = Flask(__name__)
CORS(app)
app.secret_key = secrets.token_hex(32)

try:
    FLAG = open("./flag.txt", "r", encoding="utf-8").read().strip()
except:
    FLAG = "[**FLAG**]"

accounts = {"test": "1234", "admin": FLAG}

logging.getLogger('flask_cors').level = logging.DEBUG
open("log.txt", "w", encoding="utf-8").close()

file_handler = logging.FileHandler("log.txt", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler.setFormatter(formatter)

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(file_handler)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET"])
def login():
    username = request.args.get("username")
    password = request.args.get("password")

    if username in accounts and accounts[username] == password:
        logging.debug(f"\nuser={username}")
        return "로그인 성공!"
    else:
        return "로그인 실패"

@app.route("/logout", methods=["GET"])
def logout():
    user = F.get_login_user()
    if user:
        logging.debug(f"user={user} logged out")
        logging.debug("\nuser=None")
        return f"{user} 로그아웃 성공!"
    else:
        return "로그인 상태가 아닙니다."

@app.route("/whoami", methods=["GET"])
def whoami():
    user = F.get_login_user()
    return user if user else "로그인 안됨"

@app.route('/calc', methods=['GET'])
def calc_proxy():
    user = F.get_login_user()
    if user != 'admin':
        return 'Get admin account', 403
    
    text = request.args.get('text')
    allowed_chars = "0123456789+-*/"
    if not all(char in allowed_chars for char in text):
        return 'Do not cheat!!!', 503
    
    try:
        response = requests.get(
            url=f'http://php_app:5000/?{request.query_string.decode()}',
            timeout=10
        )
        
        return str(eval(response.text, {'__builtins__': {}}))
    except:
        return 'PHP 서버 연결 실패', 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, threaded=True)

