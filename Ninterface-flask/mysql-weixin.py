from flask import Flask, request, jsonify
import mysql.connector
app = Flask(__name__)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="weixin"
)
#查询department数据
@app.route('/get_data_departemnt', methods=['GET'])
def get_data_department():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM department")
    result = cursor.fetchall()
    data = []
    for row in result:
        data.append({'_id': row[0], 'dep_ment': row[1]})
    return jsonify(data)
#查询reglist数据
@app.route('/get_data_reglist', methods=['GET'])
def get_data_reglist():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM reglist")
    result = cursor.fetchall()
    data = []
    for row in result:
        data.append({'_id': row[0], 'dep_id': row[1],'dep_name': row[2]})
    return jsonify(data)
#查询alldist数据
@app.route('/get_data_alldlist', methods=['GET'])
def get_data_alldist():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM alldist")
    result = cursor.fetchall()
    data = []
    for row in result:
        data.append({'cost': row[0], 'good_at': row[1],'hospital': row[2],'name': row[3],'post': row[4],'doctor_id': row[5],'dep_id': row[6]})
    return jsonify(data)

#添加病人信息至patients
app.route('/add_data_patients', methods=['POST'])
def add_data_patients():
    data = request.get_json()
    cursor = mydb.cursor()
    sql = "INSERT INTO patients (age, born,id_card,name,phone) VALUES ({}, {},{},{},{})".format(data['age'],data['born'],data['id_card'],data['name'],data['phone'])
    cursor.execute(sql)
    mydb.commit()

# 查询patients数据
@app.route('/get_data_patients', methods=['GET'])
def get_data_patients():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM patients")
    result = cursor.fetchall()
    data = []
    for row in result:
        data.append({'age': row[0], 'born': row[1], 'id_card': row[2], 'name': row[3], 'phone': row[4]})
    return jsonify(data)

# 查询order数据
@app.route('/get_data_order', methods=['GET'])
def get_data_order():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM order")
    result = cursor.fetchall()
    data = []
    for row in result:
        data.append({'order_id': row[0], 'cancel': row[1], 'dep_ment': row[2], 'que_number': row[3], 'reg_cost': row[4],'remark': row[5],'time': row[6],'doctor_name': row[7],'order_name': row[8],'patients_name': row[9]})
    return jsonify(data)

#添加订单信息至order
app.route('/add_data_order', methods=['POST'])
def add_data_order():
    data = request.get_json()
    cursor = mydb.cursor()
    sql = "INSERT INTO order (order_id,cancel,dep_ment,que_number,reg_cost,remark,time,doctor_name,order_name,patients_name) VALUES ({}, {},{},{},{})".format(data['order_id'],data['cancel'],data['dep_ment'],data['que_number'],data['reg_cost'],data['remark'],data['time'],data['doctor_name'],data['order_name'],data['patients_name'])
    cursor.execute(sql)
    mydb.commit()

#添加信息至examination表单
app.route('/add_data_examination', methods=['POST'])
def add_data_examination():
    data = request.get_json()
    cursor = mydb.cursor()
    sql = "INSERT INTO examination (phy_name,phy_time,patients_id,patients_name) VALUES ({}, {},{},{})".format(data['phy_time'],data['phy_name'],['patient_id'],['patient_name'])
    mydb.commit()

# 查询examination数据
@app.route('/get_data_examination', methods=['GET'])
def get_data_examination():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM examination")
    result = cursor.fetchall()
    data = []
    for row in result:
        data.append({'phy_name': row[0], 'phy_time': row[1], 'patients_id': row[2], 'patients_name': row[3]})
    return jsonify(data)


#添加信息至hpv表单
app.route('/add_data_hpv', methods=['POST'])
def add_data_hpv():
    data = request.get_json()
    cursor = mydb.cursor()
    sql = "INSERT INTO hpv (name,id_card,gender、born_date、phone、cambo、ino_time、price、hpv_name) VALUES ({}, {},{},{},{})".format(data['name'],data['id_card'],data['gender'],data['born_date'],data['phone'],data['cambo'],data['ino_time'],data['price'],data['hpv_name'])
    cursor.execute(sql)
    mydb.commit()

# 查询hpv数据
@app.route('/get_data_hpv', methods=['GET'])
def get_data_hpv():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM hpv")
    result = cursor.fetchall()
    data = []
    for row in result:
        data.append({'name': row[0], 'id_card': row[1], 'gender': row[2], 'born_date': row[3],'phone': row[3],'cambo': row[4],'ino_time': row[5],'price': row[6],'hpv_name': row[7]})
    return jsonify(data)


if __name__ == '__main__':
    app.run()












