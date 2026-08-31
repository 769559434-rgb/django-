"""
URL configuration for user_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from app01.views.depart_views import depart_list, depart_add, depart_edit, depart_delete
from app01.views.user_views import user_list, user_add, user_edit, user_delete
from app01.views.pretty_views import pretty_list, pretty_add, pretty_edit, pretty_delete
from app01.views.admin_views import admin_list, admin_add, admin_edit, admin_reset, admin_delete
from app01.views.account_views import login, logout




urlpatterns = [
    # 登录 / 登出
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),

    #部门
    path('depart/list/', depart_list, name="depart_list"),
    path('depart/add/', depart_add, name="depart_add"),
    path('depart/edit/<int:nid>/', depart_edit, name="depart_edit"),
    path('depart/delete/<int:nid>/', depart_delete, name="depart_delete"),

    #员工
    path('user/list/', user_list, name="user_list"),
    path('user/add/', user_add, name="user_add"),
    path('user/edit/<int:nid>/', user_edit, name="user_edit"),
    path('user/delete/<int:nid>/', user_delete, name="user_delete"),

    #靓号 ✅这里重点！加上name
    path('pretty/list/', pretty_list, name="pretty_list"),
    path('pretty/add/', pretty_add, name="pretty_add"),
    path('pretty/edit/<int:pk>/', pretty_edit, name="pretty_edit"),
    path('pretty/delete/<int:pk>/', pretty_delete, name="pretty_delete"),

    #管理员
    path('admin/list/', admin_list, name="admin_list"),
    path('admin/add/', admin_add, name="admin_add"),
    path('admin/edit/<int:pk>/', admin_edit, name="admin_edit"),
    path('admin/reset/<int:pk>/', admin_reset, name="admin_reset"),
    path('admin/delete/<int:pk>/', admin_delete, name="admin_delete"),
]