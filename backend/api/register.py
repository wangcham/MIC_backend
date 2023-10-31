from flask import Flask,request,Blueprint,jsonify
from flask_cors import CORS
import db

register_app = Blueprint('register_app',__name__)
CORS(register_app)
@register_app.route('/register',methods=['post'])
def register():
    telephone = request.form.get("phonenumber")
    password = request.form.get("password")
    try:
        operate = db.Database()
        sql = """
        select * from patients where telephone = %s
        """

        result = operate.execute(sql,(telephone))

        name = "未设置"
        username = "未设置"
        sex = "未设置"
        age = "未设置"
        doctor_id = "未设置"
        status = "无检查结果"
        imagepath = "无"
        segpath = "无"
        surgery = "未知"
        if result:
            return jsonify({'status':'fail','message':'用户已存在'})
        else:
            sql = """
            insert into patients (telephone,password,name,username,sex,age,doctor_id,status,imagepath,segpath,surgery) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            #全部置空
            operate.execute(sql,(telephone,password,name,username,sex,age,doctor_id,status,imagepath,segpath,surgery))
            
    except Exception as e:
        return jsonify({'status':'fail','message':'后端异常'})