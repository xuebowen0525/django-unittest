from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required 
from sign.models import Event,Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import time
import datetime
# Create your views here.
#登录页面
def index(request):
    return render(request,'index.html')

#登录功能
def login_action(request):
    if request.method =='POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            response = HttpResponseRedirect('/event_manage/')
            # response.set_cookie('user',username,3600)
            request.session['user'] = username  
            return response
        else:
            return render(request,'index.html',{'error':'username or password error!'})

#发布会页面
@login_required  # 只能通过登录进到event_manage.html里
def event_manage(request):
    event_list = Event.objects.all()
    # username = request.COOKIES.get('user','')
    username = request.session.get('user','')
    return render(request,'event_manage.html',{'user':username,'event_list':event_list})

#搜索发布会名
@login_required
def search_name(request):
    username = request.session.get('user','')
    search_name = request.GET.get('name','')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request,'event_manage.html',{'user':username,'event_list':event_list})

#宾客页面
@login_required
def guest_manage(request):
    guest_list = Guest.objects.all().order_by('creat_time')
    username = request.session.get('user','')
    #将guest_list放到Paginator类中,每页显示2页数据
    paginator = Paginator(guest_list,2)
    #得到当前要显示page页的数据
    page = request.GET.get('page')
    try:
        #获取第page页的数据
        contacts = paginator.page(page)
    except PageNotAnInteger:
        #没有第page页会出PageNotAnInteger异常,显示第一页的数据
        contacts = paginator.page(1)
    except EmptyPage:
        #超出页数范围会出EmptyPage异常,显示最后一页的数据
        contacts = paginator.page(paginator.num_pages)
    return render(request,'guest_manage.html',{'user':username,'guest_list':contacts})

#搜索宾客名
@login_required
def search_realname(request):
    username = request.session.get('user','')
    search_name = request.GET.get('name','')
    guest_list = Guest.objects.filter(realname__contains=search_name)
    return render(request,'guest_manage.html',{'user':username,'guest_list':guest_list})

#签到页面
@login_required
def sign_index(request,eid):
    event = get_object_or_404(Event,id=eid)
    return render(request,'sign_index.html',{'event':event})

#签到功能
@login_required
def sign_index_action(request,eid):
    event = get_object_or_404(Event,id=eid)
    phone = request.POST.get('phone','')
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'phone erro'})
    result = Guest.objects.filter(phone=phone,event_id=eid)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'phone or event_id erro'})
    result = Guest.objects.filter(phone=phone,event_id=eid)
    if result[0].sign:
        return render(request,'sign_index.html',{'event':event,'hint':'user is sign'})
    else:
        result.update(sign=1)
        return render(request,'sign_index.html',{'event':event,'hint':'sign success','guest_list':result[0]})

#退出系统
@login_required 
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response

#修改发布会信息
@login_required
def change_event(request,eid):
    if request.method == "GET":
        event_result = Event.objects.get(id=eid)
        event_time = Event.objects.get(id=eid).start_time #发布会开始时间
        event_time = str(event_time).split('+')[0]   
        event_time1 = event_time.split(' ')[0]
        event_time2 = event_time.split(' ')[1]
        event_time = event_time1 + 'T' + event_time2
        time = event_time
        return render(request,'change_event.html',{'event_result':event_result,'time':time})
    elif request.method == "POST":
        name = request.POST.get('name')
        limit = request.POST.get('limit')
        status = request.POST.get('status')
        address = request.POST.get('address')
        start_time = request.POST.get('start_time')
        Event.objects.filter(id=eid).update(name=name,limit=limit,status=status,address=address,start_time=start_time)
        return render(request,'change_event.html',{'event_result':event_result,'time':time})

#增加发布会
def add_event(request):
    if request.method == "POST":
        name = request.POST.get('name')
        limit= request.POST.get('limit')
        status = request.POST.get('status')
        status = isTrue = status == str(True)
        address = request.POST.get('address')
        start_time = request.POST.get('start_time')  #2018-12-29T22:22  2017-11-23 16:10:10
        start_time = start_time.split('T')
        start_time = start_time[0] + ' ' + start_time[1] + ':00'
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        Event.objects.create(name=name,limit=int(limit),status=status,address=address,start_time=start_time)
        return HttpResponseRedirect('/event_manage/')
    return render(request,'add_event.html')

#删除发布会
def del_event(request):
    eid = request.GET.get('id')
    Event.objects.filter(id=eid).delete()
    return HttpResponseRedirect('/event_manage/')

#增加嘉宾
def add_guest(request):
    if request.method == "GET":
        event_list=Event.objects.all()
        return render(request,'add_guest.html',{'event_list':event_list})
    if request.method == "POST":
        realname = request.POST.get('realname')
        phone = request.POST.get('phone')
        sign = request.POST.get('sign')
        sign = isTrue = sign == str(True)
        event_id = request.POST.getlist('event')
        print(realname,phone,sign,event_id)
        if event_id:
            for id in event_id:
                Guest.objects.create(realname=realname,phone=int(phone),sign=sign,event_id=id)
        else:
            Guest.objects.create(realname=realname,phone=int(phone),sign=sign)
        return HttpResponseRedirect('/guest_manage/')
    return render(request,'add_guest.html')
#嘉宾删除功能
def del_guest(request):
    gid = request.GET.get('guest_id')
    Guest.objects.filter(id=gid).delete()
    return HttpResponseRedirect('/guest_manage/')
#嘉宾信息更改
def change_sign(request):
    gid = request.GET.get('guest_id')
    gl = Guest.objects.filter(id=gid)
    gl.update(sign=1)
    return HttpResponseRedirect('/guest_manage/')