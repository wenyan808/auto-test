#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/31
# @Author  : zhangranghan


from common.util import order_http_post, order_http_get
from config.conf import URL2, MULANURL, hbsession


class LinearServiceOrder:

    def __init__(self, host, hbsession):
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

    # 计划委托下单
    def linear_swap_triggerOrder_insert(self,contract_code=None, trigger_type=None, trigger_price=None, order_price=None,
                                        order_price_type=None,symbol=None, volume=None, direction=None, offset=None, lever_rate=None):
        # 属性	                数据类型	是否必填	说明
        # contract_code	        String	否	    BTC-USDT
        # trigger_type	        String	是	    触发类型： ge大于等于(触发价比最新价大)；le小于(触发价比最新价小)
        # trigger_price	        Number	是	    触发价
        # order_price	        Number	否	    委托价
        # order_price_type	    String	否	    委托类型： 不填默认为limit; 限价：limit ，最优5档：optimal_5，最优10档：optimal_10，最优20档：optimal_20
        # volume	            Number	是	    委托数量(张)
        # direction	            String	是	    buy:买 sell:卖
        # offset	            String	是	    open:开 close:平
        # lever_rate	        Number	否	    开仓必须填写，平仓可以不填。杠杆倍数[开仓若有10倍多单，就不能再下20倍多单]
        params = {}
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

        request_path = self.__path + '/x/v1/linear_swap_triggerorder_insert'
        return order_http_post(self.__host, request_path, params, self.__hbsession)

    # 计划委托-撤单
    def linear_swap_triggerorder_cancel(self,contract_code=None, order_id=None):

        # 属性                       数据类型 是否必填        说明
        # contract_code             String      Y       合约BTC - USDT
        # order_id                  String      Y       用户订单ID（多个订单ID中间以","分隔,一次最多允许撤消50个订单 ）
        params = {}
        if contract_code:
            params['contract_code'] = contract_code
        if order_id:
            params['order_id'] = order_id

        request_path = self.__path + '/x/v1/linear_swap_triggerorder_cancel'
        return order_http_post(self.__host, request_path, params, self.__hbsession)

    # 限价单-当前挂单
    def linear_swap_openorders(self, contract_code=None,order_type='1'):
        # 属性	数据类型	是否必填	说明
        # page_index	Integer	是	页码
        # page_size	Integer	是	每页大小
        # contract_code	String	否	合约代码
        # order_type	String	否	多个以英文逗号隔开，1：限价单，3：对手价，4：闪电平仓，5：计划委托，6：post_only，7：最优5档，8：最优10档，9：最优20档，10：fok，11：ioc
        # trade_type	Integer	否	（不填默认查询全部，取值范围：0:全部,1:买入开多,2: 卖出开空,3: 买入平空,4: 卖出平多
        # sort_by	String	否	排序字段（降序），不填默认按照create_time降序，取值范围："created_at"：按订单创建时间进行降序，"update_time"：按订单更新时间进行降序
        params = {'page_index':1,'page_size':10 }
        if contract_code:
            params['contract_code'] = contract_code
        if order_type:
            params['order_type'] = order_type
        request_path = self.__path + '/x/v1/linear_swap_openorders'
        return order_http_post(self.__host, request_path, params, self.__hbsession)

    # 计划委托-获取当前委托
    def linear_swap_open_triggerorders(self, contract_code=None, trade_type=None):
        # 属性	            数据类型	是否必填	说明
        # contract_code	    String	N	    合约BTC-USDT
        # page_index	    Number	N	    第几页，不填默认第一页
        # page_size	        Number	N	    不填默认20，不得多于50
        # trade_type	    Integer	N	    （不填默认查询全部，取值范围：0:全部,1:买入开多,2: 卖出开空,3: 买入平空,4: 卖出平多
        params = {}
        if contract_code:
            params['contract_code'] = contract_code
        if trade_type:
            params['trade_type'] = trade_type

        request_path = self.__path + '/x/v1/linear_swap_open_triggerorders'
        return order_http_post(self.__host, request_path, params, self.__hbsession)


# 定义t并传入hbsessionL,供用例直接调用
t = LinearServiceOrder(URL2, MULANURL, hbsession)