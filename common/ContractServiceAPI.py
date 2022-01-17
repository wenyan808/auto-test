#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/31
# @Author  : zhangranghan
from pprint import pprint
from common.redisComm import redisConf
from config.conf import DEFAULT_SYMBOL, USERINFO
from common.util import api_http_get, api_key_post, api_key_get
from config import conf
from config.conf import URL, ACCESS_KEY, SECRET_KEY, COMMON_ACCESS_KEY, COMMON_SECRET_KEY, DEFAULT_CONTRACT_CODE, ATP_SERVER_ACCESS_KEY, ATP_SERVER_SECRET_KEY
import time


class ContractServiceAPI:

    def __init__(self, url, access_key, secret_key):
        self.__url = url
        self.__access_key = access_key
        self.__secret_key = secret_key

    # 获取合约信息
    def contract_contract_info(self, symbol=None, contract_type=None, contract_code=None):
        """
        参数名称         参数类型  必填    描述
        symbol          string  false   "BTC","ETH"...
        contract_type   string  false   合约类型: this_week:当周 next_week:下周 quarter:季度
        contract_code   string  false   BTC181228
        备注：如果contract_code填了值，那就按照contract_code去查询，如果contract_code 没有填值，则按照symbol+contract_type去查询
        """
        params = {}
        if symbol:
            params['symbol'] = symbol
        if contract_type:
            params['contract_type'] = contract_type
        if contract_code:
            params['contract_code'] = contract_code
        url = self.__url + '/api/v1/contract_contract_info'
        return api_http_get(url, params)

    # 获取合约指数信息
    def contract_index(self, symbol=None):
        """
        :symbol    "BTC","ETH"...
        """
        if symbol:
            if '_' in symbol:
                symbol = symbol[:-3]
            params = {'symbol': symbol}
        else:
            params = {}

        url = self.__url + '/api/v1/contract_index'
        return api_http_get(url, params)

    # 获取合约最高限价和最低限价
    def contract_price_limit(self, symbol=None, contract_type=None, contract_code=None):
        """
        :symbol          "BTC","ETH"...
        :contract_type   合约类型: this_week:当周 next_week:下周 quarter:季度
        "contract_code   BTC180928
        备注：如果contract_code填了值，那就按照contract_code去查询，如果contract_code 没有填值，则按照symbol+contract_type去查询
        """
        params = {}
        if symbol:
            params['symbol'] = symbol
        if contract_type:
            params['contract_type'] = contract_type
        if contract_code:
            params['contract_code'] = contract_code

        url = self.__url + '/api/v1/contract_price_limit'
        return api_http_get(url, params)

    # 获取当前可用合约总持仓量
    def contract_open_interest(self, symbol=None, contract_type=None, contract_code=None):
        """
        :symbol          "BTC","ETH"...
        :contract_type   合约类型: this_week:当周 next_week:下周 quarter:季度
        "contract_code   BTC180928
        备注：如果contract_code填了值，那就按照contract_code去查询，如果contract_code 没有填值，则按照symbol+contract_type去查询
        """
        params = {'symbol': symbol,
                  'contract_type': contract_type,
                  'contract_code': contract_code}

        url = self.__url + '/api/v1/contract_open_interest'
        return api_http_get(url, params)

    # 获取行情深度
    def contract_depth(self, symbol=None, type=None):
        """
        :param symbol:   BTC_CW, BTC_NW, BTC_CQ , ...
        :param type: 可选值：{ step0, step1, step2, step3, step4, step5 （合并深度0-5）；step0时，不合并深度 }
        :return:
        """
        params = {'symbol': symbol,
                  'type': type}

        url = self.__url + '/market/depth'
        return api_http_get(url, params)

    # 获取KLine
    def contract_kline(self, symbol=None, period=None, size=None, From=None, to=None):
        """
        :param symbol  BTC_CW, BTC_NW, BTC_CQ , ...
        :param period: 可选值：{1min, 5min, 15min, 30min, 60min, 4hour, 1day, 1week, 1mon }
        :param size: [1,2000]
        :return:
        """
        params = {'symbol': symbol,
                  'period': period}
        if size:
            params['size'] = size
        if From:
            params['from'] = From
        if to:
            params['to'] = to

        url = self.__url + '/market/history/kline'
        return api_http_get(url, params)

    # 获取聚合行情
    def contract_detail_merged(self, symbol=None):
        """
        :symbol	    "BTC_CW","BTC_NW", "BTC_CQ" ...
        """
        params = {'symbol': symbol}

        url = self.__url + '/market/detail/merged'
        pprint(url)
        return api_http_get(url, params)

    # 获取市场最近成交记录
    def contract_trade(self, symbol=None):
        """
        :param symbol: 可选值：{ BTC_CW, BTC_NW, BTC_CQ, etc. }
        :return:
        """
        params = {'symbol': symbol}

        url = self.__url + '/market/trade'
        return api_http_get(url, params)

    # 获取最新价
    def current_redis_price(self, contract_code=None):
        # 如果未传合约，获取默认
        if contract_code is None:
            contract_code = DEFAULT_CONTRACT_CODE
            contractInfo = self.contract_contract_info(
                symbol=DEFAULT_SYMBOL)
            contract_code = contractInfo['data'][0]['contract_code']
        # 查询最新价
        redis_client = redisConf('redis6379').instance()
        redis_value = redis_client.hget('RsT:BILP:', 'CP:' + contract_code)
        print("{}:{}".format('RsT:BILPCP:' + contract_code, redis_value))
        # 以2个小数点返回结果
        last_price = redis_value.split('#')[0]
        return round(float(last_price), 2)

    # 批量获取最近的交易记录
    def contract_history_trade(self, symbol=None, size=None):
        """
        :param symbol: 可选值：{ BTC_CW, BTC_NW, BTC_CQ, etc. }, size: int
        :return:
        """
        params = {'symbol': symbol,
                  'size': size}
        url = self.__url + '/market/history/trade'
        return api_http_get(url, params)

    # 查询系统状态
    def contract_api_state(self, symbol=None):
        """
        :param symbol: "BTC","ETH"...,如果缺省，默认返回所有品种
        :return:
        """

        params = {}
        if symbol:
            params['symbol'] = symbol

        url = self.__url + '/api/v1/contract_api_state'
        return api_http_get(url, params)

    # 获取市场最优挂单
    def contract_bbo(self, symbol=None):
        """
        :param symbol: "BTC","ETH"...,如果缺省，默认返回所有品种
        :return:
        """

        params = {}
        if symbol:
            params['symbol'] = symbol

        url = self.__url + '/market/bbo'
        return api_http_get(url, params)

    # 批量获取聚合行情
    def contract_batch_merged(self, symbol=None):
        """
        :param symbol: "BTC","ETH"...,如果缺省，默认返回所有品种
        :return:
        """

        params = {}
        if symbol:
            params['symbol'] = symbol

        url = self.__url + '/market/detail/batch_merged'
        return api_http_get(url, params)

    # 获取标记价格的K线数据
    def contract_mark_price_kline(self, symbol=None, period=None, size=None):
        """
        :param symbol: "BTC","ETH"...,如果缺省，默认返回所有品种
        :return:
        """

        params = {}
        if symbol:
            params['symbol'] = symbol
        if period:
            params['period'] = period
        if size:
            params['size'] = size

        url = self.__url + '/index/market/history/mark_price_kline'
        return api_http_get(url, params)

    # 查询合约风险准备金余额和预估分摊比例
    def contract_risk_info(self, symbol=None):
        """

        :param symbol:
        :return:
        """

        params = {}

        if symbol:
            params['symbol'] = symbol

        request_path = '/api/v1/contract_risk_info'
        return api_key_get(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 批量设置子账户交易权限
    def contract_sub_auth(self, sub_uid=None, sub_auth=None):
        """
        :param symbol:
        :return:
        """
        params = {}

        if sub_uid:
            params['sub_uid'] = sub_uid
        if sub_auth:
            params['sub_auth'] = sub_auth

        request_path = '/api/v1/contract_sub_auth'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 批量获取子账户资产信息
    def contract_sub_account_info_list(self, symbol=None, page_index=None, page_size=None):
        """
        :param symbol:
        :return:
        """
        params = {}

        if symbol:
            params['symbol'] = symbol
        if page_index:
            params['page_index'] = page_index
        if page_size:
            params['page_size'] = page_size

        request_path = '/api/v1/contract_sub_account_info_list'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 获取用户账户信息
    def contract_account_info(self, symbol=None):
        """
        :param symbol: "BTC","ETH"...如果缺省，默认返回所有品种
        :return:
        """

        params = {}
        if symbol:
            params["symbol"] = symbol

        request_path = '/api/v1/contract_account_info'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 获取用户持仓信息
    def contract_position_info(self, symbol=None):
        """
        :param symbol: "BTC","ETH"...如果缺省，默认返回所有品种
        :return:
        """

        params = {}
        if symbol:
            params["symbol"] = symbol

        request_path = '/api/v1/contract_position_info'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 合约下单
    def contract_order(self, symbol=None, contract_type=None, contract_code=None,
                       client_order_id=None, price=None, volume=1, direction=None, offset='open',
                       lever_rate=5, order_price_type='limit', tp_trigger_price=None, tp_order_price=None,
                       tp_order_price_type=None,
                       sl_trigger_price=None, sl_order_price=None, sl_order_price_type=None, channel_code=None):
        """
        :symbol: "BTC","ETH"..
        :contract_type: "this_week", "next_week", "quarter"
        :contract_code: "BTC181228"
        :client_order_id: 客户自己填写和维护，这次一定要大于上一次
        :price             必填   价格
        :volume            必填  委托数量（张）
        :direction         必填  "buy" "sell"
        :offset            必填   "open", "close"
        :lever_rate        必填  杠杆倍数
        :order_price_type  必填   "limit"限价， "opponent" 对手价
        备注：如果contract_code填了值，那就按照contract_code去下单，如果contract_code没有填值，则按照symbol+contract_type去下单。
        :
        """

        params = {"price": price,
                  "volume": volume,
                  "direction": direction,
                  "offset": offset,
                  "lever_rate": lever_rate,
                  "order_price_type": order_price_type}
        if symbol:
            params["symbol"] = symbol
        if contract_type:
            params['contract_type'] = contract_type
        if contract_code:
            params['contract_code'] = contract_code
        if client_order_id:
            params['client_order_id'] = client_order_id
        if tp_trigger_price:
            params['tp_trigger_price'] = tp_trigger_price
        if tp_order_price:
            params['tp_order_price'] = tp_order_price
        if tp_order_price_type:
            params['tp_order_price_type'] = tp_order_price_type
        if sl_trigger_price:
            params['sl_trigger_price'] = sl_trigger_price
        if sl_order_price:
            params['sl_order_price'] = sl_order_price
        if sl_order_price_type:
            params['sl_order_price_type'] = sl_order_price_type
        if channel_code:
            params['channel_code'] = channel_code
        request_path = '/api/v1/contract_order'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 合约批量下单 ?
    def contract_batchorder(self, orders_data=None):
        """
        :symbol:        "BTC","ETH"..
        :contract_type: "this_week", "next_week", "quarter"
        :contract_code: "BTC181228"
        :client_order_id:   必填   客户自己填写和维护，这次一定要大于上一次
        :price              必填   价格
        :volume             必填   委托数量（张）
        :direction          必填   "buy" "sell"
        :offset             必填   "open", "close"
        :lever_rate         必填   杠杆倍数
        :order_price_type   必填   "limit"限价， "opponent" 对手价
        备注：如果contract_code填了值，那就按照contract_code去下单，如果contract_code没有填值，则按照symbol+contract_type去下单。
        :
        """

        params = orders_data

        request_path = '/api/v1/contract_batchorder'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 撤销订单
    def contract_cancel(self, symbol=None, order_id=None, client_order_id=None):
        """
        参数名称          是否必须 类型     描述
        order_id	         false  string  订单ID（ 多个订单ID中间以","分隔,一次最多允许撤消50个订单 ）
        client_order_id  false  string  客户订单ID(多个订单ID中间以","分隔,一次最多允许撤消50个订单)
        备注： order_id 和 client_order_id都可以用来撤单，同时只可以设置其中一种，如果设置了两种，默认以order_id来撤单。
        """

        params = {"symbol": symbol}
        if order_id:
            params["order_id"] = order_id
        if client_order_id:
            params["client_order_id"] = client_order_id
        # print(params)
        request_path = '/api/v1/contract_cancel'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 全部撤单
    def contract_cancelall(self, symbol=None, direction=None, offset=None):
        """
        symbol: BTC, ETH, ...
        """

        params = {"symbol": symbol}
        if direction:
            params['direction'] = direction
        if offset:
            params['offset'] = offset

        request_path = '/api/v1/contract_cancelall'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 获取合约订单信息
    def contract_order_info(self, symbol=None, order_id=None, client_order_id=None):
        """
        参数名称         是否必须  类型     描述
        order_id        false   string  订单ID（ 多个订单ID中间以","分隔,一次最多允许查询20个订单 ）
        client_order_id false   string  客户订单ID(多个订单ID中间以","分隔,一次最多允许查询20个订单)
        备注：order_id和client_order_id都可以用来查询，同时只可以设置其中一种，如果设置了两种，默认以order_id来查询。
        """

        params = {"symbol": symbol}
        if order_id:
            params["order_id"] = order_id
        if client_order_id:
            params["client_order_id"] = client_order_id

        request_path = '/api/v1/contract_order_info'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 获取合约订单明细信息

    def contract_order_detail(self, symbol=None, order_id=None, created_at=None, order_type=None, page_index=None,
                              page_size=None):
        """
        参数名称     是否必须  类型    描述
        symbol      true	    string "BTC","ETH"...
        order_id    true	    long	   订单id
        page_index  false   int    第几页,不填第一页
        page_size   false   int    不填默认20，不得多于50
        """

        params = {"symbol": symbol,
                  "order_id": order_id}
        if page_index:
            params["page_index"] = page_index
        if page_size:
            params["page_size"] = page_size
        if created_at:
            params['created_at'] = created_at
        if order_type:
            params['order_type'] = order_type

        request_path = '/api/v1/contract_order_detail'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 获取合约当前未成交委托
    def contract_openorders(self, symbol=None, sort_by=None, trade_type=None, page_index=None, page_size=None):
        """
        参数名称     是否必须  类型   描述
        symbol      false   string "BTC","ETH"...
        page_index  false   int    第几页,不填第一页
        page_size   false   int    不填默认20，不得多于50
        """

        params = {}
        if symbol:
            params["symbol"] = symbol
        if sort_by:
            params["sort_by"] = sort_by
        if trade_type:
            params['trade_type'] = trade_type
        if page_index:
            params["page_index"] = page_index
        if page_size:
            params["page_size"] = page_size

        request_path = '/api/v1/contract_openorders'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 获取合约历史委托
    def contract_hisorders(self, symbol=None, trade_type=None, type=None, status=None, create_date=None, sort_by=None,
                           page_index=None, page_size=None):
        """
        参数名称     是否必须  类型     描述	    取值范围
        symbol      true	    string  品种代码  "BTC","ETH"...
        trade_type  true	    int     交易类型  0:全部,1:买入开多,2: 卖出开空,3: 买入平空,4: 卖出平多,5: 卖出强平,6: 买入强平,7:交割平多,8: 交割平空
        type        true	    int     类型     1:所有订单、2：结束汏订单
        status      true	    int     订单状态  0:全部,3:未成交, 4: 部分成交,5: 部分成交已撤单,6: 全部成交,7:已撤单
        create_date true	    int     日期     7，90（7天或者90天）
        page_index  false   int     页码，不填默认第1页
        page_size   false   int     不填默认20，不得多于50
        """

        params = {"symbol": symbol,
                  "trade_type": trade_type,
                  "type": type,
                  "status": status,
                  "create_date": create_date}
        if sort_by:
            params["sort_by"] = sort_by
        if page_index:
            params["page_index"] = page_index
        if page_size:
            params["page_size"] = page_size

        request_path = '/api/v1/contract_hisorders'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # API划转
    def transfer(self, currency=None, amount=None, type=None):
        """
        参数名称     是否必须      类型     描述	    取值范围
        currency    true	    string  品种代码  "BTC","ETH"...
        amount      true	    int     交易类型  金额
        type        true	    int     类型     可选值：futures-to-pro、pro-to-futures
        """

        params = {"currency": currency,
                  "amount": amount,
                  "type": type}

        request_path = '/v1/futures/transfer'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 获取预估交割价
    def contract_delivery_price(self, symbol=None):
        """
        参数名称     是否必须      类型     描述	    取值范围
        symbol      true	    string  品种代码  "BTC","ETH"...
        """

        params = {"symbol": symbol}

        url = url = self.__url + '/api/v1/contract_delivery_price'
        return api_http_get(url, params)

    # 获取获取资金流水
    def contract_financial_record(self, symbol=None, type=None, create_date=None, page_index=None, page_size=None):
        """
        参数名称     是否必须      类型     描述	    取值范围
        symbol      true	    string  品种代码  "BTC","ETH"...
        """

        params = {"symbol": symbol}
        if type:
            params["type"] = type
        if create_date:
            params["create_date"] = create_date
        if page_index:
            params["page_index"] = page_index
        if page_size:
            params["page_size"] = page_size

        request_path = '/api/v1/contract_financial_record'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 获取历史成交记录
    def contract_matchresults(self, symbol=None, trade_type=None, create_date=None, contract_code=None, page_index=None,
                              page_size=None):
        """
        参数名称     是否必须      类型     描述	    取值范围
        symbol      true	    string  品种代码  "BTC","ETH"...
        """

        params = {"symbol": symbol,
                  "trade_type": trade_type,
                  "create_date": create_date}
        if contract_code:
            params["contract_code"] = contract_code
        if page_index:
            params["page_index"] = page_index
        if page_size:
            params["page_size"] = page_size

        request_path = '/api/v1/contract_matchresults'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 查询合约风险准备金余额历史数据
    def contract_insurance_fund(self, symbol=None):
        """
        :param symbol:
        :return:
        """

        params = {'symbol': symbol}

        request_path = '/api/v1/contract_insurance_fund'
        return api_key_get(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 查询平台阶梯调整系数
    def contract_adjustfactor(self, symbol=None):
        """
        :param symbol:
        :return:
        """

        params = {}

        if symbol:
            params['symbol'] = symbol

        request_path = '/api/v1/contract_adjustfactor'
        return api_key_get(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 平台持仓量的查询
    def contract_his_open_interest(self, symbol=None, contract_type=None, period=None, amount_type=None, size=None):
        """

        :param symbol:
        :param contract_type:
        :param period:
        :param amount_type:
        :param size:
        :return:
        """
        params = {'symbol': symbol,
                  'period': period,
                  'contract_type': contract_type,
                  'amount_type': amount_type}

        if size:
            params['size'] = size

        request_path = '/api/v1/contract_his_open_interest'
        return api_key_get(self.__url, request_path, params, self.__access_key, self.__secret_key)

    #  精英账户多空持仓对比-账户数
    def contract_elite_account_ratio(self, symbol=None, period=None):
        """

        :param symbol:
        :param period:
        :return:
        """

        params = {'symbol': symbol,
                  'period': period}

        request_path = '/api/v1/contract_elite_account_ratio'
        return api_key_get(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 精英账户多空持仓对比-持仓量
    def contract_elite_position_ratio(self, symbol=None, period=None):
        """

        :param symbol:
        :param period:
        :return:
        """

        params = {'symbol': symbol,
                  'period': period}

        request_path = '/api/v1/contract_elite_position_ratio'
        return api_key_get(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 获取强平订单
    def contract_liquidation_orders(self, symbol=None, trade_type=None, create_date=None, page_index=None,
                                    page_size=None):
        """

        :param symbol:
        :param trade_type:
        :param create_date:
        :param page_index:
        :param page_size:
        :return:
        """

        params = {'symbol': symbol,
                  'trade_type': trade_type,
                  'create_date': create_date}

        if page_index:
            params['page_index'] = page_index
        if page_size:
            params['page_size'] = page_size

        request_path = '/api/v1/contract_liquidation_orders'
        return api_key_get(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 获取平台阶梯保证金
    def contract_ladder_margin(self, symbol=None):
        params = {}

        if symbol:
            params['symbol'] = symbol

        request_path = '/api/v1/contract_ladder_margin'
        return api_key_get(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 指数k线
    def contract_history_index(self, symbol=None, period=None, size=None):
        params = {'symbol': symbol,
                  'period': period,
                  'size': size}

        url = self.__url + '/index/market/history/index'
        return api_http_get(url, params)

    # 获取基差数据
    def contract_basis(self, symbol=None, period=None, size=None, basis_price_type=None):
        params = {'symbol': symbol,
                  'period': period,
                  'size': size}
        if basis_price_type:
            params['basis_price_type'] = basis_price_type
        url = self.__url + '/index/market/history/basis'
        return api_http_get(url, params)

    # 查询母账户下所有子账户资产信息
    def contract_sub_account_list(self, symbol=None):
        """
        :param symbol:
        :return:
        """

        params = {}

        if symbol:
            params['symbol'] = symbol

        request_path = '/api/v1/contract_sub_account_list'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 查询单个子账户资产信息
    def contract_sub_account_info(self, symbol=None, sub_uid=None):
        """
        :param symbol:
        :return:
        """

        params = {'sub_uid': sub_uid}

        if symbol:
            params['symbol'] = symbol

        request_path = '/api/v1/contract_sub_account_info'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 查询单个子账户持仓信息
    def contract_sub_position_info(self, symbol=None, sub_uid=None):
        """
        :param symbol:
        :return:
        """

        params = {'sub_uid': sub_uid}

        if symbol:
            params['symbol'] = symbol

        request_path = '/api/v1/contract_sub_position_info'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 查询用户当前的划转限制
    def contract_transfer_limit(self, symbol=None):
        """
        :param symbol:
        :return:
        """

        params = {}

        if symbol:
            params['symbol'] = symbol

        request_path = '/api/v1/contract_transfer_limit'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 用户持仓量限制的查询
    def contract_position_limit(self, symbol=None):
        """
        :param symbol:
        :return:
        """

        params = {}

        if symbol:
            params['symbol'] = symbol

        request_path = '/api/v1/contract_position_limit'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 查询用户账户和持仓信息
    def contract_account_position_info(self, symbol=None):
        params = {}

        if symbol:
            params['symbol'] = symbol

        request_path = '/api/v1/contract_account_position_info'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 母子账户划转
    def contract_master_sub_transfer(self, sub_uid=None, symbol=None, amount=None, type=None, client_order_id=None):

        params = {}
        if sub_uid:
            params['sub_uid'] = sub_uid
        if symbol:
            params['symbol'] = symbol
        if amount:
            params['amount'] = amount
        if type:
            params['type'] = type
        if client_order_id:
            params['client_order_id'] = client_order_id

        request_path = '/api/v1/contract_master_sub_transfer'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 查询母账户下的所有母子账户的划转记录
    def contract_master_sub_transfer_record(self, symbol=None, create_date=None, transfer_type=None, page_index=None,
                                            page_size=None):

        params = {'symbol': symbol,
                  'create_date': create_date}
        if transfer_type:
            params['transfer_type'] = transfer_type
        if page_index:
            params['page_index'] = page_index
        if page_size:
            params['page_size'] = page_size

        request_path = '/api/v1/contract_master_sub_transfer_record'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 获取用户的API指标禁用信息
    def contract_api_trading_status(self):
        params = {}

        request_path = '/api/v1/contract_api_trading_status'
        return api_key_get(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 查询用户品种可用杠杆倍数
    def contract_available_level_rate(self, symbol=None):
        params = {}

        if symbol:
            params['symbol'] = symbol

        request_path = '/api/v1/contract_available_level_rate'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 查询用户当前的手续费费率
    def contract_fee(self, symbol=None):
        """

        :param symbol:
        :return:
        """

        params = {}

        if symbol:
            params['symbol'] = symbol

        request_path = '/api/v1/contract_fee'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 获取用户下单限制
    def contract_order_limit(self, symbol=None, order_price_type=None):
        """
        :param symbol: 可选值：{ BTC_CW, BTC_NW, BTC_CQ, etc. }, order_price_type: limit,post_only....
        :return:
        """
        params = {'order_price_type': order_price_type}
        if symbol:
            params['symbol'] = symbol

        request_path = '/api/v1/contract_order_limit'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 闪电平仓
    def lightning_close_position(self, symbol=None, contract_type=None, contract_code=None, client_order_id=None,
                                 volume=1, direction=None, order_price_type=None, channel_code=None):
        params = {'volume': volume,
                  'direction': direction}
        if symbol:
            params["symbol"] = symbol
        if contract_type:
            params['contract_type'] = contract_type
        if contract_code:
            params['contract_code'] = contract_code
        if client_order_id:
            params['client_order_id'] = client_order_id
        if order_price_type:
            params['order_price_type'] = order_price_type
        if channel_code:
            params['channel_code'] = channel_code

        request_path = '/api/v1/lightning_close_position'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

        # 计划委托下单

    def contract_trigger_order(self, symbol=None, contract_type=None, contract_code=None, trigger_type=None,
                               trigger_price=None,
                               order_price=None, order_price_type=None, volume=None, direction=None, offset=None,
                               lever_rate=None):
        """
        参数名称              是否必须   类型     描述	    取值范围
        symbol	             false	String	品种代码	"BTC","ETH"...
        contract_type        false	String	合约类型	“this_week”:当周，“next_week”:次周，“quarter”:季度
        contract_code	     false	String	合约代码	BTC190903
        trigger_type         true	String	触发类型： ge大于等于(触发价比最新价大)；le小于(触发价比最新价小)
        trigger_price	     true	Number	触发价，精度超过最小变动单位会报错
        order_price	         false	Number	委托价，精度超过最小变动单位会报错
        order_price_type	 false	String	委托类型： 不填默认为limit; 限价：limit ，最优5档：optimal_5，最优10档：optimal_10，最优20档：optimal_20
        volume	             true	Number	委托数量(张)
        direction          	 true	String	buy:买 sell:卖
        offset	             true	String	open:开 close:平
        lever_rate         	 false	Number	开仓必须填写，平仓可以不填。杠杆倍数[开仓若有10倍多单，就不能再下20倍多单]
        """

        params = {'trigger_type': trigger_type,
                  'trigger_price': trigger_price,
                  'volume': volume,
                  'direction': direction,
                  'offset': offset}

        if symbol:
            params['symbol'] = symbol
        if contract_type:
            params['contract_type'] = contract_type
        if contract_code:
            params['contract_code'] = contract_code
        if order_price:
            params['order_price'] = order_price
        if order_price_type:
            params['order_price_type'] = order_price_type
        if lever_rate:
            params['lever_rate'] = lever_rate

        request_path = '/api/v1/contract_trigger_order'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

        # 计划委托撤单接口

    def contract_trigger_cancel(self, symbol=None, order_id=None):
        """
        参数名称              是否必须   类型     描述	    取值范围
        symbol	             True    String	品种代码	"BTC","ETH"...
        order_id             True	 String	用户订单ID（多个订单ID中间以","分隔,一次最多允许撤消20个订单 ）
        """

        params = {'symbol': symbol,
                  'order_id': order_id}

        request_path = '/api/v1/contract_trigger_cancel'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

        # 计划委托全部撤单接口

    def contract_trigger_cancelall(self, symbol=None, contract_code=None, contract_type=None, direction=None,
                                   offset=None):
        """
        参数名称              是否必须   类型     描述	    取值范围
        symbol	             True    String	品种代码	"BTC","ETH"...
        contract_code	     false   String	合约代码,"BTC180914" ...
        contract_type	     false   String	合约类型 当周:"this_week", 周:"next_week", 季度:"quarter"
        """

        params = {'symbol': symbol}

        if contract_code:
            params['contract_code'] = contract_code
        if contract_type:
            params['contract_type'] = contract_type
        if direction:
            params['direction'] = direction
        if offset:
            params['offset'] = offset

        request_path = '/api/v1/contract_trigger_cancelall'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

        # 获取计划委托当前委托接口

    def contract_trigger_openorders(self, symbol=None, contract_code=None, trade_type=None, page_index=None,
                                    page_size=None):
        """
        参数名称              是否必须   类型     描述	    取值范围
        symbol	             True    String	品种代码	"BTC","ETH"...
        contract_code	     false   String	合约代码,"BTC180914" ...
        page_index           false   Number 第几页，不填默认第一页
        page_size            false   Number 不填默认20，不得多于50
        """

        params = {'symbol': symbol}

        if contract_code:
            params['contract_code'] = contract_code
        if trade_type:
            params['trade_type'] = trade_type
        if page_index:
            params['page_index'] = page_index
        if page_size:
            params['page_size'] = page_size

        request_path = '/api/v1/contract_trigger_openorders'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

        # 获取计划委托历史委托接口

    def contract_trigger_hisorders(self, symbol=None, contract_code=None, trade_type=None, status=None,
                                   create_date=None, sort_by=None,
                                   page_index=None, page_size=None):
        """
        参数名称              是否必须   类型     描述	    取值范围
        symbol	             True    String	品种代码	"BTC","ETH"...
        contract_code	     false   String	合约代码,"BTC180914" ...
        trade_type	         true	 number	交易类型		0:全部,1:买入开多,2: 卖出开空,3: 买入平空,4: 卖出平多；后台是根据该值转换为offset和direction，然后去查询的； 其他值无法查询出结果
        status	             true	 String	订单状态		多个以英文逗号隔开，计划委托单状态：0:全部（表示全部结束状态的订单）、4:已委托、5:委托失败、6:已撤单
        create_date        	 true	 number	日期		可随意输入正整数，如果参数超过90则默认查询90天的数据
        page_index           false   int    第几页，不填默认第一页
        page_size            false   int    不填默认20，不得多于50
        """

        params = {'symbol': symbol,
                  'trade_type': trade_type,
                  'status': status,
                  'create_date': create_date}
        if sort_by:
            params['sort_by'] = sort_by
        if contract_code:
            params['contract_code'] = contract_code
        if page_index:
            params['page_index'] = page_index
        if page_size:
            params['page_size'] = page_size

        request_path = '/api/v1/contract_trigger_hisorders'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 组合查询合约历史委托
    def contract_hisorders_exact(self, symbol=None, trade_type=None, type=None, status=None, contract_code=None,
                                 order_type=None, start_time=None, end_time=None, from_id=None, size=None, direct=None):

        params = {'symbol': symbol,
                  'trade_type': trade_type,
                  'status': status}
        if symbol:
            params['symbol'] = symbol
        if trade_type:
            params['trade_type'] = trade_type
        if type:
            params['type'] = type
        if status:
            params['status'] = status
        if contract_code:
            params['contract_code'] = contract_code
        if order_type:
            params['order_type'] = order_type
        if start_time:
            params['start_time'] = start_time
        if end_time:
            params['end_time'] = end_time
        if from_id:
            params['from_id'] = from_id
        if size:
            params['size'] = size
        if direct:
            params['direct'] = direct
        request_path = '/api/v1/contract_hisorders_exact'
        pprint(params)
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 组合查询用户财务记录
    def contract_financial_record_exact(self, symbol=None, type=None, start_time=None, end_time=None, from_id=None,
                                        size=None, direct=None):
        params = {}
        if symbol:
            params['symbol'] = symbol
        if type:
            params['type'] = type
        if start_time:
            params['start_time'] = start_time
        if end_time:
            params['end_time'] = end_time
        if from_id:
            params['from_id'] = from_id
        if size:
            params['size'] = size
        if direct:
            params['direct'] = direct
        request_path = '/api/v1/contract_financial_record_exact'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 查询用户结算记录
    def contract_user_settlement_records(self, symbol=None, start_time=None, end_time=None, page_index=None,
                                         page_size=None):
        params = {}
        if symbol:
            params['symbol'] = symbol
        if start_time:
            params['start_time'] = start_time
        if end_time:
            params['end_time'] = end_time
        if page_index:
            params['page_index'] = page_index
        if page_size:
            params['page_size'] = page_size
        request_path = '/api/v1/contract_user_settlement_records'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    def contract_matchresults_exact(self, symbol=None, trade_type=None, contract_code=None, start_time=None,
                                    end_time=None, from_id=None, size=None, direct=None):
        params = {'symbol': symbol,
                  'trade_type': trade_type}
        if symbol:
            params['symbol'] = symbol
        if trade_type:
            params['trade_type'] = trade_type
        if contract_code:
            params['contract_code'] = contract_code
        if start_time:
            params['start_time'] = start_time
        if end_time:
            params['end_time'] = end_time
        if from_id:
            params['from_id'] = from_id
        if size:
            params['size'] = size
        if direct:
            params['direct'] = direct
        request_path = '/api/v1/contract_matchresults_exact'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 平台结算记录接口
    def contract_settlement_records(self, symbol=None, start_time=None, end_time=None, page_index=None, page_size=None):
        params = {'symbol': symbol}

        if start_time:
            params['start_time'] = start_time
        if end_time:
            params['end_time'] = end_time
        if page_index:
            params['page_index'] = page_index
        if page_size:
            params['page_size'] = page_size

        url = self.__url + '/api/v1/contract_settlement_records'
        return api_http_get(url, params)

    # 获取预估结算价
    def contract_estimated_settlement_price(self, symbol=None):
        params = {}

        if symbol:
            params['symbol'] = symbol

        url = self.__url + '/api/v1/contract_estimated_settlement_price'
        return api_http_get(url, params)

    # 切换杠杆倍数
    def contract_switch_lever_rate(self, symbol=None, lever_rate=None):
        params = {}

        if symbol:
            params['symbol'] = symbol
        if lever_rate:
            params['lever_rate'] = lever_rate

        request_path = '/api/v1/contract_switch_lever_rate'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 对仓位设置止盈止损订单
    def contract_tpsl_order(self, symbol=None, contract_type=None, contract_code=None, direction=None, volume=None,
                            tp_trigger_price=None, tp_order_price=None, tp_order_price_type=None,
                            sl_trigger_price=None, sl_order_price=None, sl_order_price_type=None):

        params = {}
        if symbol:
            params["symbol"] = symbol
        if contract_type:
            params['contract_type'] = contract_type
        if contract_code:
            params['contract_code'] = contract_code
        if direction:
            params['direction'] = direction
        if volume:
            params['volume'] = volume
        if tp_trigger_price:
            params['tp_trigger_price'] = tp_trigger_price
        if tp_order_price:
            params['tp_order_price'] = tp_order_price
        if tp_order_price_type:
            params['tp_order_price_type'] = tp_order_price_type
        if sl_trigger_price:
            params['sl_trigger_price'] = sl_trigger_price
        if sl_order_price:
            params['sl_order_price'] = sl_order_price
        if sl_order_price_type:
            params['sl_order_price_type'] = sl_order_price_type

        request_path = '/api/v1/contract_tpsl_order'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 止盈止损订单撤单接口
    def contract_tpsl_cancel(self, symbol=None, order_id=None):
        params = {}

        if symbol:
            params["symbol"] = symbol
        if order_id:
            params['order_id'] = order_id

        request_path = '/api/v1/contract_tpsl_cancel'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 止盈止损订单全部撤单接口
    def contract_tpsl_cancelall(self, symbol=None, contract_code=None, contract_type=None, direction=None):

        params = {}

        if symbol:
            params["symbol"] = symbol
        if contract_code:
            params['contract_code'] = contract_code
        if contract_type:
            params['contract_type'] = contract_type
        if direction:
            params['direction'] = direction

        request_path = '/api/v1/contract_tpsl_cancelall'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 查询止盈止损订单当前委托接口
    def contract_tpsl_openorders(self, symbol=None, contract_code=None, trade_type=None, page_index=None,
                                 page_size=None):

        params = {}

        if symbol:
            params["symbol"] = symbol
        if contract_code:
            params['contract_code'] = contract_code
        if trade_type:
            params['trade_type'] = trade_type
        if page_index:
            params['page_index'] = page_index
        if page_size:
            params['page_size'] = page_size

        request_path = '/api/v1/contract_tpsl_openorders'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 查询止盈止损订单历史委托接口
    def contract_tpsl_hisorders(self, symbol=None, contract_code=None, status=None, create_date=None, page_index=None,
                                page_size=None, sort_by=None):

        params = {"symbol": symbol, "status": status,
                  "create_date": create_date}

        if symbol:
            params["symbol"] = symbol
        if contract_code:
            params['contract_code'] = contract_code
        if status:
            params['status'] = status
        if create_date:
            params['create_date'] = create_date
        if sort_by:
            params['sort_by'] = sort_by
        if page_index:
            params['page_index'] = page_index
        if page_size:
            params['page_size'] = page_size

        request_path = '/api/v1/contract_tpsl_hisorders'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 查询开仓单关联的止盈止损订单详情接口
    def contract_relation_tpsl_order(self, symbol=None, order_id=None):

        params = {}

        if symbol:
            params["symbol"] = symbol
        if order_id:
            params['order_id'] = order_id

        request_path = '/api/v1/contract_relation_tpsl_order'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 跟踪委托订单下单接口
    def contract_track_order(self, symbol=None, contract_type=None, contract_code=None, direction=None, offset=None,
                             lever_rate=None, volume=None, callback_rate=None, active_price=None,
                             order_price_type=None):

        params = {}

        if symbol:
            params['symbol'] = symbol
        if contract_type:
            params['contract_type'] = contract_type
        if contract_code:
            params['contract_code'] = contract_code
        if direction:
            params['direction'] = direction
        if offset:
            params['offset'] = offset
        if lever_rate:
            params['lever_rate'] = lever_rate
        if volume:
            params['volume'] = volume
        if callback_rate:
            params['callback_rate'] = callback_rate
        if active_price:
            params['active_price'] = active_price
        if order_price_type:
            params['order_price_type'] = order_price_type

        request_path = '/api/v1/contract_track_order'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 跟踪委托订单撤单接口
    def contract_track_cancel(self, symbol=None, order_id=None):

        params = {}
        if symbol:
            params['symbol'] = symbol
        if order_id:
            params['order_id'] = order_id

        request_path = '/api/v1/contract_track_cancel'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 跟踪委托订单全部撤单接口
    def contract_track_cancelall(self, symbol=None, contract_code=None, contract_type=None, direction=None,
                                 offset=None):

        params = {}
        if symbol:
            params['symbol'] = symbol
        if contract_code:
            params['contract_code'] = contract_code
        if contract_type:
            params['contract_type'] = contract_type
        if direction:
            params['direction'] = direction
        if offset:
            params['offset'] = offset

        request_path = '/api/v1/contract_track_cancelall'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 查询跟踪委托订单当前委托接口
    def contract_track_openorders(self, symbol=None, contract_code=None, trade_type=None, page_index=None,
                                  page_size=None):

        params = {}
        if symbol:
            params['symbol'] = symbol
        if contract_code:
            params['contract_code'] = contract_code
        if trade_type:
            params['trade_type'] = trade_type
        if page_index:
            params['page_index'] = page_index
        if page_size:
            params['page_size'] = page_size

        request_path = '/api/v1/contract_track_openorders'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 查询跟踪委托订单历史委托接口
    def contract_track_hisorders(self, symbol=None, contract_code=None, status=None, trade_type=None, create_date=None,
                                 page_index=None, page_size=None, sort_by=None):

        params = {"symbol": symbol, "status": status, "trade_type": trade_type}
        if symbol:
            params['symbol'] = symbol
        if contract_code:
            params['contract_code'] = contract_code
        if status:
            params['status'] = status
        if trade_type:
            params['trade_type'] = trade_type
        if create_date:
            params['create_date'] = create_date
        if page_index:
            params['page_index'] = page_index
        if page_size:
            params['page_size'] = page_size
        if sort_by:
            params['sort_by'] = sort_by

        request_path = '/api/v1/contract_track_hisorders'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 自买自卖调节最新价
    def contract_control_price(self, symbol='', price=None, contract_type=None, lever_rate='5'):
        if not symbol:
            symbol = conf.DEFAULT_SYMBOL
        self.contract_order(symbol=symbol, contract_type=contract_type, price=price, volume='1', direction='buy',
                            offset='open', lever_rate=lever_rate, order_price_type='limit')
        time.sleep(0.5)
        self.contract_order(symbol=symbol, contract_type=contract_type, price=price, volume='1', direction='sell',
                            offset='open', lever_rate=lever_rate, order_price_type='limit')
        time.sleep(2)
        self.contract_order(symbol=symbol, contract_type=contract_type, price=price, volume='1', direction='buy',
                            offset='close', lever_rate=lever_rate, order_price_type='limit')
        time.sleep(0.5)
        self.contract_order(symbol=symbol, contract_type=contract_type, price=price, volume='1', direction='sell',
                            offset='close', lever_rate=lever_rate, order_price_type='limit')

    # 清空当前持仓
    def contract_empty_position(self, symbol='', price=None):  # 恢复环境时用

        r = self.contract_position_info(symbol=symbol)
        count = len(r["data"])

        if count == 0:
            print("当前没有持仓，无需清空")
            return True
        elif count == 1:
            print("当前只持仓一种单，无法通过自我成交清空，请人工处理")
            return False
        elif count == 2:
            volume1 = str(int(r["data"][0]['volume']))
            volume2 = str(int(r["data"][1]['volume']))
            contracttype1 = r["data"][0]['contract_type']
            contracttype2 = r["data"][1]['contract_type']
            leverrate = r["data"][0]['lever_rate']

            if volume1 == volume2 and contracttype1 == contracttype2:
                self.contract_order(symbol=symbol, contract_type=contracttype1, price=price, volume=str(volume1),
                                    direction='buy', offset='close', lever_rate=leverrate, order_price_type='limit')
                time.sleep(0.5)
                self.contract_order(symbol=symbol, contract_type=contracttype1, price=price, volume=str(volume1),
                                    direction='sell', offset='close', lever_rate=leverrate, order_price_type='limit')

                r = self.contract_position_info(symbol=symbol)
                count = len(r["data"])
                if count == 0:
                    print("清除持仓成功")
                    return True
                else:
                    print("清除持仓失败")
                    return False
            else:
                print("当前持仓量不匹配，无法通过自我成交清空，请人工处理")
                return False
        else:
            print("当前持仓状况复杂，无法通过自我成交清空，请人工处理")
            return False

    def contract_market_over_view(self):
        request_path = '/market/overview'
        return api_http_get(self.__url + request_path, {})

    def contract_get_datacode(self, symbol=None):
        contract_type_dict = {}
        contract_infos = self.contract_contract_info(symbol=symbol)
        for contrace_info in contract_infos['data']:
            contract_code = contrace_info.get("contract_code")
            contract_type = contrace_info.get("contract_type")
            contract_type_dict[contract_type] = contract_code
        return contract_type_dict


# 定义t并传入公私钥和URL,供用例直接调用
t = ContractServiceAPI(URL, ACCESS_KEY, SECRET_KEY)
common_user_contract_service_api = ContractServiceAPI(URL, COMMON_ACCESS_KEY, COMMON_SECRET_KEY)
atp_contract_service_api = ContractServiceAPI(URL, ATP_SERVER_ACCESS_KEY, ATP_SERVER_SECRET_KEY)
userList = eval(USERINFO)
user01 = ContractServiceAPI(
    URL, userList[0]['ACCESS_KEY'], userList[0]['SECRET_KEY'])
user02 = ContractServiceAPI(
    URL, userList[1]['ACCESS_KEY'], userList[1]['SECRET_KEY'])
user03 = ContractServiceAPI(
    URL, userList[2]['ACCESS_KEY'], userList[2]['SECRET_KEY'])
