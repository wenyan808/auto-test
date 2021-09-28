#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/9/14
# @Author  : lss
# @link : p0.交割


from common.ContractServiceAPI import t as contranct_api
from common.ContractServiceOrder import t as contranct_order
from common.util import compare_dict

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
class TestContractLimitOrder_006:

    def setUp(self):
        print('\n前置条件')

    @allure.title('{title}')
    def test_contract_limit_order(self, symbol, symbol_period):
        """ IOC卖出开空下单后自动撤单测试 """
        lever_rate = 5

        self.setUp()
        print('\n步骤一:获取盘口买一价\n')
        r_trend_req = contranct_api.contract_depth(symbol="LTC_CW", type="step5")
        pprint(r_trend_req)
        data_r_trade_res = r_trend_req.get("tick").get("bids")
        assert len(data_r_trade_res) > 0, "盘口(买入盘)无数据"
        highest_price_buy = max([i[0] for i in data_r_trade_res])
        print('\n步骤二:下一个高于买一价的卖单\n')
        order_price_type = "ioc"
        higher_price = round((highest_price_buy * 1.1), 1)
        r_order_sell = contranct_api.contract_order(symbol=symbol, contract_type='this_week', price=higher_price, volume='1',
                                                    direction='sell', offset='open', lever_rate=lever_rate,
                                                    order_price_type=order_price_type)
        pprint(r_order_sell)
        current_time = int(str(time.time()).split(".")[0])
        time.sleep(5)
        generated_order_id = r_order_sell['data']['order_id']
        history_orders = contranct_api.contract_hisorders(symbol=symbol, trade_type=0, type=1, status=0, create_date=7)
        all_orders = history_orders.get("data").get("orders")
        all_order_ids = [i.get("order_id") for i in all_orders]
        for order in all_orders:
            current_order_id = order.get("order_id")
            if current_order_id == generated_order_id:
                expected_info_dic = {"status": 7, "lever_rate": 5, "order_type": 1, "volume": 1, "price": higher_price}
                actual_time_from_query = int(str(order.get("create_date"))[0:10])
                assert (actual_time_from_query - current_time) <= 180, "时间不一致, 限价单%d创建时间: %s, 查询到的时间: %s" % (generated_order_id, current_time, actual_time_from_query)
                assert compare_dict(expected_info_dic, order)
                return
        raise BaseException("在{all_order_ids}中未找到历史订单含有订单号: {generated_order_id}".format(all_order_ids=all_order_ids, generated_order_id=generated_order_id))


if __name__ == '__main__':
    pytest.main()
