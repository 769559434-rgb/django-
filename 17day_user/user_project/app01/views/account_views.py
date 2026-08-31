from django.shortcuts import redirect, render

from app01.forms import LoginForm
from app01.models import Admin
from app01.utils import md5_encrypt


def login(request):
    """ 管理员登录：校验用户名和密码，成功则写入 session """
    # 已登录还访问登录页，直接回首页
    if request.session.get("info"):
        return redirect("/depart/list/")

    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = md5_encrypt(form.cleaned_data["password"])
        admin_obj = Admin.objects.filter(username=username, password=password).first()

        if admin_obj:
            # 登录成功：把管理员信息写进 session，作为“已登录”标记
            request.session["info"] = {"id": admin_obj.id, "username": admin_obj.username}
            # 支持登录后跳回原本要访问的页面（next 参数）
            next_url = request.GET.get("next", "")
            if next_url.startswith("/") and not next_url.startswith("//"):
                return redirect(next_url)
            return redirect("/depart/list/")

        # 用户名或密码错误
        form.add_error(None, "用户名或密码错误")

    return render(request, "login.html", {"form": form})


def logout(request):
    """ 退出登录：清空 session 并回登录页 """
    request.session.flush()
    return redirect("/login/")
