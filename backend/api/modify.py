from flask import Flask,request,jsonify,Blueprint
from flask_cors import CORS

modify_app = Blueprint('modify_app',__name__)



@modify_app.route('/modify_user_info',methods=['post'])
def modify():
    data = request.get_json()

    #进行增删改查等数据库操作

    return jsonify({'status':'success','message':'修改成功'})
