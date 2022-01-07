#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : lss
import datetime

import common.util
from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.ContractServiceAPI import ContractServiceAPI
from config.conf import *
from schema import Schema, And, Or, Regex, SchemaError
from pprint import pprint
import pytest
import allure
import random
import time
from tool.get_test_data import case_data
from tool.atp import ATP


@allure.epic('反向交割')
@allure.feature('功能')
@pytest.mark.stable
class TestContractTriggerOrder_0011:

    def setup(self):
        self.symbol = None
        self.new_order_id = None
        print(''' cancel all types orders ''')
        ATP.cancel_all_types_order()
        time.sleep(1)
        ATP.clean_market()
        self.current_price = ATP.get_current_price()
        ATP.current_user_make_order(direction='buy')
        ATP.current_user_make_order(direction='sell')
        time.sleep(1)

    @allure.title("触发计划委托订单平仓测试")
    def test_contract_account_position_info(self, symbol, symbol_period):
        """ 触发计划委托订单平仓测试 """
        self.symbol = symbol
        current_user = ContractServiceAPI(
            url=URL, access_key=ACCESS_KEY, secret_key=SECRET_KEY)
        common_user = ContractServiceAPI(
            url=URL, access_key=COMMON_ACCESS_KEY, secret_key=COMMON_SECRET_KEY)
        #     获取最新价
        r_contract_trade = current_user.contract_trade(symbol=symbol_period)
        data_r_tract_trade = r_contract_trade.get("tick").get("data")
        last_price = float(data_r_tract_trade[0].get("price"))
        pprint("\n前置： 获取合约code\n")
        contract_ltc_info = current_user.contract_contract_info(
            symbol=symbol).get("data")
        print("查询当前限价委托单")
        r = current_user.contract_openorders(symbol=symbol, trade_type=0)
        pprint(r)
        res_before_limit_created_orders = r.get("data").get("orders")

        pprint("\n步骤一: 平仓-计划委托单\n")
        contract_type = "this_week"
        contract_code = [i.get("contract_code") for i in contract_ltc_info if i.get(
            "contract_type") == contract_type][0]
        direction = "buy"
        volume = 10

        trigger_price = last_price
        order_price = round(last_price * 1.01, 1)
        trigger_type = "ge"
        offset = "close"
        lever_rate = 5
        order_price_type = "limit"
        resp_plan_buy = current_user.contract_trigger_order(symbol=symbol, contract_type=contract_type, contract_code=contract_code, trigger_type=trigger_type, trigger_price=trigger_price, order_price=order_price, order_price_type=order_price_type, volume=volume,
                                                            direction=direction, offset=offset, lever_rate=lever_rate)
        assert resp_plan_buy.get(
            "status") == "ok", "下单出错: {res}".format(res=resp_plan_buy)
        order_id = resp_plan_buy['data']['order_id']
        time.sleep(5)
        res_all_his_orders = current_user.contract_trigger_openorders(
            symbol=symbol, contract_code=contract_code).get("data").get("orders")
        order_created = False
        for r in res_all_his_orders:
            if r.get("order_id") == order_id:
                expected_did = {"trigger_type": trigger_type, "volume": volume, "lever_rate": lever_rate, "order_price_type": order_price_type, "trigger_price": trigger_price, "contract_code": contract_code, "symbol": symbol,
                                "contract_type": contract_type, "direction": direction, "offset": offset}
                assert common.util.compare_dict(expected_did, r)
                order_created = True
                break
        if order_created:
            print("步骤二：用另一个账号做一个限价卖->买的成交，使最新价达到触发价")
            resp_limit_sell = common_user.contract_order(symbol=symbol, contract_type=contract_type, contract_code=contract_code,
                                                         price=order_price, volume=1, direction="sell", offset="open", lever_rate=lever_rate, order_price_type=order_price_type)
            assert resp_limit_sell.get(
                "status") == "ok", "下单出错: {res}".format(res=resp_limit_sell)
            resp_limit_buy = common_user.contract_order(symbol=symbol, contract_type=contract_type, contract_code=contract_code,
                                                        price=order_price, volume=1, direction="buy", offset="open", lever_rate=lever_rate, order_price_type=order_price_type)
            assert resp_limit_buy.get(
                "status") == "ok", "下单出错: {res}".format(res=resp_limit_buy)
            after_orders = None
            time_count = 0
            while (not after_orders) and (time_count < 10):
                time.sleep(1)
                res_all_orders = current_user.contract_openorders(
                    symbol=symbol, trade_type=0)
                print(res_all_orders)
                after_orders = res_all_orders.get("data").get("orders")
                time_count += 1
            new_order = [
                i for i in after_orders if i not in res_before_limit_created_orders][0]
            expected_dic = {"symbol": symbol, "order_price_type": order_price_type,
                            "lever_rate": lever_rate, "volume": 10, "price": order_price}
            assert common.util.compare_dict(expected_dic, new_order)
            self.new_order_id = new_order.get("order_id")
            created_time = datetime.datetime.fromtimestamp(
                new_order.get("created_at") / 1000)
            now = datetime.datetime.now()
            assert (now + datetime.timedelta(seconds=180) >= created_time >= now) or (created_time +
                                                                                      datetime.timedelta(seconds=180) >= now >= created_time), "时间过长对不上(时间差超过180s)"
        else:
            raise BaseException("在{res_all_his_orders}中未找到历史订单含有订单号: {order_id}".format(
                res_all_his_orders=res_all_his_orders, order_id=order_id))

    @allure.step("恢复环境")
    def teardown(self):
        ATP.cancel_all_types_order()


if __name__ == '__main__':
    pytest.main()
