#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210923
# @Author : 邱大伟

#script by: lss
用例编号
    TestUSDTSwapTriggerOrder_014
所属分组
    计划委托
用例标题
    全部撤销计划委托订单
前置条件
    不要触发，至少2条以上订单
步骤/文本
    1、登录U本位永续界面
    2、选择BTC当周，选择杠杆5X，点击开仓-计划按钮
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
@allure.story('全部撤销计划委托订单')  # 这里填子功能，没有的话就把本行注释掉
class TestUSDTSwapTriggerOrder_014:

    @allure.step('前置条件')
    def setup(self):
        print(''' 不要触发，至少2条以上订单 ''')
        self.contract_code = conf.DEFAULT_CONTRACT_CODE
        self.current_user = LinearServiceAPI(url=URL2, access_key=ACCESS_KEY, secret_key=SECRET_KEY)
        ATP.clean_market()
        time.sleep(1)
        ATP.current_user_make_order(direction='buy')
        time.sleep(1)
        ATP.current_user_make_order(direction='sell')
        time.sleep(1)

    @allure.title('全部撤销计划委托订单')
    @allure.step('测试执行')
    def test_execute(self, symbol):
        with allure.step('1、登录U本位永续界面'):

            highest_price_bid = ATP.get_adjust_price()
            trigger_price = highest_price_bid
            order_price = round(trigger_price * 0.9, 1)
            r_order_plan = self.current_user.linear_trigger_order(contract_code=self.contract_code, trigger_type="ge",
                                                                  trigger_price=trigger_price, order_price=order_price,
                                                                  order_price_type="limit", volume=10, direction="buy",
                                                                  offset="open", lever_rate=5)
            assert r_order_plan.get("status") == "ok", f"下计划委托单失败: {r_order_plan}"
            plan_order_id = r_order_plan.get("data").get("order_id")
            r_order_plan_2 = self.current_user.linear_trigger_order(contract_code=self.contract_code, trigger_type="ge",
                                                                    trigger_price=trigger_price,
                                                                    order_price=order_price, order_price_type="limit",
                                                                    volume=10, direction="buy", offset="open",
                                                                    lever_rate=5)
            assert r_order_plan_2.get("status") == "ok", f"下计划委托单失败: {r_order_plan_2}"
            plan_order_id_2 = r_order_plan_2.get("data").get("order_id")
            time.sleep(3)
            print(plan_order_id, plan_order_id_2)

        with allure.step('2、选择BTC当周，选择杠杆5X，点击开仓-计划按钮'):
            pass
        with allure.step('3、下单至少2条以上订单'):
            pass
        with allure.step('4、检查当前委托-计划委托列表有结果A'):
            pass
        with allure.step('5、点击全部撤销按钮弹框选择计划委托类型,点击确定后有结果B'):
            r_cancel_all = self.current_user.linear_trigger_cancelall(contract_code=self.contract_code)
            assert r_cancel_all.get("status") == "ok", f"撤销所有计划单失败: {r_cancel_all}"
            time.sleep(4)
        with allure.step('6、检查当前委托-计划委托信息有结果C'):
            pass
        with allure.step('7、检查历史委托-计划委托信息有结果D'):
            trigger_his_orders = self.current_user.linear_trigger_hisorders(contract_code=self.contract_code,
                                                                            status="6", trade_type=1,
                                                                            create_date=7).get("data").get("orders")
            trigger_order = [i for i in trigger_his_orders if i.get("order_id") in [plan_order_id, plan_order_id_2]]
            assert len(trigger_order) == 2, f"生成的历史计划订单不为2个: {trigger_order}"
            for o in trigger_order:
                expected_info = {"contract_code": self.contract_code, "trigger_type": "ge", "margin_mode": "isolated",
                                 "volume": 10, "direction": "buy", "offset": "open", "lever_rate": 5, "status": 6,
                                 "trigger_price": trigger_price, "order_price_type": "limit"}
                assert common.util.compare_dict(expected_info, o)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_types_order()


if __name__ == '__main__':
    pytest.main()
