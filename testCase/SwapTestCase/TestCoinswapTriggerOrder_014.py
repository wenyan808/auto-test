#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210918
# @Author : 邱大伟

#script by: lss
用例编号
    TestCoinswapTriggerOrder_014
所属分组
    计划委托
用例标题
    全部撤销计划委托订单
前置条件
    不要触发，至少2条以上订单
步骤/文本
    1、登录币本位永续界面
    2、选择BTC/USD，选择杠杆5X，点击开仓-计划按钮
    3、下单至少2条以上订单
    4、检查当前委托-计划委托列表有结果A
    5、点击全部撤销按钮弹框选择计划委托类型,点击确定后有结果B
    6、检查当前委托-计划委托信息有结果C
    7、检查历史委托-计划委托信息有结果D
预期结果
    A)在当前委托-计划委托列表显示了步骤3下的左右订单
    B)t提示撤销申请成功
    C)当前委托-计划委托列表订单消失
    D)在历史委托-计划委托包含全部撤销的订单
用例作者
    邱大伟
自动化作者
    刘双双
"""

import common.util
from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api, SwapService
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest, allure, random, time

from config.conf import URL, LSS_ACCESS_KEY, COMMON_ACCESS_KEY, LSS_SECRET_KEY, COMMON_SECRET_KEY


@allure.epic('所属分组')  # 这里填业务线
@allure.feature('计划委托')  # 这里填功能
@allure.story('全部撤销计划委托订单')  # 这里填子功能，没有的话就把本行注释掉
class TestCoinswapTriggerOrder_014:

    @allure.step('前置条件')
    def setup(self):
        print(''' 不要触发，至少2条以上订单 ''')
        print(''' 选择正常限价下单 ''')
        self.current_user = SwapService(url=URL, access_key=LSS_ACCESS_KEY, secret_key=LSS_SECRET_KEY)
        self.common_user = SwapService(url=URL, access_key=COMMON_ACCESS_KEY, secret_key=COMMON_SECRET_KEY)
        self.contract_type = "this_week"
        self.contract_code = "EOS-USD"
        self.symbol = "EOS"
        self.lever_rate = 5
        latest_swap_trade = self.current_user.swap_trade(contract_code=self.contract_code)
        print("步骤一(0): 获取最新价")
        data_r_swap_trade = latest_swap_trade.get("tick").get("data")
        self.last_price = float(data_r_swap_trade[0].get("price"))
        self.trigger_price = self.last_price
        self.trigger_type = "ge"
        self.order_price = round(self.last_price * 0.9, 1)

    @allure.title('全部撤销计划委托订单')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('1、登录币本位永续界面'):
            print(''' 选择正常限价下单 ''')
            self.current_user = SwapService(url=URL, access_key=LSS_ACCESS_KEY, secret_key=LSS_SECRET_KEY)
            self.common_user = SwapService(url=URL, access_key=COMMON_ACCESS_KEY, secret_key=COMMON_SECRET_KEY)
            self.contract_type = "this_week"
            self.contract_code = "EOS-USD"
            self.symbol = "EOS"
            self.lever_rate = 5
            latest_swap_trade = self.current_user.swap_trade(contract_code=self.contract_code)
            print("步骤一(0): 获取最新价")
            data_r_swap_trade = latest_swap_trade.get("tick").get("data")
            self.last_price = float(data_r_swap_trade[0].get("price"))
            self.trigger_price = self.last_price
            self.trigger_type = "ge"
            self.order_price = round(self.last_price * 0.9, 1)
        with allure.step('2、选择BTC/USD，选择杠杆5X，点击开仓-计划按钮'):
            pass
        with allure.step('3、下单至少2条以上订单'):
            r_new_open_1 = self.current_user.swap_trigger_order(contract_code=self.contract_code, trigger_type=self.trigger_type, trigger_price=self.trigger_price, order_price=self.order_price, volume=10, direction="buy", offset="open", lever_rate=self.lever_rate)
            assert r_new_open_1.get("status") == "ok", f"下单失败: {r_new_open_1}"
            order_id_open_1 = r_new_open_1.get("data").get("order_id")
            r_new_open_2 = self.current_user.swap_trigger_order(contract_code=self.contract_code, trigger_type=self.trigger_type, trigger_price=self.trigger_price, order_price=self.order_price, volume=10, direction="buy", offset="open", lever_rate=self.lever_rate)
            assert r_new_open_1.get("status") == "ok", f"下单失败: {r_new_open_2}"
            order_id_open_2 = r_new_open_2.get("data").get("order_id")
        with allure.step('4、检查当前委托-计划委托列表有结果A'):
            time.sleep(3)
            all_order_plans = self.current_user.swap_trigger_openorders(contract_code=self.contract_code).get("data").get("orders")
            checked = []
            expected_info = {"symbol": self.symbol, "trigger_type": self.trigger_type, "volume": 10, "direction": "buy", "offset": "open", "trigger_price": self.trigger_price, "order_price": self.order_price, "status": 2}
            for o in all_order_plans:
                if o.get("order_id") in [order_id_open_1, order_id_open_2]:
                    assert common.util.compare_dict(expected_info, o)
                    checked.append(True)
            cancel_orders_ids = [order_id_open_1, order_id_open_2]
            if not all(checked):
                raise BaseException("在当前委托单{all_order_plans}中未找到计划委托单{order_id}".format(all_order_plans=all_order_plans, order_id=cancel_orders_ids))
        with allure.step('5、点击全部撤销按钮弹框选择计划委托类型,点击确定后有结果B'):
            r_cancel_all = self.current_user.swap_trigger_cancelall(contract_code=self.contract_code)
            assert r_cancel_all.get("status") == "ok", f"全部撤销失败: {r_cancel_all}"
            time.sleep(3)
        with allure.step('6、检查当前委托-计划委托信息有结果C'):
            pass
        with allure.step('7、检查历史委托-计划委托信息有结果D'):
            all_his_orders = self.current_user.swap_trigger_hisorders(contract_code=self.contract_code, trade_type=1, status="6", create_date=7).get("data").get("orders")
            actual_order = [i for i in all_his_orders if i.get("order_id") in cancel_orders_ids]
            assert len(actual_order) == 2, f"找不到期望的计划委托单或有多个这样的计划委托单, 实际单号列表为: {all_his_orders}"
            for o in actual_order:
                expected_info = {"symbol": self.symbol, "trigger_type": self.trigger_type, "volume": 10, "direction": "buy", "offset": "open", "trigger_price": self.trigger_price, "order_price": self.order_price, "status": 6}
                assert common.util.compare_dict(expected_info, o)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
