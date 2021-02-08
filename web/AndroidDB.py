from web import models
import logging

logger = logging.getLogger('log')


# 添加用户
def register(data):
    name = data['name']
    pwd = data['pwd']
    openId = data['openId']
    prefectural = data['prefectural']
    models.User.objects.create(name=name, pwd=pwd)
    models.ask.objects.create(name=name, openId=openId, model='废弃',prefectural=prefectural)


# 删除用户
def userdel(data):
    name = data['name']
    user = models.User.objects.filter(name=name).first()
    models.User.objects.filter(id=user.id).delete()
    ask_user = models.ask.objects.filter(name=name).first()
    models.ask.objects.filter(id=ask_user.id).delete()


# 修改用户
def change(data):
    name = data['name']
    pwd = data['pwd']
    openId = data['openId']
    prefectural = data['prefectural']
    models.User.objects.filter(name=name).update(pwd=pwd)
    models.ask.objects.filter(name=name).update(openId=openId, prefectural=prefectural)


# 查询用户
def inquire(data):
    name = data['name']
    pwd = models.User.objects.filter(name=name)[0].pwd
    openId = models.ask.objects.filter(name=name)[0].openId
    prefectural = models.ask.objects.filter(name=name)[0].prefectural
    user = {'name':name,'pwd':pwd,'openId':openId,'prefectural':prefectural}
    logger.info(user)


# 查询所有用户（管理权限）
def inquires():
    information = []
    users = models.User.objects.all()
    for user in users:
        name = user.name
        pwd = user.pwd
        openId = models.ask.objects.filter(name=name)[0].openId
        prefectural = models.ask.objects.filter(name=name)[0].prefectural
        user = {'name': name, 'pwd': pwd, 'openId': openId, 'prefectural': prefectural}
        logger.info(user)
        information.append(user)
    return information
