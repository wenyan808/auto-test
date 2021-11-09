#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/9/14
# @Author  : lss
# @link : p0.交割


import allure
import pytest
import time

from common.ContractServiceAPI import t as contract_api, ContractServiceAPI
from common.util import compare_dict
from config.conf import URL, COMMON_ACCESS_KEY, COMMON_SECRET_KEY
from tool.atp import ATP


# tpsl止盈止损
# tracker 跟踪委托
# hisorder 限价委托
@allure.epic('反向交割')
@allure.feature('功能')
@pytest.mark.stable
class TestContractLimitOrder_006:

    def setUp(self):
        print('\n前置条件')
        ATP.make_market_depth()
        time.sleep(1)

    @allure.title('IOC卖出开空下单后自动撤单测试')
    def test_contract_limit_order(self, symbol, symbol_period):
        """ IOC卖出开空下单后自动撤单测试 """
        lever_rate = 5

        self.setUp()
        print('\n步骤一:获取盘口买一价\n')
        r_trend_req = contract_api.contract_depth(
            symbol=symbol_period, type="step5")
        bids = r_trend_req.get("tick").get("bids")
        asks = r_trend_req.get("tick").get("asks")
        # 如果盘口无买一价，则用通用账号挂一个买单,为了防止成交，价格得低于卖一价
        common_user = ContractServiceAPI(
            url=URL, access_key=COMMON_ACCESS_KEY, secret_key=COMMON_SECRET_KEY)
        r_contract_info = contract_api.contract_contract_info(
            symbol=symbol, contract_type="this_week")
        contract_this_week = r_contract_info.get(
            "data")[0].get("contract_code")
        if not bids:
            if not asks:
                price = ATP.get_current_price()
            else:
                price = round(min([i[0] for i in asks]) * 0.9, 1)
            r_common_buy = common_user.contract_order(symbol=symbol, contract_code=contract_this_week, price=price,
                                                      volume=1, direction="buy", offset="open", lever_rate=lever_rate,
                                                      order_price_type="limit")
            assert r_common_buy.get(
                "status") == "ok", f"通用账号下买单失败: {r_common_buy}"
            r_trend_req = contract_api.contract_depth(
                symbol=symbol_period, type="step5")
            bids = r_trend_req.get("tick").get("bids")
        highest_price_buy = max([i[0] for i in bids])
        print('\n步骤二:下一个高于买一价的卖单\n')
        order_price_type = "ioc"
        higher_price = round((highest_price_buy * 1.1), 1)
        r_order_sell = contract_api.contract_order(symbol=symbol, contract_type='this_week', price=higher_price,
                                                   volume='1',
                                                   direction='sell', offset='open', lever_rate=lever_rate,
                                                   order_price_type=order_price_type)
        current_time = int(str(time.time()).split(".")[0])
        time.sleep(5)
        generated_order_id = r_order_sell['data']['order_id']
        history_orders = contract_api.contract_hisorders(
            symbol=symbol, trade_type=0, type=1, status=0, create_date=7)
        all_orders = history_orders.get("data").get("orders")
        all_order_ids = [i.get("order_id") for i in all_orders]
        for order in all_orders:
            current_order_id = order.get("order_id")
            if current_order_id == generated_order_id:
                expected_info_dic = {"status": 7, "lever_rate": 5,
                                     "order_type": 1, "volume": 1, "price": higher_price}
                actual_time_from_query = int(
                    str(order.get("create_date"))[0:10])
                assert (actual_time_from_query - current_time) <= 180, "时间不一致, 限价单%d创建时间: %s, 查询到的时间: %s" % (
                    generated_order_id, current_time, actual_time_from_query)
                assert compare_dict(expected_info_dic, order)
                return
        raise BaseException("在{all_order_ids}中未找到历史订单含有订单号: {generated_order_id}".format(all_order_ids=all_order_ids,
                                                                                         generated_order_id=generated_order_id))

    @allure.step("恢复环境")
    def teardown(self):
        ATP.cancel_all_order()


if __name__ == '__main__':
    pytest.main()
