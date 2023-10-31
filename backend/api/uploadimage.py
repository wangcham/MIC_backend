import imghdr
from flask import Flask, jsonify, request, Blueprint, send_file
import os
import db
import datetime
from config import origin_path
import net_work.segmentation as seg
from flask_cors import CORS
uploadimage_app = Blueprint('uploadimage_app', __name__)
CORS(uploadimage_app)
#匿名用户使用此功能，生成图片名称为分割时间
# 本文件需要的
ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg'}

path = origin_path

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_current_time():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')


@uploadimage_app.route('/pubfunc', methods=['POST'])
def uploadimage():
    doctor_id = request.form.get("username")
    image_file = request.files.get('image', None)
    print("id:"+doctor_id)
    if image_file is not None:
        if not allowed_file(image_file.filename):
            return jsonify({'message': '只允许上传jpg，jpeg和png类型的文件','status':'fail'})
    else:
        return jsonify({'message': '空文件！','status':'fail'})

    os.makedirs(path, exist_ok=True)

    # 获取拓展名
    ext = os.path.splitext(image_file.filename)[1]

    # 生成新的文件名
    image_name = get_current_time() + ext
    #path是///images，image_name是生成的文件名字
    image_path = os.path.join(path, image_name)
    image_file.save(image_path)
    print("保存新图片成功,保存在："+image_path)

    #进行分割操作
    operate = seg.operate()

    result = operate.pubrun(img_path=image_path)
    #分割操作完成

    try:
        params = (doctor_id,image_path)
        sql = "INSERT INTO uploaded_images (doctor_id, image_path) VALUES (%s, %s)"
        operate = db.Database()
        operate.execute(sql, params)
        print("存入数据库成功")
    except Exception as e:
        return jsonify({'status':'fail','message':'存入数据库操作失败'})

    try:
        image_type = imghdr.what(result)
        if image_type == 'jpeg':
            mimetype = 'image/jpeg'
        elif image_type == 'png':
            mimetype = 'image/png'
        else:
            print('不属于任何图片类型,mimetype被设置为空')
            mimetype = ''
        return send_file(result,mimetype=mimetype)
    
    except Exception as e:
        print(str(e))
        return jsonify({'status':'fail','message':'后端异常'})