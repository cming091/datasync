from .uemail import MailSend
from .uerror import *
from .uio import ioUtils
from config import Settings


emailUtil = MailSend(*Settings.email)