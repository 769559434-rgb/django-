from django.shortcuts import redirect, render
from django import forms
from app01.models import UserInfo, Department
from app01.views.common import get_paginated_data


class User_ModelForm(forms.ModelForm):
    name = forms.CharField(min_length=2, label="姓名")

    class Meta:
        model = UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def user_add(request):
    """ 添加员工 """
    if request.method == "GET":
        depart_list = Department.objects.all()
        return render(request, "user_add.html", {"depart_list": depart_list})

    name = request.POST.get("name")
    password = request.POST.get("password")
    age = request.POST.get("age")
    account = request.POST.get("account")
    create_time = request.POST.get("create_time")
    depart_id = request.POST.get("depart")
    gender = request.POST.get("gender")

    UserInfo.objects.create(
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
    queryset = UserInfo.objects.all()
    page_obj = get_paginated_data(request, queryset)
    context = {
        "queryset": page_obj.object_list,
        "page_obj": page_obj,
    }
    return render(request, "user_list.html", context)


def user_edit(request, nid):
    """编辑员工ModelForm"""
    row_obj = UserInfo.objects.filter(id=nid).first()
    if not row_obj:
        return redirect("/user/list/")

    if request.method == "GET":
        form = User_ModelForm(instance=row_obj)
        return render(request, "user_edit.html", {"form": form})

    form = User_ModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    else:
        return render(request, "user_edit.html", {"form": form})


def user_delete(request, nid):
    """ 删除员工 """
    UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")


def user_model_form_add(request):
    """添加员工ModelForm"""
    if request.method == "GET":
        form = User_ModelForm()
        return render(request, "user_model_form_add.html", {"form": form})

    form = User_ModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    else:
        return render(request, "user_model_form_add.html", {"form": form})