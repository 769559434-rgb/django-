from flask import Flask
import pymysql

app = Flask(__name__)

# 数据库连接测试
try:
    conn = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="123456",
        charset="utf8mb4"
    )
    print("✅ MySQL 连接成功！")
    conn.close()
except Exception as e:
    print("❌ 连接失败：", e)

if __name__ == '__main__':
    app.run(debug=True)