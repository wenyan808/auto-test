#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/31
# @Author  : zhangranghan

import os
import yaml



path = os.path.abspath(os.path.dirname(__file__))
with open('{}/application.yml'.format(path),'rb') as f:
    conf = yaml.load(stream=f,Loader=yaml.FullLoader)
    URL = conf['URL']
    ACCESS_KEY = conf['ACCESS_KEY']
    SECRET_KEY = conf['SECRET_KEY']
    hbsession = conf['hbsession']
    f.close()


