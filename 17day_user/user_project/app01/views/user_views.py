from django.shortcuts import redirect

from app01.forms import UserInfoModelForm
from app01.models import UserInfo
from app01.views.common import paginate_list_page, save_model_form


def user_list(request):
    """ 员工列表 """
    return paginate_list_page(
        request,
        UserInfo.objects.all(),
        "user_list.html",
        extra_context={"add_url": "/user/add/", "add_text": "新建用户"},
    )


def user_add(request):
    """ 添加员工（ModelForm） """
    return save_model_form(
        request, UserInfoModelForm, "form_layout.html", "/user/list/",
        form_title="新建用户", back_url="/user/list/",
    )


def user_edit(request, nid):
    """ 编辑员工（ModelForm） """
    instance = UserInfo.objects.filter(id=nid).first()
    if not instance:
        return redirect("/user/list/")
    return save_model_form(
        request, UserInfoModelForm, "form_layout.html", "/user/list/",
        instance=instance, form_title="编辑用户", back_url="/user/list/",
    )


def user_delete(request, nid):
    """ 删除员工 """
    UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")
