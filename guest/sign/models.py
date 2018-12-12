from django.db import models

# Create your models here.
# 发布会表
class Event(models.Model):
    #标题
    name = models.CharField(max_length=100)
    # 参加人数 models.IntegerField 整形
    limit = models.IntegerField()
    # 状态 BooleanField(Blank=True) 布尔型不可为空
    status = models.BooleanField()
    #地址
    address = models.CharField(max_length=200)
    #开始时间
    start_time = models.DateTimeField()
    #修改时间
    creat_time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

#嘉宾表
class Guest(models.Model):
    event = models.ForeignKey(Event,on_delete=True)
    realname = models.CharField(max_length=64)
    phone = models.CharField(max_length=16)
    # email = models.EmailField()
    sign = models.BooleanField()
    creat_time = models.DateTimeField(auto_now=True)

    class Meta:
        #联合唯一unique_together
        unique_together = ("event","phone")

    def __str__(self):
        return self.realname