import smtplib
import time
from .uerror import retry
from email.header import Header
from email.mime.text import MIMEText

from log.log_handler import LogHandler
logger = LogHandler(__name__)


class MailSend():
    def __init__(self, sender, pwd, name, receivers, host):
        self.sender =sender
        self.pwd = pwd
        self.name = name
        self.receivers = receivers
        self.host = host

    @property
    def now(self):
        return str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    def endSign(self):
        self.sendMail('sync ok', self.now)

    @retry
    def sendMail(self, subject, body):
        self.sendMailInner(self.sender,
                      self.pwd,
                      self.name,
                      self.receivers,
                      self.host,
                      subject,
                      body)


    def sendMailInner(self, sender, sender_pwd, sender_name, receivers, host, subject, body):
        msg = MIMEText(body, _subtype='html', _charset='utf-8')
        format_from = "%s<%s>" % (Header(sender_name, 'utf-8'), sender)
        msg['Subject'] = subject
        msg['From'] = format_from
        msg['To'] = ",".join(receivers) if type(receivers) is list else receivers
        msg["Accept-Language"] = "zh-CN"
        msg["Accept-Charset"] = "ISO-8859-1,utf-8"
        try:
            s = smtplib.SMTP()
            s.connect(host)
            s.ehlo()
            s.esmtp_features['auth'] = 'LOGIN DIGEST-MD5 PLAIN'
            s.login(sender, sender_pwd)
            s.sendmail(sender, receivers, msg.as_string())
            s.close()
        except Exception as e:
            logger.exception(e)
