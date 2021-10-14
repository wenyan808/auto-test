#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210923
# @Author : 邱大伟

#script by: lss
用例编号
    TestUSDTSwapTriggerOrder_019
所属分组
    计划委托
用例标题
    持仓区域下止盈止损正常限价
前置条件
    有持仓且大于等于10张
    
步骤/文本
    1、登录U本位永续界面
    2、在当前持仓tab选择持仓BTC当周多单，点击止盈止损按钮
    3、选择按价格按钮
    4、输入止盈价，止盈价高于最新价（如：50000）
    5、输入卖出价55000
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

import allure
import pytest
import time

import common.util
from common.LinearServiceAPI import LinearServiceAPI
from config import conf
from config.conf import URL2, ACCESS_KEY, SECRET_KEY
from tool.atp import ATP


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('计划委托')  # 这里填功能
@allure.story('持仓区域下止盈止损正常限价')  # 这里填子功能，没有的话就把本行注释掉
class TestUSDTSwapTriggerOrder_019:

    @allure.step('前置条件')
    def setup(self):
        print(''' 有持仓且大于等于10张''')
        ATP.clean_market()
        time.sleep(1)
        ATP.current_user_make_order(direction='sell')
        time.sleep(1)
        ATP.current_user_make_order(direction='buy')
        time.sleep(1)

        self.contract_code = conf.DEFAULT_CONTRACT_CODE
        self.current_user = LinearServiceAPI(url=URL2, access_key=ACCESS_KEY, secret_key=SECRET_KEY)
        price = ATP.get_current_price()
        self.open_price = price

    @allure.title('持仓区域下止盈止损正常限价')
    @allure.step('测试执行')
    def test_execute(self, symbol):
        with allure.step('1、登录U本位永续界面'):
            pass
        with allure.step('2、在当前持仓tab选择持仓BTC当周多单，点击止盈止损按钮'):
            latest_trades = self.current_user.linear_trade(contract_code=self.contract_code)
            last_price = float(latest_trades.get("tick").get("data")[0].get("price"))
            trigger_price = round(last_price * 1.1, 1)
            tp_order_price = trigger_price
            req = self.current_user.linear_tpsl_order(contract_code=self.contract_code, direction="sell", volume=10,
                                                      tp_trigger_price=trigger_price, tp_order_price=tp_order_price)
            assert req.get("status") == "ok", f"下单失败: {req}"
            order_id = req.get("data").get("tp_order").get("order_id")
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
            current_open_tp_sl_orders = self.current_user.linear_tpsl_openorders(contract_code=self.contract_code).get(
                "data").get('orders')
            actual_tp_sl_order = [i for i in current_open_tp_sl_orders if i.get("order_id") == order_id]
            assert len(actual_tp_sl_order) == 1, f"生成的止盈止损单不止一个或为0个: {actual_tp_sl_order}"
            actual_tp_sl_order = actual_tp_sl_order[0]
            expected_info = {"contract_code": self.contract_code, "volume": 10, "direction": "sell",
                             "trigger_type": "ge", "order_price": tp_order_price, "order_price_type": "limit",
                             "tpsl_order_type": "tp"}
            assert common.util.compare_dict(expected_info, actual_tp_sl_order)
        with allure.step("撤单"):
            r_cancel = self.current_user.linear_tpsl_cancelall(contract_code=self.contract_code)
            assert r_cancel.get("status") == "ok", f"撤单失败: {r_cancel}"

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_types_order()


if __name__ == '__main__':
    pytest.main()
