#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/31
# @Author  : zhangranghan


from common.util import order_http_post, order_http_get
from config.conf import URL, MULANURL, hbsession,USERINFO
import json

class SwapServiceOrder:

    def __init__(self, host, mulanhost, hbsession):
        self.__host = host
        self.__mulanhost = mulanhost
        self.__hbsession = hbsession
        self.__path = '/swap-order'

    def swap_order(self,contract_code=None,price=None,order_price_type='limit',volume=1,direction='buy',offset='open',
                   lever_rate=5,client_order_id=None,check_min_volume=None,
                   tp_trigger_price=None,tp_order_price=None,tp_order_price_type=None,
                   sl_trigger_price=None,sl_order_price=None,sl_order_price_type=None):
        #           限价单下单
        # 属性	                数据类型	是否必填	说明
        # contract_code	        String	否	BTC-USD
        # price	                Number	否	委托价
        # order_price_type	    String	是	委托类型： 限价：limit ，对手价：opponent，postOnly 订单：post_only，最优5档：optimal_5，最优10档：optimal_10，最优20档：optimal_20，ImmediateOrCancel订单：ioc ,opponent_ioc（对手价-IOC下单），optimal_5_ioc（最优5档-IOC下单），optimal_10_ioc（最优10档-IOC下单），optimal_20_ioc（最优20档-IOC下单），FillOrKill订单：fok, opponent_fok（对手价-FOK下单），optimal_5_fok（最优5档-FOK下单），optimal_10_fok（最优10档-FOK下单），optimal_20_fok（最优20档-FOK下单）
        # volume	            Number	是	委托数量(张)
        # direction	            String	是	buy:买 sell:卖
        # offset	            String	是	open:开 close:平
        # lever_rate	        Number	是	杠杆倍数[开仓若有10倍多单，就不能再下20倍多单]
        # client_order_id	    Number	N	客户自己填写和维护，必须为数字
        # check_min_volume	    Number	N	下单量取小处理：0-否，1-是
        # tp_trigger_price	    Number	N	止盈触发价格
        # tp_order_price	    Number	N	止盈委托价格（最优N档委托类型时无需填写价格）
        # tp_order_price_type	String	N	止盈委托类型,不填默认为limit; 限价：limit ，最优5档：optimal_5，最优10档：optimal_10，最优20档：optimal_20
        # sl_trigger_price	    Number	N	止损触发价格
        # sl_order_price	    Number	N	止损委托价格（最优N档委托类型时无需填写价格）
        # sl_order_price_type	String	N	止损委托类型,不填默认为limit; 限价：limit ，最优5档：optimal_5，最优10档：optimal_10，最优20档：optimal_20
        params = {}
        if contract_code:
            params['contract_code'] = contract_code
        if price:
            params['price'] = price
        if order_price_type:
            params['order_price_type'] = order_price_type
        if volume:
            params['volume'] = volume
        if direction:
            params['direction'] = direction
        if offset:
            params['offset'] = offset
        if lever_rate:
            params['lever_rate'] = lever_rate
        if client_order_id:
            params['client_order_id'] = client_order_id
        if check_min_volume:
            params['check_min_volume'] = check_min_volume
        if tp_trigger_price:
            params['tp_trigger_price'] = tp_trigger_price
        if tp_order_price:
            params['v'] = tp_order_price
        if tp_order_price_type:
            params['tp_order_price_type'] = tp_order_price_type
        if sl_trigger_price:
            params['sl_trigger_price'] = sl_trigger_price
        if sl_order_price:
            params['sl_order_price'] = sl_order_price
        if sl_order_price_type:
            params['sl_order_price_type'] = sl_order_price_type

        request_path = self.__path + '/x/v1/swap_order'
        return order_http_post(self.__host, request_path, params, self.__hbsession)


    # 获取合约信息
    def swap_contract_info(self,contract_code=None):

        params_list = []


        if contract_code:
            params_list.append('{}={}'.format('contract_code',contract_code))

        params = '&'.join(params_list)

        request_path = self.__path + '/x/v1/swap_contract_info'

        return order_http_get(self.__host,request_path, params,self.__hbsession)


    # 获取用户账户信息
    def swap_account_info(self, contract_code=None):

        params = {}
        if contract_code:
            params['contract_code'] = contract_code

        request_path = self.__path + '/x/v1/swap_account_info'

        return order_http_post(self.__host,request_path, params,self.__hbsession)

    def swap_cancel(self,contract_code=None,order_id=None,client_order_id=None):
        # 属性	            数据类型	是否必填	说明
        # contract_code	    String	Y	    合约代码,"BTC-USD"
        # order_id	        String	N	    用户订单ID（多个订单ID中间以","分隔,一次最多允许撤消50个订单 ）
        # client_order_id	String	N	    客户订单ID(多个订单ID中间以","分隔,一次最多允许撤消50个订单)）
        params = {}
        if contract_code:
            params['contract_code'] = contract_code
        if order_id:
            params['order_id'] = order_id
        if client_order_id:
            params['client_order_id'] = client_order_id
        request_path = self.__path+'/x/v1/swap_cancel'
        return order_http_post(self.__mulanhost, request_path, params, self.__hbsession)

    # 币本位永续划转
    def coinswap_transfer(self, currency=None, amount=None, _from=None, _to=None):
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
        if _from:
            params['from'] = _from
        if _to:
            params['to'] = _to

        request_path = '/v2/account/transfer'

        return order_http_post(self.__mulanhost, request_path, params, self.__hbsession)



# 定义t并传入hbsessionL,供用例直接调用
t = SwapServiceOrder(URL, MULANURL, hbsession)
userList = eval(USERINFO)
user01 = SwapServiceOrder(URL,URL,userList[0]['HB_SESSION'])
user02 = SwapServiceOrder(URL,URL,userList[1]['HB_SESSION'])
user03 = SwapServiceOrder(URL,URL,userList[2]['HB_SESSION'])