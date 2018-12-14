from django.http import JsonResponse
from sign.models import Event,Guest
from django.core.exceptions import ValidationError,ObjectDoesNotExist
import time
from django.db.utils import IntegrityError
#添加发布会接口
def add_event(request):
    eid = request.POST.get('eid','')
    name = request.POST.get('name','')
    limit = request.POST.get('limit','')
    status = request.POST.get('status','')
    address = request.POST.get('address','')
    start_time = request.POST.get('start_time','')

    if eid=='' or name=='' or limit=='' or address=='' or start_time=='':
        return JsonResponse({'status':10021,'message':'parameter error'})
    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'status':10022,'message':'event id exists'})
    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'sratus':10023,'message':'event name exists'})
    if status=='':
        status='1'
    try:
        Event.objects.create(id=eid,name=name,limit=limit,status=int(status),address=address,start_time=start_time)
    except ValidationError as e:
        erro = 'start_time erro'
        return JsonResponse({'status':10024,'message':erro})
    return JsonResponse({'status':200,'message':'add event success'})

#查询发布会接口
def get_event_list(request):
    eid = request.GET.get('eid','')
    name = request.GET.get('name','')
    if eid=='' and name=='':
        return JsonResponse({'status':10021,'message':'parameter error'})
    if eid !='':
        event={}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status':10022,'message':'query result is empty'})
        else:
            event['name']=result.name
            event['limit']=result.limit
            event['status']=result.status
            event['address']=result.address
            event['start_time']=result.start_time
            return JsonResponse({'status':200,'message':'success','data':event})
    if name != '':
        datas=[]
        results = Event.objects.filter(name__contains=name)
        if results:
            for r in results:
                event = {}
                event['name']=r.name
                event['limit']=r.limit
                event['status']=r.status
                event['address']=r.address
                event['start_time']=r.start_time
                datas.append(event)
            return JsonResponse({'status':200,'message':'success','data':datas})
        else:
            return JsonResponse({'status':10022,'message':'query result is empty'})

#添加嘉宾接口
def add_guest(request):
    eid = request.POST.get('eid','')
    realname = request.POST.get('realname','')
    phone = request.POST.get('phone','')
    if eid=='' and realname=='' and phone=='':
        return JsonResponse({'status':10021,'message':'parameter erro'})
    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status':10022,'message':'event id null'})
    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status':10023,'message':'event status is not available'})
    event_limit = Event.objects.get(id=eid).limit #发布会限制人数
    guest_limit = Guest.objects.filter(event_id=eid) #发布会已添加的嘉宾数
    if len(guest_limit) >= event_limit:
        return JsonResponse({'status':10024,'message':'event number is full'})
    event_time = Event.objects.get(id=eid).start_time #发布会开始时间
    etime = str(event_time).split('.')[0]
    timeArray = time.strptime(etime,"%Y-%m-%d %H:%M:%S")
    etime=int(time.mktime(timeArray))
    now_time = str(time.time())
    ntime = now_time.split(".")[0]
    n_time = int(ntime)
    if n_time >= e_time:
        return JsonResponse({'status':10025,'message':'event has start'})
    try:
        Guest.objects.create(realname=realname,phone=int(phone),sign=0,event_id=int(eid))
    except IntegrityError:
        return JsonResponse({'status':10026,'message':'the event guest phone number repeat'})
    return JsonResponse({'status':200,'message':'add guest success'})

#嘉宾查询接口
def get_guest_list(request):
    eid = request.GET.get('eid','')
    phone = request.GET.get('phone','')
    if eid=='':
        return JsonResponse({'status':10021,'message':'eid cannnot be empty'})
    if eid == '' and phone == '':
        datas=[]
        results = Guest.objects.filter(event_id=eid)
        if results:
            for r in results:
                guest={}
                guest['realname']=r.realname
                guest['phone']=r.phone
                guest['sign']=r.sign
                datas.append(guest)
            return jsonResponse({'status':200,'message':'success','data':datas})
        else:
            return jsonResponse({'status':10022,'message':'query result is empty'})
    if eid !='' and phone !='':
        guest={}
        try:
            result = Guest.objects.filter(event_id=eid,phone=phone)
        except ObjectDoesNotExist:
            return jsonResponse({'status':10022,'message':'query result is empty'})
        else:
            guest['realname']=r.realname
            guest['phone']=r.phone
            guest['sign']=r.sign
            return jsonResponse({'status':200,'message':'success','data':guest})

#嘉宾签到接口
def user_sign(request):
    eid = request.POST.get('eid','')
    phone = request.POST.get('phone','')
    if eid =='' and phone=='':
        return JsonResponse({'statue':10021,'message':'parameter erro'})
    result = Event.objects.filter(id = eid)
    if not result:
        return JsonResponse({'statue':10022,'message':'event id is null'})
    result = Event.objects.filter(id=eid).status
    if not result:
        return JsonResponse({'statue':10023,'message':'event status is not available'})
    event_time = Event.objects.get(id=eid).start_time #发布会开始时间
    etime = str(event_time).split('.')[0]
    timeArray = time.strptime(etime,"%Y-%m-%d %H:%M:%S")
    etime=int(time.mktime(timeArray))
    now_time = str(time.time())
    ntime = now_time.split(".")[0]
    n_time = int(ntime)
    if n_time >= e_time:
        return JsonResponse({'status':10024,'message':'event has start'})
    result = Event.objects.filter(phone=phone)
    if not result:
        return JsonResponse({'statue':10025,'message':'user phone null'})
    result = Event.objects.filter(id=eid,phone=phone)
    if not result:
        return JsonResponse({'statue':10026,'message':'user did not join conference'})
    result = Event.objects.filter(id=eid,phone=phone).sign
    if result:
        return JsonResponse({'statue':10027,'message':'user has sign in'})
    else:
        return JsonResponse({'statue':200,'message':'user sign success'})    


