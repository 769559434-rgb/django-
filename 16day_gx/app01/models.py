from django.db import models

# Create your models here.
class UserInfo(models.Model):
    name =  models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    age = models.IntegerField()

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

"""
    生成一张表
    create table app01_userinfo(
    id bigint auto_increment primary key,
    name varchar(32)
    ,password varchar(64),
    age int
)
"""
#新建数据 insert into app01_userinfo(title) values("销售部")
class Department(models.Model):
    title = models.CharField(max_length=16)

# Department.objects.create(title="销售部")

# ==========重点！！删掉下面两行！！不要放在models.py=========
# UserInfo.objects.create(name="alex",password="123",age=18)
# UserInfo.objects.create(name="alex",password="123",age=18)