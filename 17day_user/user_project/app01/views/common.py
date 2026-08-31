"""
公共工具：分页、通用列表页渲染、通用 ModelForm 新增/编辑
"""
from django.core.paginator import Paginator
from django.shortcuts import redirect, render


def get_paginated_data(request, queryset, per_page=10):
    """ 通用分页函数：返回分页后的 page_obj """
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page", 1)
    try:
        page_obj = paginator.get_page(page_number)
    except Exception:
        page_obj = paginator.get_page(1)
    return page_obj


def paginate_list_page(request, queryset, template_name, search_field=None, extra_context=None):
    """
    通用列表页：搜索 + 分页 + 渲染，返回 HttpResponse。
    :param request:        请求对象
    :param queryset:       待展示的查询集
    :param template_name:  列表模板（继承 list_layout.html）
    :param search_field:   可选，搜索字段名（如 "mobile"），传了才启用右上角搜索框
    :param extra_context:  可选，额外的模板上下文（如 add_url / add_text）
    """
    search_key = request.GET.get("search", "")
    if search_key and search_field:
        queryset = queryset.filter(**{f"{search_field}__contains": search_key})

    # 未排序的查询集直接分页会出现元素漂移警告，统一按 id 排序
    if not queryset.ordered:
        queryset = queryset.order_by("id")

    page_obj = get_paginated_data(request, queryset)
    context = {
        "queryset": page_obj.object_list,
        "page_obj": page_obj,
        "search_key": search_key,
    }
    if extra_context:
        context.update(extra_context)
    return render(request, template_name, context)


def save_model_form(request, form_class, template_name, success_url,
                    instance=None, form_title="表单", back_url="/"):
    """
    通用 ModelForm 新增/编辑：
      - POST 且校验通过 -> 保存并重定向到 success_url
      - 其余情况（GET / 校验失败）-> 渲染表单页（form_layout.html）
    :param request:       请求对象
    :param form_class:    表单类（继承 BootstrapModelForm）
    :param template_name: 表单模板（统一用 form_layout.html）
    :param success_url:   保存成功后跳转的地址
    :param instance:      编辑时传入要修改的对象，新增时为 None
    :param form_title:    表单页标题（如 "新建部门" / "编辑部门"）
    :param back_url:      表单页“返回”按钮地址
    """
    form = form_class(request.POST or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(success_url)

    return render(request, template_name, {
        "form": form,
        "form_title": form_title,
        "back_url": back_url,
    })
