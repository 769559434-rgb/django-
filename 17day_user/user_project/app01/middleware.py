from django.shortcuts import redirect


class LoginRequiredMiddleware:
    """
    登录拦截中间件：未登录访问受保护页面时，跳转到登录页。
    白名单：登录页 /login/、登出 /logout/（静态文件由 Django 自行处理，不会走到这里）。
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 白名单直接放行
        if request.path.startswith("/login") or request.path.startswith("/logout"):
            return self.get_response(request)

        # 未登录：带上原本要访问的地址，登录成功后跳回去
        if not request.session.get("info"):
            return redirect(f"/login/?next={request.path}")

        return self.get_response(request)
