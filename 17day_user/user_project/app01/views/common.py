from django.core.paginator import Paginator


def get_paginated_data(request, queryset, per_page=10):
    """ 通用分页函数：返回分页后的对象列表和分页器 """
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page", 1)
    try:
        page_obj = paginator.get_page(page_number)
    except Exception:
        page_obj = paginator.get_page(1)
    return page_obj