from django.shortcuts import redirect

from app01.forms import AdminModelForm, AdminEditForm, AdminResetForm
from app01.models import Admin
from app01.views.common import paginate_list_page, save_model_form


def admin_list(request):
    """ 管理员列表 + 搜索 """
    return paginate_list_page(
        request,
        Admin.objects.all(),
        "admin_list.html",
        search_field="username",
        extra_context={
            "add_url": "/admin/add/",
            "add_text": "新建管理员",
            "search_placeholder": "输入用户名搜索",
            "search_url": "/admin/list/",
        },
    )


def admin_add(request):
    """ 添加管理员 """
    return save_model_form(
        request, AdminModelForm, "form_layout.html", "/admin/list/",
        form_title="新建管理员", back_url="/admin/list/",
    )


def admin_edit(request, pk):
    """ 编辑管理员（只改用户名） """
    instance = Admin.objects.filter(id=pk).first()
    if not instance:
        return redirect("/admin/list/")
    return save_model_form(
        request, AdminEditForm, "form_layout.html", "/admin/list/",
        instance=instance, form_title="编辑管理员", back_url="/admin/list/",
    )


def admin_reset(request, pk):
    """ 重置管理员密码 """
    instance = Admin.objects.filter(id=pk).first()
    if not instance:
        return redirect("/admin/list/")
    return save_model_form(
        request, AdminResetForm, "form_layout.html", "/admin/list/",
        instance=instance, form_title="重置密码", back_url="/admin/list/",
    )


def admin_delete(request, pk):
    """ 删除管理员 """
    Admin.objects.filter(id=pk).delete()
    return redirect("/admin/list/")
