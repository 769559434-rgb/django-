from flask import Flask, render_template,request
import pymysql

app = Flask(__name__)

@app.route('/add/user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template("add_user.html")
    print(request.form)
    user = request.form.get('user')
    password = request.form.get('pwd')
    mobile = request.form.get('mobile')

    
    
    # 1. 连接MySQL服务器
    conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    charset='utf8mb4',
    database='unicom',
    )
    # 创建游标（只写一次！）
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 2. 插入数据
    sql = "insert into admin(username,password,mobile) values(%s,%s,%s)"
    cursor.execute(sql, [user, password, mobile])

    # 提交事务保存数据
    conn.commit()

    # 关闭资源
    cursor.close()
    conn.close()
    print("数据插入成功！")

    return "添加用户成功"


@app.route('/show/user', methods=['GET'])
def show_user():
     # 1. 连接MySQL服务器
    conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    charset='utf8mb4',
    database='unicom',
    )
    # 创建游标（只写一次！）
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 2. 查询数据
    sql = "select * from admin"
    cursor.execute(sql)
    data_list = cursor.fetchall()
    # 关闭资源
    cursor.close()
    conn.close()
    print("data_list")
    return render_template("show_user.html", users=data_list)

if __name__ == '__main__':
    app.run(debug=True)