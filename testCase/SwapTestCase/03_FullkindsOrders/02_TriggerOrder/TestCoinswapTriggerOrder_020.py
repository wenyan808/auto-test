#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210918
# @Author : 邱大伟

#script by: lss
用例编号
    TestCoinswapTriggerOrder_020
所属分组
    计划委托
用例标题
    持仓区域下止盈止损最优5档
前置条件
    有持仓且大于等于10张
    
步骤/文本
    1、登录币本位永续界面
    2、在当前持仓tab选择持仓BTC/USD多单，点击止盈止损按钮
    3、选择按价格按钮
    4、输入止盈价，止盈价高于最新价（如：50000）
    5、输入卖出价最优5/10/20档，任意一档
    6、输入卖出量10张
    7、点击确认按钮有结果A
    8、查看当前委托列表中的止盈止损页面有结果B
预期结果
    A)提示下单成功
    B)在当前委托-止盈止损列表查看显示订单A，且数值正确，状态显示等待委托
用例作者
    邱大伟
自动化作者
    刘双双
"""

from decimal import Decimal

import common.util
from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api, SwapService
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest, allure, random, time

from config.conf import URL, SECRET_KEY, ACCESS_KEY, COMMON_ACCESS_KEY, COMMON_SECRET_KEY


@allure.epic('所属分组')  # 这里填业务线
@allure.feature('计划委托')  # 这里填功能
@allure.story('持仓区域下止盈止损最优5档')  # 这里填子功能，没有的话就把本行注释掉
class TestCoinswapTriggerOrder_020:

    @allure.step('前置条件')
    def setup(self):
        print(''' 有持仓且大于等于10张''')
        print(''' 有持仓且大于等于10张''')
        self.contract_code = "EOS-USD"
        self.current_user = SwapService(url=URL, access_key=ACCESS_KEY, secret_key=SECRET_KEY)
        self.common_user = SwapService(url=URL, access_key=COMMON_ACCESS_KEY, secret_key=COMMON_SECRET_KEY)
        position_larger_than_10 = self.current_user.check_positions_larger_than(contract_code=self.contract_code, direction="buy", amount=10)
        if not position_larger_than_10:
            req_eat = self.current_user.eat_orders(contract_code=contract_order, eat_type="all")
            assert req_eat.get("status") == "ok", f"吃盘失败: {req_eat}"
            req_temp_buy = self.current_user.swap_order(contract_code=self.contract_code, price=5, volume=10, direction="buy", offset="open", lever_rate=5, order_price_type="limit")
            assert req_temp_buy.get("status") == "ok", f"下临时买单失败: {req_temp_buy}"
            req_temp_sell = self.current_user.swap_order(contract_code=self.contract_code, price=5, volume=10, direction="sell", offset="open", lever_rate=5, order_price_type="limit")
            assert req_temp_sell.get("status") == "ok", f"下临时卖单失败: {req_temp_sell}"

    @allure.title('持仓区域下止盈止损最优5档')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('1、登录币本位永续界面'):
            before_current_tp_sl_orders = self.current_user.swap_tpsl_openorders(contract_code=self.contract_code).get("data").get("orders")
            latest_swap_trade = self.current_user.swap_trade(contract_code=self.contract_code)
            print("步骤一(1): 获取最新价")
            data_r_swap_trade = latest_swap_trade.get("tick").get("data")
            last_price = float(data_r_swap_trade[0].get("price"))
            tp_trigger_price = round(last_price * 1.1, 1)
            order_price_type = "optimal_5"
            req_tp_sl = self.current_user.swap_tpsl_order(contract_code=self.contract_code, volume=10, direction="sell", tp_trigger_price=tp_trigger_price, tp_order_price=last_price, tp_order_price_type=order_price_type)
            assert req_tp_sl.get("status") == "ok", f"下止盈止损单失败: {req_tp_sl}"
            time.sleep(3)
        with allure.step('2、在当前持仓tab选择持仓BTC/USD多单，点击止盈止损按钮'):
            pass
        with allure.step('3、选择按价格按钮'):
            pass
        with allure.step('4、输入止盈价，止盈价高于最新价（如：50000）'):
            pass
        with allure.step('5、输入卖出价最优5/10/20档，任意一档'):
            pass
        with allure.step('6、输入卖出量10张'):
            pass
        with allure.step('7、点击确认按钮有结果A'):
            after_current_tp_sl_orders = self.current_user.swap_tpsl_openorders(contract_code=self.contract_code).get("data").get("orders")

        with allure.step('8、查看当前委托列表中的止盈止损页面有结果B'):
            new_tp_sl_order = [o for o in after_current_tp_sl_orders if o not in before_current_tp_sl_orders]
            assert len(new_tp_sl_order) == 1, f"新增止盈止损单不为1个, 实际: {new_tp_sl_order}"
            expected_info = {"contract_code": self.contract_code, "direction": "sell", "trigger_type": "ge", "trigger_price": tp_trigger_price, "volume": 10, "status": 2, "order_price_type": order_price_type}
            assert common.util.compare_dict(expected_info, new_tp_sl_order[0])
        with allure.step("撤单"):
            req_cancel = self.current_user.swap_tpsl_cancelall(contract_code=self.contract_code)
            assert req_cancel.get("status") == "ok", f"撤单失败: {req_cancel}"

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
