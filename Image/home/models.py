from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length = 30)
    password=models.CharField(max_length=32)
    email=models.EmailField()
    reg_time=models.DateTimeField(auto_now_add=True)
    headImg = models.FileField(upload_to = './static/upload/')

    def __unicode__(self):
        return self.username

class Shares(models.Model):
    share_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User)
    time=models.DateTimeField(auto_now_add=True)
    img=models.FileField(upload_to='./static/usershare/')
    is_hot=models.BooleanField(default=False)
    like=models.IntegerField(default=0)

    def __unicode__(self):
        return self.share_id

class Likes(models.Model):
    share=models.ForeignKey(Shares)
    user=models.ForeignKey(User)
    time=models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.time