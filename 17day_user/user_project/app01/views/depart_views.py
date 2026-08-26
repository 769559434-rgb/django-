from django.shortcuts import redirect, render
from app01.models import Department
from app01.views.common import get_paginated_data


def depart_list(request):
    """ 部门列表 """
    queryset = Department.objects.all()
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
        title = request.POST.get("title")
        Department.objects.create(title=title)
        return redirect("/depart/list/")


def depart_edit(request, nid):
    """ 编辑部门 """
    obj = Department.objects.filter(id=nid).first()
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
    Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")