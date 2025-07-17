

# ,로 연결 가능
from flask import Flask, render_template
from flask import request , redirect , make_response
from aws import detect_labels_local_file as label # 모듈화 할 함수
from aws import compare_faces as facecom
from werkzeug.utils import secure_filename 


# redirect : 이동, 데이터값을 넘겨주지는 못함
# make_response : 쿠키를 만들기 위한

# render_template : html문서를 load!
# 단, templates 폴더에 있는 html만 바라볼 수 있다

# 터미널에서 mkdir templates -> 폴더 만들기
#  cp .\html\exam03.html .\templates\exam03.html -> 복사

app = Flask(__name__) # instance로 받을 수 있음


# 서버 주소 /
# 주소하나 당 함수 하나 
# 서버 주소 /  로 들어오면 return html문서
@app.route("/")
def index():
    return render_template("home.html")
#  return render_template("exam03.html") -> template안에 있는 html 로드!!
# 다른 곳은 불가능


# html 폴더 내 exam04.html 을 templates 폴더로 복사
# http://10.10.15.32:5000/exam04 뒤에 exam04 쳐주면 들어가짐

@app.route("/compare", methods = ["POST"])
def compare():
    try:
        if request.method == "POST":
            f1 = request.files["file1"]
            f2 = request.files["file2"]

            f1_filename = secure_filename(f1.filename)
            f2_filename = secure_filename(f2.filename)

            f1.save("static/" + f1_filename)
            f2.save("static/" + f2_filename)

            r = facecom("static/" + f1_filename ,"static/" + f2_filename)

            return r
    except:
        return "얼굴 비교 실패"
    



@app.route("/detect",methods=["POST"])
def detect():
    try:
        if request.method == "POST":
            f = request.files["file"]

            filename = secure_filename(f.filename)
            # 외부에서 온 이미지, 파일등을 마음대로 저장할 수 없음

            # 서버에 클라이언트가 보낸 이미지를 저장!

            f.save("static/" + filename)
            r = label("static/" + filename)

            return r
           
    except:
        return "감지 실패"


# 객체 탐지 파이썬 파일 모듈화 시켜서 불러옴

@app.route("/mbti" , methods=["POST"]) # GET방식보다 조금 더 보안이 강함
def mbti():
    try:
        if request.method =="POST":
            mbti = request.form["mbti"]

            return f"당신의 MBTI는 {mbti}입니다."
    except:
        return "데이터 수신 실패"



@app.route("/login", methods=["GET"])
def login():

    try:
        if request.method =="GET":
            # login_id, login_pw
            # get-> request.args
            login_id = request.args["login_id"]
            login_pw = request.args["login_pw"]
            
            #로그인 성공
            if(login_id =="rhkrtjdb") and (login_pw=="tjdbtjdb"):
                #로그인 성공 -> 로그인 성공페이지 이동 -> rhkrtjdb님 환영합니다
                response = make_response(redirect("/login/success"))
                response.set_cookie("user", login_id)

                return response
            else:
                #로그인 실패 -> /경로로 다시 이동   
                return redirect("/")
    
    except:
        return "로그인 실패"



@app.route("/login/success", methods=["GET"])
def login_success():
    login_id = request.cookies.get("user")
    return f"{login_id}님 환영합니다"

if __name__ == "__main__":
    #1. host
    #2. port
 
    app.run(host="0.0.0.0") # 자기자신을 의미 # 터미널에 ipconfig 치면 아이피주소 알 수 있음
    #0.0.0.0하면 알아서 올라감   