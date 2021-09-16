#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/31
# @Author  : zhangranghan


from common.util import order_http_post, order_http_get
from config.conf import URL2, MULANURL, hbsession


class LinearServiceOrder:

    def __init__(self, host, mulanhost, hbsession):
        self.__host = host
        self.__mulanhost = mulanhost
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

    # U本位永续划转
    def linear_transfer(self, currency=None, margin_account=None, amount=None, _from=None, _to=None):
        """===========================说明=================================
        #
        # currency: str  划转币种   例："BTC"，"ETH"
        # amount: str  数量      例： "10"，"0.01"
        # _from： str  从……转出    例："spot", "swap"
        # _to： str  转入……       例："spot", "swap"
        #
        """
        params = {}
        if currency:
            params['currency'] = currency
        if amount:
            params['amount'] = amount
        if margin_account:
            params['margin-account'] = margin_account
        if _from:
            params['from'] = _from
        if _to:
            params['to'] = _to

        request_path = '/v2/account/transfer'

        return order_http_post(self.__mulanhost, request_path, params, self.__hbsession)


# 定义t并传入hbsessionL,供用例直接调用
t = LinearServiceOrder(URL2, MULANURL, hbsession)
