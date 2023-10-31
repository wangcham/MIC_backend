from flask import Flask, Blueprint, request, jsonify
import db

search_app = Blueprint('search_app', __name__)

def handletime(datetime):
    date = datetime.replace("-", "")
    return date

@search_app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    datetime = data['datetime']
    name = data['name']
    telephone = data['telephone']

    date = handletime(datetime)
    try:
        sql = "SELECT * FROM patients WHERE 1=1"
        params = {}

        if datetime:
            sql += " AND imagepath LIKE %(date)s"
            params['date'] = f"%{date}%"

        if name:
            sql += " AND name LIKE %(name)s"
            params['name'] = f"%{name}%"

        if telephone:
            sql += " AND telephone = %(telephone)s"
            params['telephone'] = telephone

        operate = db.Database()
        results = operate.execute(sql, params)

        if not results:
            return jsonify({'message': '未查询到匹配结果'})

        res = []

        for result in results:
            name, sex, age, status, id, telephone, surgery = result
            item = {'name': name, 'sex': sex, 'age': age, 'status': status, 'id': id, 'telephone': telephone, 'surgery': surgery}
            res.append(item)

        return jsonify(res)
    except Exception as e:
        return str(e)
