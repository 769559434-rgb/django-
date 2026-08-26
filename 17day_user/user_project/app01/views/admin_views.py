from django.shortcuts import render
from app01.models import Admin
from app01.views.common import get_paginated_data


def admin_list(request):
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