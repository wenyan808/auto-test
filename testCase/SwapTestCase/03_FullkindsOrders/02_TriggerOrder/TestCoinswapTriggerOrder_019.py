#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210918
# @Author : 邱大伟

#script by: lss
用例编号
    TestCoinswapTriggerOrder_019
所属分组
    计划委托
用例标题
    持仓区域下止盈止损正常限价
前置条件
    有持仓且大于等于10张
    
步骤/文本
    1、登录币本位永续界面
    2、在当前持仓tab选择持仓BTC/USD多单，点击止盈止损按钮
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
from tool.atp import ATP
from config.case_content import epic, features

@allure.epic(epic[1])
@allure.feature(features[2]['feature'])
@allure.story(features[2]['story'][2])
class TestCoinswapTriggerOrder_019:

    @allure.step('前置条件')
    def setup(self):
        print(''' 有持仓且大于等于10张''')
        self.current_user = SwapService(url=URL, access_key=ACCESS_KEY, secret_key=SECRET_KEY)
        self.common_user = SwapService(url=URL, access_key=COMMON_ACCESS_KEY, secret_key=COMMON_SECRET_KEY)
        ATP.current_user_make_order(direction='sell')
        time.sleep(1)
        ATP.current_user_make_order(direction='buy')
        time.sleep(1)
        ATP.make_market_depth()
        time.sleep(1)

    @allure.title('持仓区域下止盈止损正常限价')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        self.contract_code = contract_code
        with allure.step('1、登录币本位永续界面'):
            before_current_tp_sl_orders = self.current_user.swap_tpsl_openorders(contract_code=self.contract_code).get("data").get("orders")
            latest_swap_trade = self.current_user.swap_trade(contract_code=self.contract_code)
            print("步骤一(1): 获取最新价")
            data_r_swap_trade = latest_swap_trade.get("tick").get("data")
            last_price = float(data_r_swap_trade[0].get("price"))
            tp_trigger_price = round(last_price * 1.1, 1)
            req_tp_sl = self.current_user.swap_tpsl_order(contract_code=self.contract_code, volume=10, direction="sell", tp_trigger_price=tp_trigger_price, tp_order_price=last_price)
            assert req_tp_sl.get("status") == "ok", f"下止盈止损单失败: {req_tp_sl}"
            time.sleep(3)
        with allure.step('2、在当前持仓tab选择持仓BTC/USD多单，点击止盈止损按钮'):
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
            after_current_tp_sl_orders = self.current_user.swap_tpsl_openorders(contract_code=self.contract_code).get("data").get("orders")
            new_tp_sl_order = [o for o in after_current_tp_sl_orders if o not in before_current_tp_sl_orders]
            assert len(new_tp_sl_order) == 1, f"新增止盈止损单不为1个, 实际: {new_tp_sl_order}"
            expected_info = {"contract_code": self.contract_code, "direction": "sell", "trigger_type": "ge", "trigger_price": tp_trigger_price, "volume": 10, "status": 2}
            assert common.util.compare_dict(expected_info, new_tp_sl_order[0])
        with allure.step("撤单"):
            req_cancel = self.current_user.swap_tpsl_cancelall(contract_code=self.contract_code)
            assert req_cancel.get("status") == "ok", f"撤单失败: {req_cancel}"

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_types_order()
        ATP.clean_market()


if __name__ == '__main__':
    pytest.main()
