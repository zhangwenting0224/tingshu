# !/usr/bin/python3.7.8
# -*- coding: utf-8 -*-
# @Date: 2022/2/26 20:39
# @Author: shidingming
# @Email: 2209832868@qq.com
# @Company: hulishuju

import logzero
import logging
from logzero import setup_logger

log_format = f'%(color)s[%(levelname)s %(asctime)s %(module)s:%(lineno)d] [pid:%(process)d] %(end_color)s %(message)s'
formatter = logzero.LogFormatter(fmt=log_format)
logger = setup_logger(name="tingshu", level=logging.DEBUG, formatter=formatter)
