from django.shortcuts import render,redirect
from django import forms
from app01.models import Admin
from app01.views.common import get_paginated_data
from app01 import models
from app01.views.encrypt import md5_encrypt

# 第一步：先定义表单类（放在函数前面！）
class AdminModelForm(forms.ModelForm):
    confirm_pwd = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput()
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password"]
        widgets = {
            "password": forms.PasswordInput()
        }

    # clean方法缩进对齐到class，属于表单类内部
    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_pwd")

        if pwd != confirm:
            raise forms.ValidationError("两次密码不一致")
        else:
            cleaned_data["password"] = md5_encrypt(pwd)
           
        return cleaned_data


def admin_list(request):
    """管理员列表"""
    # 1.获取搜索参数
    search_key = request.GET.get("search", "")
    # 2.全部数据
    queryset = Admin.objects.all()
    # 3.有搜索词就过滤
    if search_key:
        queryset = queryset.filter(username__contains=search_key)
    # 4.分页
    page_obj = get_paginated_data(request, queryset)
    # 5.传给模板
    context = {
        "queryset": page_obj.object_list,
        "page_obj": page_obj,
        "search_key": search_key,
    }
    return render(request, "admin_list.html", context)


def admin_add(request):
    """添加管理员"""
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, "admin_add.html", {"form": form})

    # POST提交表单
    form = AdminModelForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "admin_add.html", {"form": form})