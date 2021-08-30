#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/10
# @Author  : zhangranghan


from common.util import api_http_get, api_key_post,api_key_get
from config.conf import URL,ACCESS_KEY,SECRET_KEY


class OptionService:

    def __init__(self,url,access_key,secret_key):
        self.__url = url
        self.__access_key = access_key
        self.__secret_key = secret_key






    # 获取合约信息
    def option_contract_info(self,symbol=None,trade_partition=None,contract_type=None,contract_code=None):
        """
        :param symbol:
        :param trade_partition:
        :param contract_type:
        :param contract_code:
        :return:
        """

        params = {}
        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition
        if contract_type:
            params['contract_type'] = contract_type
        if contract_code:
            params['contract_code'] = contract_code

        url = self.__url + '/option-api/v1/option_contract_info'
        return api_http_get(url, params)


    # 获取合约指数信息
    def option_index(self,symbol=None):
        """
        :param symbol:
        :return:
        """

        params = {}
        if symbol:
            params['symbol'] = symbol

        url = self.__url + '/option-api/v1/option_index'
        return api_http_get(url, params)


    # 获取合约最高限价和最低限价
    def option_price_limit(self,contract_code=None):
        """
        :param contract_code:
        :return:
        """

        params = {}
        if contract_code:
            params['contract_code'] = contract_code

        url = self.__url + '/option-api/v1/option_price_limit'
        return api_http_get(url, params)


    # 查询合约市场指标
    def option_market_index(self,symbol=None,trade_partition=None,contract_type=None,option_ritgh_type=None,contract_code=None):
        """
        :param symbol:
        :param trade_partition:
        :param contract_type:
        :param option_ritgh_type:
        :param contract_code:
        :return:
        """
        params = {}
        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition
        if contract_type:
            params['contract_type'] = contract_type
        if option_ritgh_type:
            params['option_ritgh_type'] = option_ritgh_type
        if contract_code:
            params['contract_code'] = contract_code

        url = self.__url + '/option-api/v1/option_market_index'
        return api_http_get(url, params)

    # 获取当前可用合约总持仓量
    def option_open_interest(self,symbol=None,trade_partition=None,contract_type=None,contract_code=None):
        """
        :param symbol:
        :param trade_partition:
        :param contract_type:
        :param contract_code:
        :return:
        """

        params = {}
        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition
        if contract_type:
            params['contract_type'] = contract_type
        if contract_code:
            params['contract_code'] = contract_code

        url = self.__url + '/option-api/v1/option_open_interest'
        return api_http_get(url, params)



    # 获取预估交割价
    def option_delivery_price(self,symbol=None,trade_partition=None):
        """
        :param symbol:
        :param trade_partition:
        :return:
        """

        params = {}
        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition

        url = self.__url + '/option-api/v1/option_delivery_price'
        return api_http_get(url, params)


    # 获取平台持仓量
    def option_his_open_interest(self,symbol=None,trade_partition=None,contract_type=None,period=None,size=None,amount_type=None,option_right_type=None):
        """
        :param symbol:
        :param trade_partition:
        :param contract_type:
        :param period:
        :param size:
        :param amount_type:
        :param option_right_type:
        :return:
        """

        params = {}
        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition
        if contract_type:
            params['contract_type'] = contract_type
        if period:
            params['period'] = period
        if size:
            params['size'] = size
        if amount_type:
            params['amount_type'] = amount_type
        if option_right_type:
            params['option_right_type'] = option_right_type

        url = self.__url + '/option-api/v1/option_his_open_interest'
        return api_http_get(url, params)



    # 查询系统状态
    def option_api_state(self,symbol=None,trade_partition=None):
        """
        :param symbol:
        :param trade_partition:
        :return:
        """
        params = {}
        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition

        url = self.__url + '/option-api/v1/option_api_state'
        return api_http_get(url, params)


    # 获取行情深度数据
    def option_depth(self,contract_code=None,type=None):
        """
        :param contract_code:
        :param type:
        :return:
        """

        params = {}
        if contract_code:
            params['contract_code'] = contract_code
        if type:
            params['type'] = type

        url = self.__url + '/option-ex/market/depth'
        return api_http_get(url, params)


    # 获取K线数据
    def option_kline(self,contract_code=None,period=None,size=None,From=None,to=None):
        """
        :param contract_code:
        :param period:
        :param size:
        :param From:
        :param to:
        :return:
        """

        params = {}
        if contract_code:
            params['contract_code'] = contract_code
        if period:
            params['period'] = period
        if size:
            params['size'] = size
        if From:
            params['from'] = From
        if to:
            params['to'] = to

        url = self.__url + '/option-ex/market/history/kline'
        return api_http_get(url, params)


    # 获取聚合行情
    def option_merged(self,contract_code=None):
        """
        :param contract_code:
        :return:
        """

        params = {}
        if contract_code:
            params['contract_code'] = contract_code


        url = self.__url + '/option-ex/market/detail/merged'
        return api_http_get(url, params)


    # 获取市场最近成交记录
    def option_trade(self,contract_code=None):
        """
        :param contract_code:
        :return:
        """

        params = {}
        if contract_code:
            params['contract_code'] = contract_code


        url = self.__url + '/option-ex/market/trade'
        return api_http_get(url, params)


    # 批量获取最近的交易记录
    def option_history_trade(self,contract_code=None,size=None):
        """
        :param contract_code:
        :param size:
        :return:
        """

        params = {}
        if contract_code:
            params['contract_code'] = contract_code
        if size:
            params['size'] = size

        url = self.__url + '/option-ex/market/history/trade'
        return api_http_get(url, params)


    # 获取用户账户信息
    def option_account_info(self,symbol=None,trade_partition=None):
        """
        :param symbol:
        :param trade_partition:
        :return:
        """

        params = {}
        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition

        request_path = '/option-api/v1/option_account_info'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)


    # 获取用户持仓信息
    def option_position_info(self,symbol=None,trade_partition=None,contract_code=None):
        """
        :param symbol:
        :param trade_partition:
        :param contract_code:
        :return:
        """

        params = {}
        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition
        if contract_code:
            params['contract_code'] = contract_code

        request_path = '/option-api/v1/option_position_info'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)


    # 查询母账户下所有子账户资产信息
    def option_sub_account_list(self,symbol=None,trade_partition=None):
        """
        :param symbol:
        :param trade_partition:
        :return:
        """
        params = {}
        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition

        request_path = '/option-api/v1/option_sub_account_list'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)


    # 查询母账户下的单个子账户资产信息
    def option_sub_account_info(self,symbol=None,trade_partition=None,sub_uid=None):
        """
        :param symbol:
        :param trade_partition:
        :param sub_uid:
        :return:
        """
        params = {}
        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition
        if sub_uid:
            params['sub_uid'] = sub_uid

        request_path = '/option-api/v1/option_sub_account_info'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)


    # 查询母账户下的单个子账户资产信息
    def option_sub_position_info(self,symbol=None,trade_partition=None,contract_code=None,sub_uid=None):
        """
        :param symbol:
        :param trade_partition:
        :param contract_code:
        :param sub_uid:
        :return:
        """
        params = {}
        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition
        if contract_code:
            params['contract_code'] = contract_code
        if sub_uid:
            params['sub_uid'] = sub_uid

        request_path = '/option-api/v1/option_sub_position_info'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)


    # 查询用户财务记录
    def option_financial_record(self,symbol=None,trade_partition=None,type=None,create_date=None,page_index=None,page_size=None):
        """
        :param symbol:
        :param trade_partition:
        :param type:
        :param create_date:
        :param page_index:
        :param page_size:
        :return:
        """

        params = {}
        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition
        if type:
            params['type'] = type
        if create_date:
            params['create_date'] = create_date
        if page_index:
            params['page_index'] = page_index
        if page_size:
            params['page_size'] = page_size


        request_path = '/option-api/v1/option_financial_record'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)


    # 获取用户当前的下单量限制
    def option_order_limit(self,symbol=None,trade_partition=None,order_price_type=None):
        """
        :param symbol:
        :param trade_partition:
        :param order_price_type:
        :return:
        """

        params = {}
        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition
        if order_price_type:
            params['order_price_type'] = order_price_type


        request_path = '/option-api/v1/option_order_limit'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 获取用户当前的手续费费率
    def option_fee(self,symbol=None,trade_partition=None):
        """
        :param symbol:
        :param trade_partition:
        :return:
        """

        params = {}
        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition

        request_path = '/option-api/v1/option_fee'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)


    # 获取用户当前的划转限制
    def option_transfer_limit(self,symbol=None,trade_partition=None):
        """
        :param symbol:
        :param trade_partition:
        :return:
        """

        params = {}
        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition

        request_path = '/option-api/v1/option_transfer_limit'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)


    # 获取用户当前的持仓量限制
    def option_position_limit(self,symbol=None,trade_partition=None):
        """
        :param symbol:
        :param trade_partition:
        :return:
        """

        params = {}
        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition

        request_path = '/option-api/v1/option_position_limit'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)


    # 获取用户资产和持仓信息
    def option_account_position_info(self,symbol=None,trade_partition=None):
        """
        :param symbol:
        :param trade_partition:
        :return:
        """

        params = {}
        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition

        request_path = '/option-api/v1/option_account_position_info'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)


    # 母子账户划转
    def option_master_sub_transfer(self,sub_uid=None,symbol=None,trade_partition=None,amount=None,type=None,client_order_id =None):
        """
        :param sub_uid:
        :param symbol:
        :param trade_partition:
        :param amount:
        :param type:
        :return:
        """

        params = {}
        if sub_uid:
            params['sub_uid'] = sub_uid
        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition
        if amount:
            params['amount'] = amount
        if type:
            params['type'] = type
        if client_order_id:
            params['client_order_id'] = client_order_id

        request_path = '/option-api/v1/option_master_sub_transfer'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)


    # 获取母账户下的所有母子账户划转记录
    def option_master_sub_transfer_record(self,symbol=None,trade_partition=None,transfer_type=None,create_date=None,page_index=None,page_size=None):
        """
        :param symbol:
        :param trade_partition:
        :param transfer_type:
        :param create_date:
        :param page_index:
        :param page_size:
        :return:
        """

        params = {}
        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition
        if transfer_type:
            params['transfer_type'] = transfer_type
        if create_date:
            params['create_date'] = create_date
        if page_index:
            params['page_index'] = page_index
        if page_size:
            params['page_size'] = page_size


        request_path = '/option-api/v1/option_master_sub_transfer_record'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)


    # 获取用户API指标禁用信息
    def option_api_trading_status(self):
        """
        :return:
        """

        params = {}

        request_path = '/option-api/v1/option_api_trading_status'
        return api_key_get(self.__url, request_path, params, self.__access_key, self.__secret_key)


    # 合约下单
    def option_order(self,contract_code=None,client_order_id=None,price=None,volume=None,direction=None,offset=None,order_price_type=None):
        """
        :param contract_code:
        :param client_order_id:
        :param price:
        :param volume:
        :param direction:
        :param offset:
        :param order_price_type:
        :return:
        """

        params = {}
        if contract_code:
            params['contract_code'] = contract_code
        if client_order_id:
            params['client_order_id'] = client_order_id
        if price:
            params['price'] = price
        if volume:
            params['volume'] = volume
        if direction:
            params['direction'] = direction
        if offset:
            params['offset'] = offset
        if order_price_type:
            params['order_price_type'] = order_price_type

        request_path = '/option-api/v1/option_order'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)




    # 合约批量下单
    def option_batchorder(self,orders_data=None):
        """
        :param orders_data:
        :return:
        """

        params=orders_data

        request_path = '/option-api/v1/option_batchorder'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)


    # 撤销订单
    def option_cancel(self,order_id=None,client_order_id=None,trade_partition=None):
        """
        :param order_id:
        :param client_order_id:
        :param trade_partition:
        :return:
        """

        params = {}

        if order_id:
            params['order_id'] = order_id
        if client_order_id:
            params['client_order_id'] = client_order_id
        if trade_partition:
            params['trade_partition'] = trade_partition

        request_path = '/option-api/v1/option_cancel'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)



    # 撤销全部订单
    def option_cancelall(self,symbol=None,trade_partition=None,contract_type=None,contract_code=None,direction=None,offset=None):
        """
        :param trade_partition:
        :param contract_type:
        :param contract_code:
        :return:
        """

        params = {}
        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition
        if contract_type:
            params['contract_type'] = contract_type
        if contract_code:
            params['contract_code'] = contract_code
        if direction:
            params['direction'] = direction
        if offset:
            params['offset'] = offset

        request_path = '/option-api/v1/option_cancelall'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)



    # 获取用户的订单信息
    def option_order_info(self,order_id=None,client_order_id=None,symbol=None,trade_partition=None):
        """
        :param order_id:
        :param client_order_id:
        :param symbol:
        :param trade_partition:
        :return:
        """

        params = {}

        if order_id:
            params['order_id'] = order_id
        if client_order_id:
            params['client_order_id'] = client_order_id
        if symbol:
            params['symbol'] = symbol
        if trade_partition	:
            params['trade_partition'] = trade_partition

        request_path = '/option-api/v1/option_order_info'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 获取用户的订单明细信息
    def option_order_detail(self,symbol=None,trade_partition=None,order_id=None,created_at=None,order_type=None,page_index=None,page_size=None):
        """
        :param symbol:
        :param trade_partition:
        :param order_id:
        :param created_at:
        :param order_type:
        :param page_index:
        :param page_size:
        :return:
        """


        params = {}

        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition
        if order_id:
            params['order_id'] = order_id
        if created_at	:
            params['created_at'] = created_at
        if order_type:
            params['order_type'] = order_type
        if page_index:
            params['page_index'] = page_index
        if page_size	:
            params['page_size'] = page_size


        request_path = '/option-api/v1/option_order_detail'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)



    # 获取用户的当前未成交委托
    def option_openorders(self,symbol=None,trade_partition=None,contract_code=None,sort_by=None,trade_type=None,page_index=None,page_size=None):
        """
        :param symbol:
        :param trade_partition:
        :param contract_code:
        :param page_index:
        :param page_size:
        :return:
        """

        params ={}

        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition
        if contract_code:
            params['contract_code'] = contract_code
        if sort_by:
            params['sort_by'] = sort_by
        if trade_type:
            params['trade_type'] = trade_type
        if page_index:
            params['page_index'] = page_index
        if page_size:
            params['page_size'] = page_size

        request_path = '/option-api/v1/option_openorders'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)



    # 获取用户的历史委托
    def option_hisorders(self,symbol=None,trade_partition=None,trade_type=None,type=None,status=None,create_date=None,sort_by=None,page_index=None,page_size=None,contract_code=None,order_type=None):
        """
        :param symbol:
        :param trade_partition:
        :param trade_type:
        :param type:
        :param status:
        :param creste_date:
        :param page_index:
        :param page_size:
        :param contract_code:
        :param order_type:
        :return:
        """

        params = {}

        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition
        if trade_type:
            params['trade_type'] = trade_type
        if type:
            params['type'] = type
        if status:
            params['status'] = status
        if create_date:
            params['create_date'] = create_date
        if contract_code:
            params['contract_code'] = contract_code
        if page_index:
            params['page_index'] = page_index
        if page_size:
            params['page_size'] = page_size
        if contract_code:
            params['contract_code'] = contract_code
        if order_type:
            params['order_type'] = order_type
        if sort_by:
            params['sort_by'] = sort_by


        request_path = '/option-api/v1/option_hisorders'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)



    # 获取用户的历史成交记录
    def option_matchresults(self,symbol=None,trade_partition=None,trade_type=None,create_date=None,contract_code=None,page_index=None,page_size=None):
        """
        :param symbol:
        :param trade_partition:
        :param trade_type:
        :param create_date:
        :param contract_code:
        :param page_index:
        :param page_size:
        :return:
        """

        params = {}

        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition
        if trade_type:
            params['trade_type'] = trade_type
        if create_date:
            params['create_date'] = create_date
        if contract_code:
            params['contract_code'] = contract_code
        if page_index:
            params['page_index'] = page_index
        if page_size:
            params['page_size'] = page_size


        request_path = '/option-api/v1/option_matchresults'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)



    # 闪电平仓下单
    def option_lightning_close_position(self,contract_code=None,volume=None,direction=None,client_order_id=None,order_price_type=None):
        """
        :param contract_code:
        :param volume:
        :param direction:
        :param client_order_id:
        :param order_price_type:
        :return:
        """


        params = {}

        if contract_code:
            params['contract_code'] = contract_code
        if volume:
            params['volume'] = volume
        if direction:
            params['direction'] = direction
        if client_order_id:
            params['client_order_id'] = client_order_id
        if order_price_type:
            params['order_price_type'] = order_price_type


        request_path = '/option-api/v1/option_lightning_close_position'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)



    # 计划委托下单
    def option_trigger_order(self,contract_code=None,trigger_type=None,trigger_price=None,order_price=None,order_price_type=None,volume=None,direction=None,offset=None):
        """
        :param contract_code:
        :param trigger_type:
        :param trigger_price:
        :param order_price:
        :param order_price_type:
        :param volume:
        :param direction:
        :param offset:
        :return:
        """

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


        request_path = '/option-api/v1/option_trigger_order'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)


    # 计划委托撤单
    def option_trigger_cancel(self,symbol=None,trade_partition=None,order_id=None):
        """
        :param trade_partition:
        :param order_id:
        :return:
        """

        params = {}
        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition
        if order_id:
            params['order_id'] = order_id

        request_path = '/option-api/v1/option_trigger_cancel'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)


    # 计划委托全部撤单
    def option_trigger_cancelall(self,symbol=None,trade_partition=None,contract_code=None,contract_type=None,direction=None,offset=None):
        """
        :param symbol:
        :param trade_partition:
        :param contract_code:
        :param contract_type:
        :return:
        """

        params = {}

        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition
        if contract_code:
            params['contract_code'] = contract_code
        if contract_type:
            params['contract_type'] = contract_type
        if direction:
            params['direction'] = direction
        if offset:
            params['offset'] = offset


        request_path = '/option-api/v1/option_trigger_cancelall'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)



    # 获取计划委托当前委托
    def option_trigger_openorders(self,symbol=None,trade_partition=None,contract_code=None,trade_type=None,page_index=None,page_size=None):
        """
        :param symbol:
        :param trade_partition:
        :param contract_code:
        :param page_index:
        :param page_size:
        :return:
        """

        params = {}

        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition
        if contract_code:
            params['contract_code'] = contract_code
        if trade_type:
            params['trade_type'] = trade_type
        if page_index:
            params['page_index'] = page_index
        if page_size:
            params['page_size'] = page_size


        request_path = '/option-api/v1/option_trigger_openorders'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)


    # 获取计划委托历史委托
    def option_trigger_hisorders(self,symbol=None,trade_partition=None,contract_code=None,trade_type=None,status=None,create_date=None,sort_by=None,page_index=None,page_size=None):
        """
        :param symbol:
        :param trade_partition:
        :param contract_code:
        :param trade_type:
        :param status:
        :param create_date:
        :param page_index:
        :param page_size:
        :return:
        """

        params = {}

        if symbol:
            params['symbol'] = symbol
        if trade_partition:
            params['trade_partition'] = trade_partition
        if contract_code:
            params['contract_code'] = contract_code
        if trade_type:
            params['trade_type'] = trade_type
        if status:
            params['status'] = status
        if create_date:
            params['create_date'] = create_date
        if page_index:
            params['page_index'] = page_index
        if page_size:
            params['page_size'] = page_size
        if sort_by:
            params['sort_by'] = sort_by


        request_path = '/option-api/v1/option_trigger_hisorders'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)






#定义t并传入公私钥和URL,供用例直接调用
t = OptionService(URL,ACCESS_KEY,SECRET_KEY)