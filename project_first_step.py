# 登录注册  

from mysqlpython import Mysqlpython
from pymysql import *
import getpass
from hashlib import sha1
import zhenzismsclient as smsclient
import random as R
from E_mail import send_check_email

class first_step:
    def __init__(self):
        pass
        #等待所需调用参数

    def change(self,select):
        #等待传入数据字符串进行解析
        #传回解析后的数据
        #return数据
        return select

    def showmain(self):
        #等待客户选择注册页面
        while True:
            select = input('通过鼠标点击得到的数据  \n1登录 2注册 3忘记密码\n')
            if user.change(select) == "1": #1.登录
                user.login()
            if user.change(select) == "2": #2.注册  
                user.set_in()
            if user.change(select) == "3": #3.忘记密码
                user.forget_password()
            else:
                print("操作有误")
            # else: #语音数据分析配对不上
                # print("您的指令小P听得不是很清楚，再重试一遍吧")
                #此处可有小弹窗弹出提示

    def phone_check(self):
        apiUrl = 'http://sms_developer.zhenzikj.com'
        appId = 100142
        appSecret = 'Y2RiMTQwZTYtOGVlOC00OTQ2LWJhMDMtYTYyOWM2NGM1Nzg3'
        client = smsclient.ZhenziSmsClient(apiUrl, appId, appSecret)
        massage_num = str(R.randrange(100000,1000000,))
        self.check_num = '【瞬时科技】短信验证码: '+massage_num+' 尊敬的用户，您正在使用手机号码操作,60秒内有效[验证码告知他人将导致风险，请勿泄露]\n更多信息可点击www.baidu.com进行了解\n期待您的到来'
        self.massage_num = massage_num
        result = client.send(int(self.userphone),'%s' % self.check_num)

    def login(self):
        #登录
        self.userphone = input("手动输入手机号码\n") # 输入登录信息
        self.userpassword = getpass.getpass()
        user.jiami() #加密处理后与数据库对接
        # 需要连接数据库
        connect_obj = Mysqlpython("database_user_first_info") #数据库中登录信息表
        sql = "select userpassword from user_info \
                where userphonename = %s ;" % self.userphone
                #match是通过语音输入的手机号码匹配出来的密码
        match = connect_obj.all(sql)
        if not match:
            print("用户未注册或匹配错误")
            key = input("重新输入还是进行忘记操作\n1.登录 2.注册 3.忘记密码 0.主页面\n") #点击页面显示按钮选择
            if key == '1':
                user.login()
            elif key == '3':
                user.forget_password()
            elif key == '0':
                user.showmain()
            elif key == '2':
                user.set_in()

        elif match[0][0] == self.userpassword:
            print("登录成功") 
            #调用第二页面的游戏大厅界面


    def jiami(self):
        #sha1加密
        s1= sha1()
        s1.update(self.userpassword.encode('utf8'))
        JM_password = s1.hexdigest()
        self.userpassword = JM_password #得到加密后的密码


    def set_in(self):
        #注册
        self.userphone = input("通过页面点击输入您需要注册的手机号码\n")
        password1 = input("通过页面点击设置第一次密码\n注意:密码长度不能少于6位,最大20位\n")
        password2 = input("通过页面点击设置第二次密码\n")
        if password1 == password2 and len(password1) >= 6 and len(self.userphone) ==11:
            connect_obj = Mysqlpython("database_user_first_info") #数据库中登录信息表
            sql = "select * from user_info \
                where userphonename = %s" % self.userphone #匹配表内是否已经注册过
            match = connect_obj.all(sql)
            if not match:
                user.phone_check()
                key = input("首次注册需要验证您的手机号码\n请输入您收到的验证码验证\n")
                if key == self.massage_num: #验证发送的短信验证码是否正确
                    print("注册成功")
                    key = input("是否进行邮箱验证以便后续使用？\n1.是 2.暂时不需要\n")
                    if key == '1':
                        s = send_check_email()
                        self.emailaddress = s.mail()
                    if key != '1':
                        pass

                    self.userpassword = password1
                    user.jiami()
                    sql = "insert into user_info values (0,'%s','%s','%s');" % (self.userphone,self.userpassword,self.emailaddress)
                    connect_obj.zhixing(sql) #将注册信息添加入数据库表
                    user.login() #返回登录界面重新登录
                else:
                    print("输入验证码不正确\n返回重新注册")
                    user.set_in()


            else:
                print("帐号已存在")
                key = input("返回登录界面或忘记密码\n 0返回主页面 1重新登录 2重新注册\n")
                if key == '0':
                    user.showmain()
                if key == '1':
                    user.login()
                if key == '２':
                    user.set_in()

        key = input("两次输入密码不一致或手机号码长度有误\n 0返回主页面 1登录 2重新注册\n")
        if key == '0':
            user.showmain()
        if key == '1':
            user.login()
        if key == '2':
            user.set_in()
    
    def forget_password(self):
        #忘记密码
        #调取通过手机短信验证码方式验证，通过进行处理
        self.userphone = input("页面上输入手机号码\n")
        connect_obj = Mysqlpython("database_user_first_info") #数据库中登录信息表
        sql = "select * from user_info \
            where userphonename = %s" % self.userphone #匹配表内是否已经注册过
        match = connect_obj.all(sql)
        if not match:
            print(" 手机号码没有注册或者手机号码长度有误\
                     \n请核实后操作")
            user.forget_password()
        else:
            user.phone_check()
        #发送短信验证码验证
            key = input("请输入你收到的验证码")
            if key == self.massage_num :
                #进行验证
                password1 = input("通过页面重新设置密码\n")
                password2 = input("通过页面再次输入密码\n")
                if password1 == password2 and len(password1) >= 6:
                    self.userpassword = password1
                    user.jiami()
                    sql = "update user_info set userpassword = '%s' where userphonename = '%s';" % (self.userpassword,self.userphone)
                    match = connect_obj.update_ziduan(sql)
                    print("重置成功\n将返回主页面登录")
                else:
                    print("两次密码输入不一致\n请重新操作")
                    user.forget_password()

            else:
                print("验证码不正确请确认")
                user.forget_password()

        #验证不通过，重新调用此方法

        #验证通过
        
    

    def connect_database(self):
        #连接数据库获取数据进行匹配
        pass




if __name__ == "__main__":
    user = first_step()
    user.showmain()