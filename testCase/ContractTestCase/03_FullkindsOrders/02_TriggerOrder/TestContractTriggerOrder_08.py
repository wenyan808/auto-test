#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : lss
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

from tool.atp import ATP
from tool.get_test_data import case_data
from tool.atp import ATP


@allure.epic('反向交割')
@allure.feature('功能')
@pytest.mark.stable
class TestContractTriggerOrder_008:

    def setup(self):
        self.available = None
        self.trigger_price = None
        self.order_id = None
        self.symbol = None
        self.symbol = None
        self.new_order_id = None
        print(''' cancel all types orders ''')
        ATP.cancel_all_types_order()
        time.sleep(1)
        self.current_price = ATP.get_current_price()
        print(''' make market depth ''')
        ATP.make_market_depth()
        sell_price = ATP.get_adjust_price(1.02)
        buy_price = ATP.get_adjust_price(0.98)
        ATP.common_user_make_order(price=sell_price, direction='sell')
        ATP.common_user_make_order(price=buy_price, direction='buy')
        time.sleep(2)

    @allure.title('计划止损正常限价')
    def test_contract_account_position_info(self, symbol, symbol_period):
        """ 计划止损正常限价 """
        self.symbol = symbol
        pprint("\n步骤一：查看自己的持仓\n")
        c = ContractServiceAPI(
            url=URL, access_key=COMMON_ACCESS_KEY, secret_key=COMMON_SECRET_KEY)
        contract_ltc_info = c.contract_contract_info(symbol=symbol).get("data")

        contract_type = "this_week"
        contract_code = [i.get("contract_code") for i in contract_ltc_info if i.get(
            "contract_type") == contract_type][0]
        trigger_type = "le"
        pprint("\n步骤二：查看最近成交记录，获取最新价(如果最近无成交，则需要造一笔成交记录)\n")
        r_contract_trade = c.contract_trade(symbol=symbol_period)
        data_r_tract_trade = r_contract_trade.get("tick").get("data")
        volume_at_least = 10
        last_price = None
        order_price_type = "limit"
        direction = "sell"
        offset = "close"
        lever_rate = 5

        def sell_and_buy():
            ATP.current_user_make_order(direction='sell')
            time.sleep(1)
            ATP.current_user_make_order(direction='buy')
            pprint("\n步骤二(3): 等待5s成交\n")
            time.sleep(1)

        if not data_r_tract_trade:
            pprint("\n未找到最新价, 准备进行一次买卖构造一个最新价...\n")
            sell_and_buy()
        else:
            pprint("\n找到最新价，准备获取持仓数据...\n")
            last_price = float(data_r_tract_trade[0].get("price"))
        order_price = round((last_price * 0.98), 1)
        self.trigger_price = order_price

        # 如果有持仓且可平量>=10，直接下计划委托单
        def get_order_id(p_data):
            for each_symbol in p_data:
                if each_symbol.get("symbol") == symbol:
                    # 判断数量
                    positions = each_symbol.get("positions")
                    for p in positions:
                        self.available = int(p.get("available"))
                        if self.available >= 10:
                            pprint("\n可平量大于等于10个\n")
                            pprint("步骤三: 下单(计划委托止损单)")
                            order = c.contract_trigger_order(symbol=symbol, contract_type=contract_type, contract_code=contract_code, trigger_type=trigger_type, trigger_price=self.trigger_price, order_price=order_price, order_price_type=order_price_type, volume=10,
                                                             direction=direction, offset=offset, lever_rate=lever_rate)
                            time.sleep(5)
                            assert order.get(
                                "status") == "ok", "下单出错: {res}".format(res=order)
                            return order['data']['order_id']
                        else:
                            pprint("\n可平量少于10个\n")

                            return None
            return None

        positions_data = c.contract_account_position_info(
            symbol=symbol).get("data")
        # 如果有持仓，就不需要再造持仓了，否则需要去造持仓数据
        if positions_data:
            pprint("\n找到已存在的LTC持仓数据, 判断可平量...\n")
            self.order_id = get_order_id(positions_data)
            if not self.order_id:
                pprint("\n可平量少于10个， 准备构造持仓...\n")
                sell_and_buy()
                positions_data = c.contract_account_position_info(
                    symbol=symbol).get("data")
                order_id = get_order_id(positions_data)
        # 否则，先持仓10张(做一个卖->买)，再下计划委托单
        else:
            sell_and_buy()
            positions_data = c.contract_account_position_info(
                symbol=symbol).get("data")
            self.order_id = get_order_id(positions_data)

        res_all_his_orders = c.contract_trigger_openorders(
            symbol=symbol, contract_code=contract_code).get("data").get("orders")
        for r in res_all_his_orders:
            if r.get("order_id") == self.order_id:
                expected_did = {"trigger_type": trigger_type, "volume": 10, "lever_rate": lever_rate, "order_price_type": order_price_type, "trigger_price": self.trigger_price, "contract_code": contract_code, "symbol": symbol,
                                "contract_type": contract_type, "direction": direction, "offset": offset}
                assert common.util.compare_dict(expected_did, r)
                pprint("\n步骤三: 撤单\n")
                r_cancel = c.contract_cancel(
                    symbol=symbol, order_id=self.order_id)
                assert r_cancel.get("status") == "ok"
                return
        raise BaseException("在{res_all_his_orders}中未找到历史订单含有订单号: {order_id}".format(
            res_all_his_orders=res_all_his_orders, order_id=self.order_id))

    @allure.step("恢复环境")
    def teardown(self):
        r_cancel = contract_api.contract_cancel(
            symbol=self.symbol, order_id=self.order_id)
        assert r_cancel.get("status") == "ok", f"撤单失败: {r_cancel}"
        ATP.cancel_all_trigger_order()


if __name__ == '__main__':
    pytest.main()
