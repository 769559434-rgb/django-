"""
app01 全部表单集中在这里（表单抽离）：
    - BootstrapModelForm   : 基类，统一给所有字段加 Bootstrap 样式
    - DepartmentModelForm  : 部门
    - UserInfoModelForm    : 员工
    - PrettyNumModelForm   : 靓号
    - AdminModelForm       : 管理员
"""
import re

from django import forms

from app01.models import Department, UserInfo, PrettyNum, Admin
from app01.utils import md5_encrypt


class _BootstrapMixin:
    """ 给表单所有字段统一加 form-control 样式和 placeholder """

    def _apply_bootstrap(self):
        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs.setdefault("placeholder", field.label)


class BootstrapModelForm(_BootstrapMixin, forms.ModelForm):
    """
    通用 ModelForm 基类：自动给每个字段加上 form-control 样式和 placeholder，
    让所有模块的表单不用再各自写一遍 __init__。
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()


class BootstrapForm(_BootstrapMixin, forms.Form):
    """ 通用 Form 基类（不存库的表单也用同一套样式） """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()


class LoginForm(BootstrapForm):
    """ 管理员登录表单 """
    username = forms.CharField(label="用户名")
    password = forms.CharField(label="密码", widget=forms.PasswordInput())


class DepartmentModelForm(BootstrapModelForm):
    """ 部门表单 """

    class Meta:
        model = Department
        fields = ["title"]


class UserInfoModelForm(BootstrapModelForm):
    """ 员工表单 """
    name = forms.CharField(min_length=2, label="姓名")

    class Meta:
        model = UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]


class PrettyNumModelForm(BootstrapModelForm):
    """ 靓号表单 """
    # 重写手机号，最小11位
    mobile = forms.CharField(
        label="手机号码",
        min_length=11,
        max_length=11,
    )

    class Meta:
        model = PrettyNum
        fields = ["mobile", "price", "level", "status"]

    def clean_mobile(self):
        """ 自定义校验手机号正则 """
        num = self.cleaned_data.get("mobile")
        if not re.match(r"^1[3-9]\d{9}$", num):
            raise forms.ValidationError("手机号格式不正确！")
        return num


class AdminModelForm(BootstrapModelForm):
    """ 新增管理员：用户名 + 密码 + 确认密码 """
    confirm_pwd = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = Admin
        fields = ["username", "password"]
        widgets = {
            "password": forms.PasswordInput(),
        }

    def clean(self):
        """ 两次密码一致则通过，并把密码加密后保存 """
        cleaned_data = super().clean()
        pwd = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_pwd")

        if pwd != confirm:
            raise forms.ValidationError("两次密码不一致")
        cleaned_data["password"] = md5_encrypt(pwd)

        return cleaned_data


class AdminEditForm(BootstrapModelForm):
    """ 编辑管理员：只改用户名，密码用“重置密码”单独改 """

    class Meta:
        model = Admin
        fields = ["username"]


class AdminResetForm(AdminModelForm):
    """ 重置密码：只改密码，不碰用户名（复用 AdminModelForm 的密码校验 + 加密逻辑） """
    password = forms.CharField(
        label="新密码",
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = Admin
        fields = ["password"]
