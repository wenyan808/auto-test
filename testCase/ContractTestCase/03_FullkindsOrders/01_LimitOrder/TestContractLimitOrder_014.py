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
@allure.feature('功能')
@pytest.mark.stable
class TestContractLimitOrder_0014:

    def setUp(self):
        print('\n前置条件')

    @allure.title('最优10档卖出开空买盘无数据自动撤单')
    def test_contract_limit_order(self, symbol, symbol_period):
        """ 最优10档卖出开空买盘无数据自动撤单 """
        lever_rate = 5

        self.setUp()
        pprint('\n步骤一:获取盘口(买)\n')
        r_trend_req = contract_api.contract_depth(symbol=symbol_period, type="step0")
        pprint(r_trend_req)
        current_bids = r_trend_req.get("tick").get("bids")
        # 如果有买单，则吃掉所有买单;如果没有，则不需要吃盘，直接卖出
        if current_bids:
            total_bids = 0
            lowest_price = []
            for each_bids in current_bids:
                each_price, each_amount = each_bids[0], each_bids[1]
                total_bids += each_amount
                lowest_price.append(each_price)
            lowest_price = min(lowest_price)
            pprint("\n步骤二：用操作账号以当前最低价吃掉所有买单(卖出)\n")
            service = ContractServiceAPI(URL, COMMON_ACCESS_KEY, COMMON_SECRET_KEY)
            service.contract_order(symbol=symbol, contract_type='this_week', price=lowest_price, volume=total_bids, direction='sell', offset='open', lever_rate=lever_rate, order_price_type='limit')
            time.sleep(3)
            pprint("\n步骤三：再次查询盘口，确认是否已吃掉所有买单\n")
            r_trend_req_confirm = contract_api.contract_depth(symbol=symbol_period, type="step0")
            current_bids = r_trend_req_confirm.get("tick").get("bids")
            assert not current_bids, "买盘不为空! 当前买盘: {current_bids}".format(current_bids=current_bids)
        pprint("\n步骤四: 以最优10档卖出做空\n")
        r_sell_opponent = contract_api.contract_order(symbol=symbol, contract_type='this_week', order_price_type='optimal_10', price="", direction="sell", offset="open", lever_rate=lever_rate, volume=1)
        actual_status = r_sell_opponent.get("status")
        actual_msg = r_sell_opponent.get("err_msg")
        assert actual_status == 'error' and actual_msg == "盘口无数据,请稍后再试", "预期: `error`+`盘口无数据,请稍后再试`, 实际: `{actual_status}+{actual_msg}`".format(actual_status=actual_status, actual_msg=actual_msg)


if __name__ == '__main__':
    pytest.main()
