import pymysql

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
while True:
    user = input("请输入用户名：")
    if user.upper() == 'Q':
        break
    password = input("请输入密码：")
    mobile = input("请输入手机号：")


    
 

    # 2. 插入数据
    sql = "insert into admin(username,password,mobile) values(%s,%s,%s)"
    cursor.execute(sql, [user, password, mobile])

    # 提交事务保存数据
    conn.commit()

 # 关闭资源
cursor.close()
conn.close()
print("数据插入成功！")