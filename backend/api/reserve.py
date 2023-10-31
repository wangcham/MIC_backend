from flask import Flask,request,jsonify,Blueprint
from flask_cors import CORS

reserve_app = Blueprint('reserve_app',__name__)
CORS(reserve_app)

@reserve_app.route('/reserve',methods=['post'])
def reserve():
    try:
        data = request.get_json()
        # username = data["username"]
        # time = data["time"]
        # doctor_id = data["doctor_id"]
        # sql = """
        # insert into appointment (username,time,doctor_id) VALUES (%s,%s,%s)
        # """

        #进行预约操作
        
        #省略调用官方接口
        return jsonify({'status':'success','message':'预约成功'})
    except Exception as e:
        return jsonify({'status':'fail','message':'预约失败'})