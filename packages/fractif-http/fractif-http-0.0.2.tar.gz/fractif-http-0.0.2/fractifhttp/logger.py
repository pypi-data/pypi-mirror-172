import coloredlogs
import urllib3
import logging

urllib3.disable_warnings()


class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(
            coloredlogs.ColoredFormatter(
                '%(asctime)s - '
                + '%(name)s %(funcName)s() (%(filename)s:%(lineno)d) - '
                + '%(levelname)s - %(message)s '
            )
        )
        self.logger.addHandler(ch)
