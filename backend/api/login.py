import traceback
from flask import Flask,request,jsonify
from functools import wraps
from flask import Blueprint
from datetime import datetime,timedelta
import db
import config
import jwt
from flask_cors import CORS

login_app = Blueprint('login_app',__name__)
CORS(login_app)

#医生登录接口
@login_app.route('/doctor_login',methods=['POST'])
def doctor_login():
    token = request.headers.get('token')

    if token == "":
        try:
            data = request.get_json()
            tel = data['phone']
            password = data['password']

            sql = "select username from doctors where telephone = %s AND password = %s"

            operate = db.Database()
            result = operate.execute(sql,(tel,password))
            user = str(result[0]).strip('(),').replace("'","")
            print(user)
            expiration_time = datetime.utcnow() + timedelta(days=15)
            if result:
                token2 = jwt.encode({'name':result[0],'exp':expiration_time},config.secret_key,algorithm='HS256')
                
                return jsonify({'token':token2,'username':user,'status':'success','message':'登陆成功:'+user})
            else:
                return jsonify({'token':'','status':'fail','message':'没有查询到用户'})
        except Exception as e:
            print(traceback.format_exc())
            return jsonify({'token':'','status':'fail','message':'未查询到用户'})
    else:
        try:
            data = jwt.decode(token, config.secret_key, algorithms=['HS256'])
            return jsonify({'message': 'Token is valid!','status':'success'})
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired','status':'fail'})
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token','status':'fail'})

#病人登录接口
@login_app.route('/patient_login',methods=['POST'])
def patient_login():
    token = request.headers.get('token')

    if token == "":
        try:
            data = request.get_json()
            tel = data["phone"]
            password = data["password"]
            print(tel)
            print(password)
            sql = "select name from patients where telephone = %s AND password = %s"

            operate = db.Database()
            result = operate.execute(sql,(tel,password))
            expiration_time = datetime.utcnow() + timedelta(days=15)
            if result:
                user = ''.join(result[0])
                print('user是'+user)
                token2 = jwt.encode({'name':result[0],'exp':expiration_time},config.secret_key,algorithm='HS256')
                print('后端user是'+user)
                return jsonify({'token':token2,'username':user,'status':'success','message':'登陆成功:'+user})
            else:
                return jsonify({'token':'','status':'fail','message':'没有查询到用户'})
        except Exception as e:
            print(traceback.format_exc())
            return jsonify({'token':'','status':'fail','message':'登陆失败，抛出异常'})
    else:
        try:
            data = jwt.decode(token, config.secret_key, algorithms=['HS256'])
            return jsonify({'message': 'Token is valid!','status':'success'})
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired','status':'fail'})
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token','status':'fail'})






     





