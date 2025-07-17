# flask server 구동 코드
from flask import Flask
from flask import render_template #html 문서를 load
# templates 폴더에 있는 html만 바라볼 수 있다
from flask import request, redirect, make_response
from aws import detect_labels_local_file as label
from werkzeug.utils import secure_filename
from aws import compare_faces

app = Flask(__name__)


@app.route("/compare", methods=["POST"])
def compare():
    try:
        if request.method == "POST":
            f_1 = request.files["file1"]
            f_2 = request.files["file2"]
            filename_1 = secure_filename(f_1.filename)
            filename_2 = secure_filename(f_2.filename)
            f_1.save("static/" + filename_1)
            f_2.save("static/" + filename_2)
            r = compare_faces("static/" + filename_1, "static/" + filename_2)
            return r
    except :
        return "error"
    

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/mbti", methods=["POST"])
def mbti():
    try:
        if request.method == "POST":
            mbti = request.form["mbti"]

            return f"당신의 MBTI는 {mbti}입니다"
    except:
        return "데이터 수신 실패"

@app.route("/login", methods=["GET"])
def  login():
    try:
        if request.method == "GET":
            # login_id, login_pw를 받아야해
            # get -> request.args
            login_id = request.args["login_id"]
            login_pw = request.args["login_pw"]

            # 로그인 성공 ->
            if (login_id == "xogud") and (login_pw == "1234"):
                response = make_response("로그인 성공")
                response.set_cookie("user",login_id)
                return redirect("/login/success")
            # 로그인 실패 ->
            else:
                return redirect("/")
    except:
        return "로그인 실패"
    
@app.route("/login/success")
def login_success():
    login_id = request.cookies.get("user")
    return f"{login_id}님 환영합니다"

@app.route("/detect", methods=["POST"])
def detect():
    try:
        if request.method == "POST":
            f = request.files["file"]
            filename = secure_filename(f.filename)
            f.save("static/" + filename)
            label("static/" + filename)
    except:
        return "감지 실패"

if __name__ == "__main__":
    app.run(host="0.0.0.0")