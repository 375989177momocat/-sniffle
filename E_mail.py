import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import random as R

class send_check_email:
# my_user=input('请输入邮箱')      # 收件人邮箱账号，我这边发送给自己
    def mail(self):
        my_sender='2458767404@qq.com'    # 发件人邮箱账号
        my_pass = 'wlmholjxkrmleaai'              # 发件人邮箱密码(当时申请smtp给的口令)
        ret=True
        address = input('请输入邮箱地址')
        check_txt = str(R.randrange(100000,1000000))
        # try:
        msg=MIMEText('尊敬的用户：感谢您登录**！请输入下面的验证码完成登录\n'+check_txt)
        msg['From']=formataddr(["组名",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']=formataddr(["收件人昵称",address])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject']= '这是您账户登录的验证码,请在120秒内完成操作'            # 邮件的主题，也可以说是标题

        server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender,[address,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        check_click = input("请输入接收到的验证码\n")
        if check_click == check_txt :
            print("验证通过")
        elif check_click != check_txt:
            print("验证不通过")
        server.quit()
        return address
        # 关闭连接
    # except Exception:# 如果 try 中的语句没有执行，则会执行下面的 ret=False
    #     ret=False
    # return ret
if __name__ =='__main__':
    s = send_check_email()
    print(s.mail())