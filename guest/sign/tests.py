from django.test import TestCase
from sign.models import Event,Guest
from django.contrib.auth.models import User
# Create your tests here. 执行：python manage.py test

#测试models模型
class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(id=1,name='iphone18',limit=200,status=True,address='杭州',start_time='2018-12-12 08:00:00')
        Guest.objects.create(id=1,event_id=1,realname='小明',phone='911',sign=False)
    def test_event_models(self):
        result = Event.objects.get(name='iphone18')
        self.assertEqual(result.address,'杭州') 
        self.assertTrue(result.status)
    def test_guest_models(self):
        result = Guest.objects.get(phone='911')
        self.assertEqual(result.realname,'小明')
        self.assertFalse(result.sign)
#测试index视图
class IndexPageTest(TestCase):
    def test_index_page_renders_index_template(self):
        response = self.client.get('/index/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')

#测试登录功能
class LoginActionTest(TestCase):
    def setUp(self):
        User.objects.create_user('xiaoming','123@126.com','123456')
    def test_add_user(self):
        #测试添加用户，密码传到服务器会转换为哈希值
        user = User.objects.get(username='xiaoming')
        self.assertEqual(user.username,'xiaoming')
        self.assertEqual(user.email,'123@126.com')
    def test_login_action_username_password_null(self):
        test_data={'username':'','password':''}
        response = self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'username or password error!',response.content)
    def test_login_action_username_passworf_erro(self):
        test_data={'username':'ming','password':'1234'}
        response = self.client.post('/login_action/',data=test_data)  
        self.assertEqual(response.status_code,200)
        self.assertIn(b'username or password error!',response.content)
    def test_login_action_username_password_success(self):
        test_data={'username':'xiaoming','password':'123456'}
        response = self.client.post('/login_action/',data=test_data)
        #登录之后重定向 状态码是302
        self.assertEqual(response.status_code,302)

#测试发布会管理页面
class EventTest(TestCase):
    def setUp(self):
        #页面需要登录才能进入，创建用户登录
        User.objects.create_user('xiaoming','123@126.com','123456')
        self.login_user={'username':'xiaoming','password':'123456'}
        Event.objects.create(id=1,name='iphone18',limit=200,status=True,address='杭州',start_time='2018-12-12 08:00:00')

    def test_event_mange_success(self):
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/event_manage/')
        self.assertEqual(response.status_code,200)
        b = bytes('杭州', encoding='utf-8')
        # response.content得到的是bytes 型的二进制数据 
        self.assertIn(b'iphone18',response.content)
        self.assertIn(b,response.content)

    def test_event_mange_search_success(self):
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/search_name/',{'name':'iphone18'})
        b = bytes('杭州', encoding='utf-8')
        self.assertIn(b,response.content)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'True',response.content)
#测试嘉宾管理系统
class GuestTest(TestCase):
    def setUp(self):
        User.objects.create_user('xiaoming','123@126.com','123456')
        self.login_user={'username':'xiaoming','password':'123456'}
        Guest.objects.create(id=1,event_id=1,realname='小明',phone='911',sign=False)
    
    def test_guest_mange_success(self):
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/guest_manage/')
        self.assertEqual(response.status_code,200)
        b = bytes('小明', encoding='utf-8')
        self.assertIn(b,response.content)
        self.assertIn(b'911',response.content)

    def test_guest_search_success(self):
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/search_realname/',{'realname':'小明'})
        b = bytes('小明', encoding='utf-8')
        self.assertIn(b,response.content)
        self.assertIn(b'911',response.content)

#测试用户签到
class SignIndexActionTest(TestCase):
    def setUp(self):
        User.objects.create_user('xiaoming','123@126.com','123456')
        self.login_user={'username':'xiaoming','password':'123456'}
        Event.objects.create(id=1,name='iphone18',limit=200,status=0,address='杭州',start_time='2018-12-12 08:00:00')
        Event.objects.create(id=2,name='iphone19',limit=200,status=1,address='杭州',start_time='2018-12-12 08:00:00')
        Guest.objects.create(event_id=1,realname='tom',phone='911',sign=0)
        Guest.objects.create(event_id=2,realname='luc',phone='912',sign=1)
    def test_index_phone_null(self):
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/sign_index_action/1/',{'phone':''})
        self.assertEqual(response.status_code,200)
        self.assertIn(b'phone erro',response.content)
    def test_index_phone_or_event_id_erro(self):
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/sign_index_action/1/',{'phone':'912'})
        self.assertEqual(response.status_code,200)
        self.assertIn(b'phone or event_id erro',response.content)
    def test_index_user_is_sign(self):
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/sign_index_action/2/',{'phone':'912'})
        self.assertEqual(response.status_code,200)
        self.assertIn(b'user is sign',response.content)
    def test_index_sign_success(self):
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/sign_index_action/1/',{'phone':'911'})
        result = Guest.objects.get(phone='911')
        self.assertEqual(response.status_code,200)
        self.assertIn(b'sign success',response.content)
        self.assertIn(b'tom',response.content)
        self.assertIn(b'911',response.content)
        self.assertEqual(result.sign,True)

        

