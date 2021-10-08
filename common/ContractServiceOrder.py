#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/31
# @Author  : zhangranghan


from common.util import order_http_post,order_http_get
from config.conf import URL,hbsession


class ContractServiceOrder:

    def __init__(self,host,hbsession):
        self.__host = host
        self.__hbsession = hbsession
        self.__path = '/contract-order'

    # 获取合约信息
    def contract_contract_info(self,symbol=None,contract_type=None,contract_code=None):

        params_list = []

        if symbol:
            params_list.append('{}={}'.format('symbol',symbol))
        if contract_type:
            params_list.append('{}={}'.format('contract_type',contract_type))
        if contract_code:
            params_list.append('{}={}'.format('contract_code',contract_code))

        params = '&'.join(params_list)

        request_path = self.__path + '/x/v1/contract_contract_info'

        return order_http_get(self.__host,request_path, params,self.__hbsession)


    # 获取用户账户信息
    def contract_account_info(self, symbol=None):

        params = {}
        if symbol:
            params['symbol'] = symbol

        request_path = self.__path + '/x/v1/contract_account_info'

        return order_http_post(self.__host,request_path, params,self.__hbsession)

    # 交割合约划转
    def contract_transfer(self, symbol=None, amount=None, _type=None):
        """===========================说明=================================
        #
        # symbol: str  划转币种   例："BTC"，"ETH"
        # amount: str  数量      例： "10"，"0.01"
        # _type： str  划转方向    "1":从币币到合约  "2"：从合约到币币
        #
        #
        """
        params = {}
        if symbol:
            params['symbol'] = symbol
        if amount:
            params['amount'] = amount
        if symbol:
            params['type'] = _type

        request_path = self.__path + '/x/v1/contract_transfer'

        return order_http_post(self.__host, request_path, params, self.__hbsession)

    #计划委托单报单
    def contract_triggerorder_insert(self, symbol=None,contract_type=None,contract_code=None,trigger_type=None,trigger_price=None,
                                     order_price=None,order_price_type=None,volume=None,direction=None,offset=None,lever_rate=None):
        """===========================说明=================================
        #
        # symbol: str  划转币种   例："BTC"，"ETH"
        # contract_type: str  合约类型      例： this_week:当周; next_week:下周; quarter:季度;
        # contract_code: String 例:"BTC190304"
        # trigger_type: String 触发类型： ge大于等于(触发价比最新价大)；le小于(触发价比最新价小)
        # trigger_price: Number 触发价
        # order_price : Number 委托价
        # order_price_type：String 委托类型： 不填默认为limit; 限价：limit ，最优5档：optimal_5，最优10档：optimal_10，最优20档：optimal_20
        # volume： Number 委托数量(张)
        # direction: String buy:买 sell:卖
        # offset: String open:开 close:平
        # offset： Number  开仓必须填写，平仓可以不填。杠杆倍数[开仓若有10倍多单，就不能再下20倍多单]
        #
        #
        """
        params = {}
        if symbol:
            params['symbol'] = symbol
        if contract_type:
            params['contract_type'] = contract_type
        if contract_code:
            params['contract_code'] = contract_code
        if trigger_type:
            params['trigger_type'] = trigger_type
        if trigger_price:
            params['trigger_price'] = trigger_price
        if order_price:
            params['order_price'] = order_price
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
        request_path = self.__path + '/x/v1/triggerorder_insert'

        return order_http_post(self.__host, request_path, params, self.__hbsession)
    #获取计划委托当前委托（未完成计划委托单列表）
    def contract_open_triggerorders(self,symbol=None,contract_code=None,page_index=None,page_size=None,trade_type=None):
        """属性	数据类型	是否必填	说明
            symbol	String	Y	BTC LTC
            contract_code	String	N	合约code
            page_index	Number	N	第几页，不填默认第一页
            page_size	Number	N	不填默认20，不得多于50
            trade_type	String	是	交易类型，0:全部，1:买入开多，2:卖出开空，3:买入平空，4:卖出平多"""
        params = {}
        if symbol:
            params['symbol'] = symbol
        if contract_code:
            params['contract_code'] = contract_code
        if page_index:
            params['page_index'] = page_index
        if page_size:
            params['page_size'] = page_size
        if trade_type:
            params['trade_type'] = trade_type
        request_path = self.__path + '/x/v1/contract_open_triggerorders'
        return order_http_post(self.__host, request_path, params, self.__hbsession)

    #全部撤单
    def contract_triggerorder_cancelall(self,symbol=None,contract_code=None):
        """
        属性	数据类型	是否必填	说明
        symbol	String	Y	BTC LTC
        contract_code	String	N	合约ID，（传合约ID时，是对单合约的全部撤单，为空时是对单币种的全部撤单）
        """
        params = {}
        if symbol:
            params['symbol'] = symbol
        if contract_code:
            params['contract_code'] = contract_code
        request_path = self.__path + '/x/v1/triggerorder_cancelall'
        return order_http_post(self.__host, request_path, params, self.__hbsession)
#定义t并传入hbsessionL,供用例直接调用
t = ContractServiceOrder(URL,hbsession)
