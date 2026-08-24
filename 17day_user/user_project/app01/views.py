from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from app01 import models
# Create your views here.

def get_paginated_data(request, queryset, per_page=10):
    """ 通用分页函数：返回分页后的对象列表和分页器 """
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page", 1)
    try:
        page_obj = paginator.get_page(page_number)
    except Exception:
        page_obj = paginator.get_page(1)
    return page_obj

def depart_list(request):
    """ 部门列表 """

    # 1. 去数据库中倒入所有的部门数据
    queryset = models.Department.objects.all()
    page_obj = get_paginated_data(request, queryset)

    context = {
        "queryset": page_obj.object_list,
        "page_obj": page_obj,
    }
    return render(request, "depart_list.html", context)

def depart_add(request):
    """ 添加部门 """
    if request.method == "GET":
        return render(request, "depart_add.html")
    else:
        #获取用户提交的部门名称
        title = request.POST.get("title")
        #保存到数据库
        models.Department.objects.create(title=title)
        #返回部门列表页面
        return redirect("/depart/list/")


def depart_edit(request, nid):
    """ 编辑部门 """
    obj = models.Department.objects.filter(id=nid).first()
    if not obj:
        return redirect("/depart/list/")

    if request.method == "GET":
        return render(request, "depart_edit.html", {"obj": obj})
    else:
        title = request.POST.get("title")
        if title:
            obj.title = title
            obj.save()
        return redirect("/depart/list/")


def depart_delete(request, nid):
    """ 删除部门 """
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")


def user_add(request):
    """ 添加员工 """
    if request.method == "GET":
        # 获取所有部门，用于下拉选择
        depart_list = models.Department.objects.all()
        return render(request, "user_add.html", {"depart_list": depart_list})

    # POST 请求：处理表单提交
    name = request.POST.get("name")

    password = request.POST.get("password")
    age = request.POST.get("age")
    account = request.POST.get("account")
    create_time = request.POST.get("create_time")
    depart_id = request.POST.get("depart")
    gender = request.POST.get("gender")

    # 保存到数据库
    models.UserInfo.objects.create(
        name=name,
        password=password,
        age=age,
        account=account,
        create_time=create_time,
        depart_id=depart_id,
        gender=gender,
    )
    return redirect("/user/list/")


def user_list(request):
    """ 员工列表 """
    queryset = models.UserInfo.objects.all()
    page_obj = get_paginated_data(request, queryset)
    context = {
        "queryset": page_obj.object_list,
        "page_obj": page_obj,
    }
    return render(request, "user_list.html", context)


def user_edit(request, nid):
    """ 编辑员工 """
    obj = models.UserInfo.objects.filter(id=nid).first()
    if not obj:
        return redirect("/user/list/")

    if request.method == "GET":
        depart_list = models.Department.objects.all()
        return render(request, "user_edit.html", {"obj": obj, "depart_list": depart_list})

    # POST 请求：更新员工信息
    obj.name = request.POST.get("name", obj.name)
    obj.password = request.POST.get("password", obj.password)
    obj.age = request.POST.get("age", obj.age)
    obj.account = request.POST.get("account", obj.account)
    create_time = request.POST.get("create_time")
    if create_time:
        obj.create_time = create_time
    depart_id = request.POST.get("depart")
    if depart_id:
        obj.depart_id = depart_id
    obj.gender = request.POST.get("gender", obj.gender)
    obj.save()

    return redirect("/user/list/")


def user_delete(request, nid):
    """ 删除员工 """
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")

from django import forms
class User_ModelForm(forms.ModelForm):
    name = forms.CharField(min_length=2, label="姓名")
    class Meta:
        model = models.UserInfo
        fields = ["name","password","age","account","create_time","gender", "depart"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 给所有字段统一添加 Bootstrap 的 form-control 样式和占位提示
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}



def user_model_form_add(request):
    """添加员工ModelForm"""
    if request.method == "GET":
        form = User_ModelForm()
        return render(request, "user_model_form_add.html", {"form": form})

    # POST 请求：校验并保存数据
    form = User_ModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    else:
        return render(request, "user_model_form_add.html", {"form": form})

def user_edit(request,nid):
    
    """编辑员工ModelForm"""
    row_obj = models.UserInfo.objects.filter(id=nid).first()
    

    if request.method == "GET":
        #根据ID去数据库获取要编辑的那一行数据，展示在表单中
        form = User_ModelForm(instance=row_obj)
        return render(request, "user_edit.html",  {"form": form})

    # POST 请求：校验并保存数据
    form = User_ModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    else:
        return render(request, "user_edit.html", {"form": form})



from django.shortcuts import render, redirect
# 导入模型
from .models import PrettyNum
# 导入ModelForm，名字是PrettyNumModelForm
from .forms import PrettyNumModelForm


def pretty_list(request):
    """靓号列表"""
    query = PrettyNum.objects.all()
    return render(request, "pretty_list.html", {"queryset": query})


def pretty_add(request):
    """新增靓号"""
    form = PrettyNumModelForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("/pretty/list/")
    return render(request, "pretty_form.html", {"form": form})


def pretty_edit(request, pk):
    obj = PrettyNum.objects.get(id=pk)
    form = PrettyNumModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    return render(request, "pretty_form.html", {"form": form})


def pretty_delete(request, pk):
    """删除靓号"""
    PrettyNum.objects.filter(id=pk).delete()
    return redirect("/pretty/list/")

def pretty_list(request):
    """靓号列表 + 搜索"""
    # 获取url传递的搜索关键词 ?search=138
    search_key = request.GET.get("search", "")
    # 全部数据
    queryset = PrettyNum.objects.all()
    # 如果有搜索内容，模糊匹配手机号mobile
    if search_key:
        queryset = queryset.filter(mobile__contains=search_key)

    page_obj = get_paginated_data(request, queryset)
    context = {
        "queryset": page_obj.object_list,
        "page_obj": page_obj,
        "search_key": search_key,
    }
    return render(request, "pretty_list.html", context)