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
import pytest, allure, random, time
from tool.get_test_data import case_data


@allure.epic('反向交割')
@allure.feature('功能')
@pytest.mark.stable
class TestContractTriggerOrder_006:

    def setUp(self):
        self.available = None
        self.trigger_price = None
        self.order_id = None
        self.symbol = None

    @allure.title('计划止盈正常限价')
    def test_contract_account_position_info(self, symbol, symbol_period):
        """ 计划止盈正常限价 """
        self.symbol = symbol
        pprint("\n步骤一：查看自己的持仓\n")
        contract_ltc_info = contract_api.contract_contract_info(symbol=symbol).get("data")
        contract_type = "this_week"
        contract_code = [i.get("contract_code") for i in contract_ltc_info if i.get("contract_type") == contract_type][0]
        trigger_type = "ge"
        pprint("\n步骤二：查看最近成交记录，获取最新价(如果最近无成交，则需要造一笔成交记录)\n")
        r_contract_trade = contract_api.contract_trade(symbol=symbol_period)
        data_r_tract_trade = r_contract_trade.get("tick").get("data")
        volume_at_least = 10
        last_price = None
        order_price_type = "limit"
        direction = "sell"
        offset = "close"
        lever_rate = 5

        def sell_and_buy():
            pprint("\n步骤二(1): 挂一个卖单\n")
            r_temp_buy = contract_api.contract_order(symbol=symbol, contract_type=contract_type, price=100.0, volume=volume_at_least, direction='sell', offset='open', lever_rate=lever_rate, order_price_type="limit")
            assert r_temp_buy.get("status") == "ok"
            pprint("\n步骤二(2): 挂一个买单\n")
            r_temp_buy = contract_api.contract_order(symbol=symbol, contract_type=contract_type, price=100.0, volume=volume_at_least, direction='buy', offset='open', lever_rate=lever_rate, order_price_type="limit")
            assert r_temp_buy.get("status") == "ok"
            pprint("\n步骤二(3): 等待5s成交\n")
            time.sleep(5)

        if not data_r_tract_trade:
            pprint("\n未找到最新价, 准备进行一次买卖制造一个最新价...\n")
            sell_and_buy()
        else:
            pprint("\n找到最新价，准备获取持仓数据...\n")
            last_price = float(data_r_tract_trade[0].get("price"))
        order_price = round((last_price * 1.1), 1)
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
                            pprint("步骤三: 下单(计划委托止盈单)")
                            order = contract_api.contract_trigger_order(symbol=symbol, contract_type=contract_type, contract_code=contract_code, trigger_type=trigger_type, trigger_price=self.trigger_price, order_price=order_price, order_price_type=order_price_type,
                                                                        volume=self.available,
                                                                        direction=direction, offset=offset, lever_rate=lever_rate)
                            time.sleep(5)
                            return order['data']['order_id']
                        else:
                            pprint("\n可平量少于10个\n")
                            return None
            return None

        positions_data = contract_api.contract_account_position_info(symbol=symbol).get("data")
        # 如果有持仓，就不需要再造持仓了，否则需要去造持仓数据
        if positions_data:
            pprint("\n找到已存在的LTC持仓数据, 判断可平量...\n")
            self.order_id = get_order_id(positions_data)
            if not self.order_id:
                pprint("\n可平量少于10个， 准备制造持仓...\n")
                sell_and_buy()
                positions_data = contract_api.contract_account_position_info(symbol=symbol).get("data")
                order_id = get_order_id(positions_data)
        # 否则，先持仓10张(做一个卖->买)，再下计划委托单
        else:
            sell_and_buy()
            positions_data = contract_api.contract_account_position_info(symbol=symbol).get("data")
            self.order_id = get_order_id(positions_data)

        res_all_his_orders = contract_api.contract_trigger_openorders(symbol=symbol, contract_code=contract_code).get("data").get("orders")
        for r in res_all_his_orders:
            if r.get("order_id") == self.order_id:
                expected_did = {"trigger_type": trigger_type, "volume": self.available, "lever_rate": lever_rate, "order_price_type": order_price_type, "trigger_price": self.trigger_price, "contract_code": contract_code, "symbol": symbol,
                                "contract_type": contract_type, "direction": direction, "offset": offset}
                assert common.util.compare_dict(expected_did, r)
                return
        raise BaseException("在{res_all_his_orders}中未找到历史订单含有订单号: {order_id}".format(res_all_his_orders=res_all_his_orders, order_id=self.order_id))

    @allure.step("恢复环境")
    def teardown(self):
        r_cancel = contract_api.contract_cancel(symbol=self.symbol, order_id=self.order_id)
        assert r_cancel.get("status") == "ok", "撤单失败"


if __name__ == '__main__':
    pytest.main()
