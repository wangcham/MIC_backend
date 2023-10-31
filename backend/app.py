from flask import Flask
import db
import config

#导入蓝图
from api.login import login_app
from api.search import search_app
from api.sendinfo import sendinfo_app
from api.uploadimage import uploadimage_app
from api.login import login_app
from api.getseg import getseg_app
from api.register import register_app
from api.reserve import reserve_app
from api.modify import modify_app


#注册蓝图生成应用
app = Flask(__name__)
app.register_blueprint(login_app)
app.register_blueprint(search_app)
app.register_blueprint(sendinfo_app)
app.register_blueprint(uploadimage_app)
app.register_blueprint(getseg_app)
app.register_blueprint(register_app)
app.register_blueprint(reserve_app)
app.register_blueprint(modify_app)


db_instance = db.Database(app)



if __name__ == '__main__':
    #删除表
    #db_instance.drop_all_tables()
    #创建表
    db_instance.create_tables(config.queryone)
    db_instance.create_tables(config.querytwo)
    db_instance.create_tables(config.querythree)
    db_instance.create_tables(config.queryfour)


    app.run(debug=True,host='0.0.0.0',port=5000)
