from __future__ import unicode_literals
from django_unixdatetimefield import UnixDateTimeField
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.


  
class session(models.Model):
 session_name=models.CharField(max_length=80,blank=False)
 serverip=models.CharField(max_length=30,blank=False)
 pemfile=models.CharField(max_length=40,blank=False)
 user=models.ForeignKey(User,on_delete=models.CASCADE)

class instance(models.Model):
 instance_name=models.CharField(max_length=40,blank=False)
 session_name=models.ForeignKey(session,on_delete=models.CASCADE)
 serviceuser=models.ForeignKey(User,on_delete=models.CASCADE)
 port_normal=models.CharField(max_length=10,blank=False)
 port_ssl=models.CharField(max_length=10,blank=False)
 port_websockets=models.CharField(max_length=10,blank=False)
 class Meta:
  unique_together=(('instance_name','serviceuser'),)

class pidfile(models.Model):
 pid=models.IntegerField(blank=False)
 instance_name=models.ForeignKey(instance,on_delete=models.CASCADE)

 class Meta:
  unique_together=(('pid','instance_name'),)


