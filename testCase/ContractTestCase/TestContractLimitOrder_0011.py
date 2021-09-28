#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/9/14
# @Author  : lss
# @link : p0.交割


from common.ContractServiceAPI import t as contract_api
from config.conf import COMMON_ACCESS_KEY, COMMON_SECRET_KEY, URL
from common.ContractServiceOrder import t as contranct_order
from common.util import compare_dict
from common.ContractServiceAPI import ContractServiceAPI
from schema import Schema, And, Or, Regex, SchemaError
from pprint import pprint
import pytest, allure, random, time
from tool.get_test_data import case_data
from datetime import datetime


# tpsl止盈止损
# tracker 跟踪委托
# hisorder 限价委托
@allure.epic('反向交割')
@allure.feature('')
class TestContractLimitOrder_0011:

    def setUp(self):
        print('\n前置条件')

    @allure.title('{title}')
    def test_contract_limit_order(self, symbol, symbol_period):
        """ 最优5档买入开多卖盘无数据自动撤单 """
        lever_rate = 5

        self.setUp()
        pprint('\n步骤一:获取盘口(卖)\n')
        r_trend_req = contract_api.contract_depth(symbol=symbol_period, type="step0")
        pprint(r_trend_req)
        current_asks = r_trend_req.get("tick").get("asks")
        # 如果有卖单，则吃掉所有卖单
        if current_asks:
            total_asks = 0
            highest_price = 0
            for each_ask in current_asks:
                each_price, each_amount = each_ask[0], each_ask[1]
                total_asks += each_amount
                highest_price = max(highest_price, each_price)
            pprint("\n步骤二：用操作账号以当前最高价吃掉(买入)所有卖单\n")
            service = ContractServiceAPI(URL, COMMON_ACCESS_KEY, COMMON_SECRET_KEY)
            service.contract_order(symbol=symbol, contract_type='this_week', price=highest_price, volume=total_asks, direction='buy', offset='open', lever_rate=lever_rate, order_price_type='limit')
            pprint("\n步骤三：再次查询盘口，确认是否已吃掉所有卖单\n")
            r_trend_req_confirm = contract_api.contract_depth(symbol=symbol_period, type="step0")
            current_asks = r_trend_req_confirm.get("tick").get("asks")
            assert not current_asks, "卖盘不为空! 当前卖盘: {current_asks}".format(current_asks=current_asks)
        pprint("\n步骤四: 以最优5档买入开多\n")
        r_buy_opponent = contract_api.contract_order(symbol=symbol, contract_type='this_week', order_price_type='optimal_5', price="", direction="buy", offset="open", lever_rate=lever_rate, volume=1)
        actual_status = r_buy_opponent.get("status")
        actual_msg = r_buy_opponent.get("err_msg")
        assert actual_status == 'error' and actual_msg == "盘口无数据,请稍后再试", "预期: `error`+`盘口无数据,请稍后再试`, 实际: `{actual_status}+{actual_msg}`".format(actual_status=actual_status, actual_msg=actual_msg)


if __name__ == '__main__':
    pytest.main()
