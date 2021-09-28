#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210917
# @Author : lss
用例标题
    持仓区域下止盈止损最优5档
前置条件
    有持仓且大于等于10张
    
步骤/文本
    1、登录交割合约界面
    2、在当前持仓tab选择持仓BTC当周多单，点击止盈止损按钮
    3、选择按价格按钮
    4、输入止盈价，止盈价高于最新价（如：50000）
    5、输入卖出价最优5/10/20档，任意一档
    6、输入卖出量10张
    7、点击确认按钮有结果A
    8、查看当前委托列表中的止盈止损页面有结果B
预期结果
    A)提示下单成功
    B)在当前委托-止盈止损列表查看显示订单A，且数值正确，状态显示等待委托
优先级
    0
用例别名
    TestContractTriggerOrder_020
"""

import common.util
from common.ContractServiceAPI import t as contract_api
from common.ContractServiceAPI import ContractServiceAPI
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest, allure, random, time

from config.conf import URL, LSS_ACCESS_KEY, LSS_SECRET_KEY


@allure.epic('交割')  # 这里填业务线
@allure.feature('止盈止损')  # 这里填功能
@allure.story('持仓区域下止盈止损最优5档')  # 这里填子功能，没有的话就把本行注释掉
class TestContractTriggerOrder_020:

    @allure.step('前置条件')
    def setup(self):
        self.c = ContractServiceAPI(url=URL, access_key=LSS_ACCESS_KEY, secret_key=LSS_SECRET_KEY)
        print(''' 有持仓且大于等于10张''')
        self.contract_type = "this_week"
        symbol, symbol_period = "LTC", "LTC_CW"
        contract_ltc_info = self.c.contract_contract_info(symbol=symbol).get("data")
        self.contract_code = [i.get("contract_code") for i in contract_ltc_info if i.get("contract_type") == self.contract_type][0]
        print("为了使持仓量满足条件, 先进行一次卖->买")
        print("步骤一(0): 获取最新价")
        r_contract_trade = self.c.contract_trade(symbol=symbol_period)
        data_r_tract_trade = r_contract_trade.get("tick").get("data")
        self.last_price = float(data_r_tract_trade[0].get("price"))
        print("步骤一(1): 挂一个卖单")
        r_temp_sell = self.c.contract_order(symbol=symbol, contract_type=self.contract_type, price=self.last_price, volume=10, direction='sell', offset='open', lever_rate=5, order_price_type="limit")
        assert r_temp_sell.get("status") == "ok", ""
        print("步骤一(2): 挂一个买单")
        r_temp_buy = self.c.contract_order(symbol=symbol, contract_type=self.contract_type, price=self.last_price, volume=10, direction='buy', offset='open', lever_rate=5, order_price_type="limit")
        assert r_temp_buy.get("status") == "ok"
        print("步骤一(3): 等待3s成交")
        time.sleep(3)
        positions_data = self.c.contract_account_position_info(symbol=symbol).get("data")
        for each_symbol in positions_data:
            if each_symbol.get("symbol") == symbol:
                # 判断数量
                positions = each_symbol.get("positions")
                for p in positions:
                    available = int(p.get("available"))
                    assert available >= 10, "经过一次卖->买之后，可平量依然不足10"
                    return

    @allure.title('持仓区域下止盈止损正常限价')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):

        with allure.step('1、登录交割合约界面'):
            tp_trigger_price = round(self.last_price * 1.1, 1)
            tp_order_price = round(tp_trigger_price * 1.1, 1)
            tp_order_price_type = "optimal_10"
            res_create_order = self.c.contract_tpsl_order(symbol=symbol, contract_type=self.contract_type, contract_code=self.contract_code, direction="sell", volume=10, tp_trigger_price=tp_trigger_price, tp_order_price=tp_order_price, tp_order_price_type=tp_order_price_type)
            assert res_create_order.get("status") == "ok", "下单失败: {r_contract_order}".format(r_contract_order=res_create_order)
            order_id = res_create_order.get("data").get("tp_order").get("order_id")
        with allure.step('2、在当前持仓tab选择持仓BTC当周多单，点击止盈止损按钮'):
            pass
        with allure.step('3、选择按价格按钮'):
            pass
        with allure.step('4、输入止盈价，止盈价高于最新价（如：50000）'):
            pass
        with allure.step('5、输入卖出价55000'):
            pass
        with allure.step('6、输入卖出量10张'):
            pass
        with allure.step('7、点击确认按钮有结果A'):
            pass

        with allure.step('8、查看当前委托列表中的止盈止损页面有结果B'):
            time.sleep(3)
            r_contract_order_history_data = self.c.contract_tpsl_openorders(symbol=symbol, contract_code=self.contract_code).get("data").get("orders")
            expected_tp_order_info = {"symbol": symbol, "contract_code": self.contract_code, "contract_type": self.contract_type, "volume": 10, "direction": "sell", "trigger_price": tp_trigger_price, "order_price": 0, "status": 2,
                                      "order_price_type": tp_order_price_type}
            for o in r_contract_order_history_data:
                if o.get("order_id") == order_id:
                    assert common.util.compare_dict(expected_tp_order_info, o)
                    with allure.step("撤单"):
                        r_cancel_all = self.c.contract_tpsl_cancelall(symbol=symbol, contract_code=self.contract_code)
                        assert r_cancel_all.get('status') == "ok", "撤单失败"
                        return
            raise BaseException("在当前所有止盈止损单{r_contract_order_history_data}中未找到止盈止损单{order_id}".format(r_contract_order_history_data=r_contract_order_history_data, order_id=order_id))

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
