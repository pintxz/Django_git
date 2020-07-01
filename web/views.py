from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json, logging, datetime
from web import models
from api import punch

logger = logging.getLogger('log')


# Create your views here.

@require_http_methods(["GET"])
def testhtmls(request):
    logger.info('info的测试！')
    logger.error('error的测试！')
    logger.debug('debug的测试！')
    return render(request, 'index.html')


@require_http_methods(["GET"])
def add_book(request):
    response = {}
    try:
        book = Book(book_name=request.GET.get('book_name'))
        book.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


def api(request):
    ret = {"status": False, "error": {"user_error": "", "pwd_error": "", "login_error": ""}}
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        # print(request.body)  # b"{username:admin}"
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        # user_obj = models.User.objects.filter(name=name, pwd=pwd).first()
        # if user_obj:
        if pwd == '123456':
            ret['status'] = True
            fengjh = {"userId": 30594, "projectId": 50411, "ruleId": 51, "addrId": 315, "apprUserId": 29707,
                      "deptId": 12526,
                      "workReportType": "1", "longitude": "112.569206", "latitude": "37.811374",
                      "address": "山西省太原市小店区长治路228号",
                      "secondAppUser": "30586", "imagePath": ""}
            result = punch.dcits(fengjh)
            return HttpResponse(result)
        else:
            ret['error']['login_error'] = '用户名或密码错误'
            return render(request, 'login.html', ret)


def login(request):
    ret = {"status": False, "error": {"user_error": "", "pwd_error": "", "login_error": ""}}
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        # print(request.body)  # b"{username:admin}"
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        user_obj = models.User.objects.filter(name=name, pwd=pwd).first()
        if user_obj:
            ret['status'] = True
            return render(request, 'index.html', ret)
        else:
            ret['error']['login_error'] = '用户名或密码错误'
            return render(request, 'login.html', ret)


def index(request):
    user_obj = models.User.objects.get(name='admin')
    print(type(user_obj.name))
    print(user_obj.pwd)
    ret = {'name': [user_obj.name, user_obj.pwd], 'pwd': 'zzz'}
    return render(request, 'index.html', ret)


def test(request):
    ret = {"status": False, "error": {"user_error": "", "pwd_error": "", "login_error": ""}}
    ret['error']['login_error'] = '用户名或密码错误'
    # return HttpResponse(ret['error'])
    return HttpResponse(ret['error']['login_error'])


def LoginForm(request):  # 登陆校验实例
    ret = {"status": False, "error": {"user_error": "", "pwd_error": "", "login_error": ""}}
    if request.method == "POST":
        user = request.POST.get("name")  # 获取用户名
        pwd = request.POST.get("pwd")  # 获取密码
        if request.META['REMOTE_ADDR']:  # 判断是否获取用户IP地址
            access_ip = request.META['REMOTE_ADDR']  # 存到access_ip变量中
        else:
            access_ip = request.META['HTTP_X_FORWARDED_FOR']  # 获取用户的真实IP，非代理IP

        if access_ip:
            ip_obj = models.login_history.objects.filter(ip=access_ip).first()  # 在历史登录表中查找是否有这个IP

            if ip_obj:
                current_time = datetime.datetime.now()  # 获取当前时间
                second = current_time - ip_obj.utime  # 用当前时间减去最近登录的时间
                second = second.seconds  # 转换为秒数
                count = ip_obj.count  # 获取当前对象的登录次数
                count = count + 1  # 次数加1
                ip_obj.count = count  # 修改次数信息
                ip_obj.save()  # 保存
                if second < 60 and count >= 10:  # 判断秒数是否小于60秒并且次数大于等于10
                    ret["error"]["login_error"] = "过于频繁登录，你已经被锁着,等一会60秒之后再登录"
                    ip_obj.user = user  # 登录的用户名
                    ip_obj.lock = 1  # 值为1表示锁着
                    ip_obj.save()  # 保存
                    return HttpResponse(json.dumps(ret))  # 返回给前端
                elif ip_obj.lock == 1 and second >= 60:  # 判断lock是否等于1和秒数大于60秒
                    ip_obj.lock = 0  # 值为0表示解锁
                    ip_obj.count = 1  # 初始化登录次数
                    ip_obj.save()  # 保存
            else:
                models.login_history.objects.create(user=user, ip=access_ip, count=1, lock=0)  # 没有登录过，就创建记录

        if user:
            account_obj = models.User.objects.filter(username=user).first()  # 判断这个用户名是否存在
            if not account_obj:
                ret["error"]["user_error"] = "用户名错误或者不存在"
        else:
            ret["error"]["user_error"] = "用户名不能为空"

        if pwd == "":
            ret["error"]["pwd_error"] = "密码不能为空"


'''
        users = authenticate(username=user, password=pwd)  # 验证用户名和密码是否一样
        if users:
            request.session["user_id"] = users.pk  # 存储到session会话中
            initial_session(users, request)
            ret["status"] = True
            ip_obj.count = 1  # 登录次数等于1
            ip_obj.save()
            return HttpResponse(json.dumps(ret))  # 返回前端
        else:
            ret["error"]["pwd_error"] = "用户名或密码不正确"
        return HttpResponse(json.dumps(ret))
    return render(request, "login.html")

'''
