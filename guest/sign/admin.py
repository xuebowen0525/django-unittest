from django.contrib import admin
from sign.models import Event,Guest
# admin  admin123456
# Register your models here.
class EventAdmin(admin.ModelAdmin):
    search_fields = ['name'] #搜索栏
    list_filter = ['status'] #过滤器
    list_display=['id','name','status','address','start_time']

class GuestAdmin(admin.ModelAdmin):
    search_fields = ['realname','phone'] #搜索栏
    list_filter = ['sign'] #过滤器
    list_display=['realname','phone','sign','creat_time','event']

admin.site.register(Event,EventAdmin)
admin.site.register(Guest,GuestAdmin)