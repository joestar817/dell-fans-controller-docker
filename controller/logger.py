import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CustomFormatter(logging.Formatter):
    def format(self, record):
        desired_timezone = timezone(timedelta(hours=8))
        current_time = datetime.now(desired_timezone).strftime('%Y-%m-%d %H:%M:%S')
        record.customtime = current_time
        return super().format(record)


stream_handler = logging.StreamHandler()
stream_handler.setFormatter(CustomFormatter(' %(customtime)s [%(levelname)s] %(message)s'))
logger.addHandler(stream_handler)
