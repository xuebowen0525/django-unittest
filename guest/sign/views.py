from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required 
from sign.models import Event,Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.
def index(request):
    return render(request,'index.html')

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
@login_required  # 只能通过登录进到event_manage.html里
def event_manage(request):
    event_list = Event.objects.all()
    # username = request.COOKIES.get('user','')
    username = request.session.get('user','')
    return render(request,'event_manage.html',{'user':username,'event_list':event_list})

@login_required
def search_name(request):
    username = request.session.get('user','')
    search_name = request.GET.get('name','')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request,'event_manage.html',{'user':username,'event_list':event_list})

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

@login_required
def search_realname(request):
    username = request.session.get('user','')
    search_name = request.GET.get('name','')
    guest_list = Guest.objects.filter(realname__contains=search_name)
    return render(request,'guest_manage.html',{'user':username,'guest_list':guest_list})

@login_required
def sign_index(request,eid):
    event = get_object_or_404(Event,id=eid)
    return render(request,'sign_index.html',{'event':event})

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

@login_required 
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response