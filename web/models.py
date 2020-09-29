from django.db import models
# Create your models here.

'''
class Elements(models.Model):
    page = models.CharField(max_length=64)
    element = models.DateTimeField(auto_now_add=True)
    by = models.DateTimeField(auto_now_add=True)
    value = models.DateTimeField(auto_now_add=True)
    custom = models.DateTimeField(auto_now_add=True)
    remark = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.book_name
'''
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)


class ask(models.Model):
    name = models.CharField(max_length=32)
    openId = models.CharField(max_length=64)
    userId = models.IntegerField(blank=True, null=True)
    projectId = models.IntegerField(blank=True, null=True)
    ruleId = models.IntegerField(blank=True, null=True)
    addrId = models.IntegerField(blank=True, null=True)
    apprUserId = models.IntegerField(blank=True, null=True)
    deptId = models.IntegerField(blank=True, null=True)
    workReportType = models.CharField(max_length=32)
    secondAppUser = models.CharField(max_length=32)
    imagePath = models.CharField(max_length=32)
    model = models.CharField(max_length=64)
    prefectural = models.CharField(max_length=64)

class location(models.Model):
    id = models.AutoField(primary_key=True)
    longitude = models.CharField(max_length=32)
    latitude = models.CharField(max_length=32)
    address = models.CharField(max_length=1024)
    prefectural = models.CharField(max_length=64)

class phone_model(models.Model):
    id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=64)
    header_dict = models.CharField(max_length=1024)