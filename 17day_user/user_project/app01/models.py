from django.db import models

# Create your models here.
from django.db import models

class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name="部门名称", max_length=32)
    def __str__(self):
        # 返回要在下拉框显示的文本，一般是部门名称
        return self.title

class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name="入职时间")

    #无约束
    # depart_id = models.BigIntegerField(verbose_name="部门ID", default=1)  # 外键

    #有约束
    #-to,与那张表关联
    #级联删除
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)  # 外键
    #置空
    # depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", null=True, blank=True, on_delete=models.CASCADE)  # 外键

    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)




from django.db import models

class PrettyNum(models.Model):
    """靓号管理"""
    mobile = models.CharField(verbose_name="手机号码", max_length=11, unique=True)
    price = models.DecimalField(verbose_name="售价", max_digits=10, decimal_places=2)
    level_choices = (
        (1, "普通靓号"),
        (2, "高级靓号"),
        (3, "顶级靓号"),
    )

    level = models.SmallIntegerField(verbose_name="靓号等级", choices=level_choices, default=1)
    status_choices = (
        (1, "已占用"),
        (2, "未使用"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)
    create_time = models.DateTimeField(verbose_name="录入时间", auto_now_add=True)

    class Meta:
        verbose_name = "靓号"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.mobile
                                  