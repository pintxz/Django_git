from django.db import models
# Create your models here.


class Elements(models.Model):
    page = models.CharField(max_length=64)
    element = models.DateTimeField(auto_now_add=True)
    by = models.DateTimeField(auto_now_add=True)
    value = models.DateTimeField(auto_now_add=True)
    custom = models.DateTimeField(auto_now_add=True)
    remark = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.book_name
