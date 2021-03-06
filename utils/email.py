from random import randint, sample
from time import strftime

from django.conf import settings
from django.core.mail import send_mail
from itsdangerous import TimedJSONWebSignatureSerializer


def send_register_active_email(email):
    random = randint(1000, 9999)
    serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 5 * 60)
    info = {
        'confirm': str(random) + strftime("%Y%m%d%H%M%S") + email,
    }
    token = serializer.dumps(info)
    token = token.decode('utf8')

    # 加密
    url = 'http://127.0.0.1:8000/active/{}'.format(token)

    # todo 发送邮件
    # 邮件主题
    subject = 'Chris博客账号激活'
    # 邮件信息，正文部分
    message = '欢迎注册Chris博客, 打开下面链接激活账号' + '\n' + url
    # 发送者，直接从配置文件中导入上面配置的发送者
    sender = settings.EMAIL_FROM
    # 接收者的邮箱，是一个列表，这里是前端用户注册时传过来的 email
    receiver = [email]
    # html结构的信息，其中包含了加密后的用户信息token
    html_message = '<a href=' + url + '>' + '欢迎注册Chris博客,点击激活博客账号' + '</a>'
    # 调用Django发送邮件的方法，这里传了5个参数
    send_mail(subject=subject, message=message, html_message=html_message, from_email=sender, recipient_list=receiver)


def send_reset_password_email(email):
    random_password = sample('abcdefghijklmnopqrstuvwxyz1234567890', 9)
    password = ''.join(random_password)
    # todo 发送邮件
    # 邮件主题
    subject = 'Chris博客重置密码'
    # 邮件信息，正文部分
    message = '密码已重置为{}'.format(password)
    # 发送者，直接从配置文件中导入上面配置的发送者
    sender = settings.EMAIL_FROM
    # 接收者的邮箱，是一个列表，这里是前端用户注册时传过来的 email
    receiver = [email]
    # html结构的信息
    html_message = '密码已重置为{}'.format(password)
    # 调用Django发送邮件的方法，这里传了5个参数
    send_mail(subject=subject, message=message, from_email=sender, recipient_list=receiver, html_message=html_message)
    return password
