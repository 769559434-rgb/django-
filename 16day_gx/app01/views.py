from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from app01.models import Department,UserInfo

# Create your views here.
def index(request):
    return HttpResponse("欢迎使用django框架")    

def orm(request):
    # 1. 先创建部门（不存在才新增，防止重复）
    dept_sale, _ = Department.objects.get_or_create(title="销售部")
    dept_it, _ = Department.objects.get_or_create(title="IT部")
    dept_op, _ = Department.objects.get_or_create(title="运营部")

    # 2. 新增 UserInfo 用户数据（get_or_create 避免重复）
    UserInfo.objects.get_or_create(
        name="张三",
        password="123",
        age=22
        
    )
    UserInfo.objects.get_or_create(
        name="李四",
        password="456",
        age=25
    )
    UserInfo.objects.get_or_create(
        name="小红",
        password="789",
        age=21
    )
    UserInfo.objects.get_or_create(
        name="小美",
        password="999",
        age=23
    
    )

    return HttpResponse("部门+用户数据插入完成，访问 /info_list/ 查看列表")

    # 仅演示：实际不要直接在视图无脑create，会重复新增
    # 先判断是否已经存在，避免重复插入
    if not Department.objects.filter(title="销售部").exists():
        Department.objects.create(title="销售部")
    if not Department.objects.filter(title="IT部").exists():
        Department.objects.create(title="IT部")
    if not Department.objects.filter(title="运营部").exists():
        Department.objects.create(title="运营部")

    return HttpResponse("orm操作数据成功")


def info_list(request):
    # 查询所有用户信息
    data_list = UserInfo.objects.all()
    print(data_list)
    return render(request,"info_list.html",{"data_list":data_list})



def add_user(request):
    #添加用户信息
    if request.method == "POST":
        name = request.POST.get("name")
        password = request.POST.get("password")
        age = request.POST.get("age")
 # 创建用户
        UserInfo.objects.create(name=name, password=password, age=int(age))
        
        # 新增完成，重定向到用户列表页（推荐，防止重复提交）
        
        return redirect("/info_list/")
    
    # ========== 关键修复：GET请求访问页面，返回表单模板 ==========
    return render(request, "add_user.html")


def delete_user(request, user_id):
    # 删除用户信息
    UserInfo.objects.filter(id=user_id).delete()
    return redirect("/info_list/")