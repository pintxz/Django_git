from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json, logging, datetime, random
from web import models
from functools import wraps
from api import punch

logger = logging.getLogger('log')
ret = {}

# 说明：这个装饰器的作用，就是在每个视图函数被调用时，都验证下有没法有登录，
# 如果有过登录，则可以执行新的视图函数，
# 否则没有登录则自动跳转到登录页面。
def check_login(f):
    @wraps(f)
    def inner(request, *arg, **kwargs):
        if request.session.get('is_login') == '1':
            return f(request, *arg, **kwargs)
        else:
            return redirect('/login')
    return inner


def test(request):
    '''
    punch.dcits('fengjh')
    return HttpResponse('123')
    119.45.15.183
    '''
    return HttpResponse('123')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        user_obj = models.User.objects.filter(name=name, pwd=pwd).first()
        if user_obj:
            # 登录成功
            # 1，生成特殊字符串
            # 2，这个字符串当成key，此key在数据库的session表（在数据库存中一个表名是session的表）中对应一个value
            # 3，在响应中,用cookies保存这个key ,(即向浏览器写一个cookie,此cookies的值即是这个key特殊字符）
            request.session['is_login'] = '1'  # 这个session是用于后面访问每个页面（即调用每个视图函数时要用到，即判断是否已经登录，用此判断）
            # request.session['username']=username  # 这个要存储的session是用于后面，每个页面上要显示出来，登录状态的用户名用。
            # 说明：如果需要在页面上显示出来的用户信息太多（有时还有积分，姓名，年龄等信息），所以我们可以只用session保存user_id
            request.session['user_name'] = user_obj.name
            request.session.set_expiry(15)
            # request.session.set_expiry(value)
            # 如果value是个整数，session会在些秒数后失效（适用于整个Django框架，即这个数值时效时整个页面都会session失效）。
            # 如果value是个datatime或timedelta，session就会在这个时间后失效。
            # 如果value是0, 用户关闭浏览器session就会失效。
            # 如果value是None, session会依赖全局session失效策略。
            return redirect('/index')
        else:
            ret['error']['login_error'] = '用户名或密码错误'
            return render(request, 'login.html', ret)


'''
            ret['status'] = True
            result = punch.dcits(name)
            return HttpResponse(result)
            # return render(request, 'result.html', result)
'''


def index(request):
    user_name = request.session.get('user_name')
    userobj = models.User.objects.filter(name=user_name)
    if userobj:
        global ret
        ret = {'name': userobj[0].name}
        return render(request, 'index.html', ret)
    else:
        return redirect('/login')

def punch_the_clock_api(request):
    user_name = request.session.get('user_name')
    userobj = models.User.objects.filter(name=user_name)
    if userobj:
        global ret
        result = punch.dcits(userobj[0].name)
        ret['date']= {"msg": result, "success": 'true'}
        return render(request, 'index.html', ret)
    else:
        return redirect('/login')



# 注销逻辑
def logout(request):
    # 把userName从当前的session移除
    # del request.session['login_user_name']
    request.session.flush()

    return redirect('/login')























