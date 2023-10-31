import imghdr
import traceback
from flask import Flask,Blueprint,request,jsonify, send_file
import db
from flask_cors import CORS

sendinfo_app = Blueprint('sendinfo_app',__name__)
CORS(sendinfo_app)

@sendinfo_app.route('/getinfo',methods=['POST'])
def sendinfo():

    sql = """
    select name,sex,age,status,id,telephone,surgery,doctor_id from patients
    """
    try:
        operate = db.Database()
        results = operate.execute(sql)

        data = []

        for result in results:
            name = result[0]
            sex = result[1]
            age = result[2]
            status = result[3]
            id = str(result[4])
            telephone = result[5]
            surgery = result[6]
            doctor_id = result[7]
            item = {'name':name,'sex':sex,'age':age,'status':status,'id':id,'telephone':telephone,'surgery':surgery,'doctor':doctor_id,'img':''}
            data.append(item)

        return jsonify(data)
    except Exception as e:
        return str(e)

@sendinfo_app.route('/get_info_image',methods=['POST'])
def get_info_image():

    patient_id = request.form.get("username")
    print("patient:"+patient_id)
    try:
        params = (int(patient_id),)
        print(type(int(patient_id)))

        sql = """
        SELECT imagepath from patients where id = %s
        """

    
        operate = db.Database()
        result = operate.execute(sql,params)
        imagepath = result[0]
        imagepath = str(result[0]).strip('(),').replace("'","")
        image_type = imghdr.what(imagepath)
        if image_type == 'jpeg':
            mimetype = 'image/jpeg'
        elif image_type == 'png':
            mimetype = 'image/png'
        else:
            print('不属于任何图片类型,mimetype被设置为空')
            mimetype = ''

        if len(result) == 0:
            return jsonify({'message':'没有查询结果','status':'fail'})
        else:
            print("发送图片的路径是:"+imagepath)
            return send_file(imagepath,mimetype=mimetype)
    except Exception as e:
        print(str(e))
        return str(e)


#get desc foe uniapp
@sendinfo_app.route('/getdesc',methods=['post'])
def getdesc():
    data = request.get_json()
    name = data['username']
    try:
        operate = db.Database()
        sql = """
        select description from patients where name = %s
        """

        result = operate.execute(sql,(name,))

        if result:
            desc = result[0][0]
            print("得到的desc是"+desc)
            return jsonify({'status':'success','message':'成功响应','desc':desc})
        else:
            return jsonify({'status':'fail','message':'未查询到医生评价'})

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'status':'fail','message':'抛出异常'}) 
    

@sendinfo_app.route('/senddesc',methods=['post'])
def senddesc():
    data = request.get_json()
    id = data['id']
    desc = data['desc']
    try:
        patient_id = int(id)
        print(patient_id)
        sql = """
        select description from patients where id = %s
        """
        operate = db.Database()
        result = operate.execute(sql,(patient_id,))
        if result[0][0]:
            return jsonify({'status':'exists','message':'已经存在点评！','desc':result[0][0]})
        else:
            sql2 = """
            update patients set description = %s where id = %s
            """
            operate.execute(sql2,(desc,patient_id,))
            return jsonify({'status':'success','message':'成功点评'})

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'status':'fail','message':'抛出异常'})
