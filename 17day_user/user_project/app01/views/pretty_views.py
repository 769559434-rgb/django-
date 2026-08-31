from django.shortcuts import redirect

from app01.forms import PrettyNumModelForm
from app01.models import PrettyNum
from app01.views.common import paginate_list_page, save_model_form


def pretty_list(request):
    """ 靓号列表 + 搜索 """
    return paginate_list_page(
        request,
        PrettyNum.objects.all(),
        "pretty_list.html",
        search_field="mobile",
        extra_context={
            "add_url": "/pretty/add/",
            "add_text": "新建靓号",
            "search_placeholder": "输入手机号搜索",
            "search_url": "/pretty/list/",
        },
    )


def pretty_add(request):
    """ 新增靓号 """
    return save_model_form(
        request, PrettyNumModelForm, "form_layout.html", "/pretty/list/",
        form_title="新建靓号", back_url="/pretty/list/",
    )


def pretty_edit(request, pk):
    """ 编辑靓号 """
    instance = PrettyNum.objects.filter(id=pk).first()
    if not instance:
        return redirect("/pretty/list/")
    return save_model_form(
        request, PrettyNumModelForm, "form_layout.html", "/pretty/list/",
        instance=instance, form_title="编辑靓号", back_url="/pretty/list/",
    )


def pretty_delete(request, pk):
    """ 删除靓号 """
    PrettyNum.objects.filter(id=pk).delete()
    return redirect("/pretty/list/")
