import imghdr
import traceback
from flask import Flask, request, jsonify, Blueprint, send_file
import db
import net_work.segmentation as seg
import threading
from flask_cors import CORS
getseg_app = Blueprint('getseg_app', __name__)
CORS(getseg_app)


@getseg_app.route('/getseg', methods=['POST'])
def getseg():
    data = request.get_json()
    patient_id = data['username']
    patient_id = int(patient_id)
    print(patient_id)
    if patient_id is None:
        return jsonify({'status': 'fail', 'message': '请求格式不正确，缺少 patient_id 参数。'})

    
    try:
        database = db.Database()
        sql1 = """
        select segpath from patients where id = %s
        """
        result = database.execute(sql1,(patient_id,))

        if not result:
            print("if")
            imagepath = str(result[0]).strip('(),').replace("'","")
            image_type = imghdr.what(imagepath)
            if image_type == 'jpeg':
                mimetype = 'image/jpeg'
            elif image_type == 'png':
                mimetype = 'image/png'
            else:
                print('不属于任何图片类型,mimetype被设置为空')
                mimetype = ''
            
            return send_file(imagepath,mimetype=mimetype)
        else:
            sql = """
            select imagepath from patients where id = %s
            """
            print("else")
            result = database.execute(sql, (patient_id,))
            imagepath = str(result[0]).strip('(),').replace("'","")
            if len(result) == 0:
                print("未查询到结果")
                return jsonify({'status': 'fail', 'message': '未找到与提供的 patient_id 匹配的患者。'})
            else:
                operate = seg.operate()
                result = operate.run(imagepath,patient_id)
                print(result)
    except Exception as e:
        print(str(e))
        return jsonify({'statis': 'fail', 'message': '服务器发生错误，无法执行图像分割。'})

    try:
        sql2 = """
        select segpath from patients where id = %s
        """
        database = db.Database()
        result = database.execute(sql2, (patient_id,))
        imagepath = str(result[0]).strip('(),').replace("'","")
        if len(result) == 0:
            return jsonify({'status': 'fail', 'message': '未找到与提供的 patient_id 匹配的患者。'})
        else:
            image_type = imghdr.what(imagepath)
            if image_type == 'jpeg':
                mimetype = 'image/jpeg'
            elif image_type == 'png':
                mimetype = 'image/png'
            else:
                print('不属于任何图片类型,mimetype被设置为空')
                mimetype = ''
                
            return send_file(imagepath,mimetype=mimetype)
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'status': 'fail', 'message': '服务器发生错误，无法执行图像分割。'})


#uniapp端
@getseg_app.route('/checkoutseg',methods=['POST'])
def checkoutseg():
    data = request.get_json()
    username = data['username']
    try:
        database = db.Database()
        sql1 = """
        select segpath from patients where name = %s
        """
        result = database.execute(sql1,(username,))

        if result:
            imagepath = str(result[0]).strip('(),').replace("'","")
            print("imagepath"+imagepath)
            image_type = imghdr.what(imagepath)
            
            print("Attempting to read image file:", imagepath)

            try:
                # 读取图像文件的代码
                with open(imagepath, 'rb') as f:
                    image_data = f.read()
                print("Image file read successfully.")
            except Exception as e:
                print("Error reading image file:", str(e))


            if image_type == 'jpeg':
                mimetype = 'image/jpeg'
            elif image_type == 'png':
                mimetype = 'image/png'
            else:
                print('不属于任何图片类型,mimetype被设置为空')
                mimetype = ''
            
            return send_file(imagepath,mimetype=mimetype)
        else:
            return jsonify({'status':'fail','message':'未找到分割图片信息'})
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'status':'fail','message':'出现异常'})    