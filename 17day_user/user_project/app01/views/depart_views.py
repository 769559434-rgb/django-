from django.shortcuts import redirect

from app01.forms import DepartmentModelForm
from app01.models import Department
from app01.views.common import paginate_list_page, save_model_form


def depart_list(request):
    """ 部门列表 """
    return paginate_list_page(
        request,
        Department.objects.all(),
        "depart_list.html",
        extra_context={"add_url": "/depart/add/", "add_text": "新建部门"},
    )


def depart_add(request):
    """ 添加部门 """
    return save_model_form(
        request, DepartmentModelForm, "form_layout.html", "/depart/list/",
        form_title="新建部门", back_url="/depart/list/",
    )


def depart_edit(request, nid):
    """ 编辑部门 """
    instance = Department.objects.filter(id=nid).first()
    if not instance:
        return redirect("/depart/list/")
    return save_model_form(
        request, DepartmentModelForm, "form_layout.html", "/depart/list/",
        instance=instance, form_title="编辑部门", back_url="/depart/list/",
    )


def depart_delete(request, nid):
    """ 删除部门 """
    Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")
