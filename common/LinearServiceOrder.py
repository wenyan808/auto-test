#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/31
# @Author  : zhangranghan


from common.util import order_http_post,order_http_get
from config.conf import URL,hbsession


class LinearServiceOrder:

    def __init__(self,host,hbsession):
        self.__host = host
        self.__hbsession = hbsession
        self.__path = '/linear-swap-order'

    # 获取合约信息
    def linear_contract_info(self,contract_code=None):

        params_list = []


        if contract_code:
            params_list.append('{}={}'.format('contract_code',contract_code))

        params = '&'.join(params_list)

        request_path = self.__path + '/x/v1/linear_swap_contract_info'

        return order_http_get(self.__host,request_path, params,self.__hbsession)


    # 获取用户账户信息
    def linear_account_info(self, contract_code=None):

        params = {}
        if contract_code:
            params['contract_code'] = contract_code

        request_path = self.__path + '/x/v1/linear_swap_account_info'

        return order_http_post(self.__host,request_path, params,self.__hbsession)


#定义t并传入hbsessionL,供用例直接调用
t = LinearServiceOrder(URL,hbsession)