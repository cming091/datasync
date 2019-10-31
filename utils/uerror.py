from tenacity import retry, stop_after_attempt
from config import Settings
from log.log_handler import LogHandler
logger = LogHandler(__name__)

class TError(Exception):
    pass

retry = retry(stop=stop_after_attempt(Settings.retryTimes))