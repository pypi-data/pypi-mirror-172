from django.db import models
from django.contrib.auth.models import User
import uuid

def gen_uuid():
    return uuid.uuid4()



class WebTelemetry(models.Model):
    uuid = models.UUIDField(default=gen_uuid,editable=False,unique=True)
    time = models.DateTimeField(auto_now_add=True)
    host = models.CharField(max_length=1000)
    path = models.CharField(max_length=1000)
    method = models.CharField(max_length=50)
    uri = models.CharField(max_length=2000)
    status_code = models.IntegerField()
    user_agent = models.CharField(max_length=1000,blank=True,null=True)
    remote_addr = models.GenericIPAddressField()
    remote_addr_fwd = models.GenericIPAddressField(blank=True,null=True)
    meta = models.TextField()
    headers = models.TextField()
    cookies = models.TextField(blank=True,null=True)
    get = models.TextField(blank=True,null=True)
    post = models.TextField(blank=True,null=True)
    raw_post = models.TextField(blank=True,null=True)
    is_secure = models.BooleanField()
    is_ajax = models.BooleanField()
    response = models.TextField(null=True,blank=True)
    duration = models.CharField(null=True,blank=True,max_length=255)
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.DO_NOTHING)


class WebQuery(models.Model):

    sql = models.TextField(null=True)
    time = models.CharField(null=True,max_length=255)
    telemetry = models.ForeignKey(WebTelemetry,on_delete=models.CASCADE,null=True,related_name='queries')


