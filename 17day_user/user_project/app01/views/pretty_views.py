from django.shortcuts import render, redirect
from app01.models import PrettyNum
from app01.forms import PrettyNumModelForm
from app01.views.common import get_paginated_data


def pretty_list(request):
    """靓号列表 + 搜索"""
    search_key = request.GET.get("search", "")
    queryset = PrettyNum.objects.all()
    if search_key:
        queryset = queryset.filter(mobile__contains=search_key)

    page_obj = get_paginated_data(request, queryset)
    context = {
        "queryset": page_obj.object_list,
        "page_obj": page_obj,
        "search_key": search_key,
    }
    return render(request, "pretty_list.html", context)


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