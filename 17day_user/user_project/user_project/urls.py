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

from django.contrib import admin
from django.urls import path
from app01 import views

urlpatterns = [
    # 部门管理
    # path("admin/", admin.site.urls),
    path("depart/list/", views.depart_list),
    path("depart/add/", views.depart_add),
    path("depart/edit/<int:nid>/", views.depart_edit),
    path("depart/delete/<int:nid>/", views.depart_delete),

    # 员工管理
    path("user/list/", views.user_list),
    path("user/add/", views.user_add),
    path("user/edit/<int:nid>/", views.user_edit),
    path("user/delete/<int:nid>/", views.user_delete),
    path("user/model/form/add/",views.user_model_form_add),
    path("user/edit/<int:nid>/",views.user_edit),
   #靓号管理
    path("pretty/list/", views.pretty_list, name="pretty_list"),
    path("pretty/add/", views.pretty_add, name="pretty_add"),
    path("pretty/edit/<int:pk>/", views.pretty_edit, name="pretty_edit"),
    path("pretty/del/<int:pk>/", views.pretty_delete, name="pretty_delete"),
]


