#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210923
# @Author : 邱大伟

#script by: lss
用例编号
    TestUSDTSwapTriggerOrder_013
所属分组
    计划委托
用例标题
    撤销计划委托订单平仓测试
前置条件
    不要触发
步骤/文本
    1、登录U本位永续界面
    2、选择BTC当周，选择杠杆5X，点击平仓-计划按钮
    3、输入触发价（如：50000）
    4、输入买入价，偏离最新价不要成交（如：40000）
    5、输入买入量10张
    6、点击买入平空按钮后弹框确认后有结果A
    7、查看当前委托列表中的计划委托有结果B
    8、点击撤销按钮有结果C
    9、检查历史委托-计划委托界面有结果D
预期结果
    A)提示下单成功
    B)在当前委托-计划委托统计数量+1，列表数量+1,展示合约交易类型，委托类型，倍数，时间，委托数量，委托价信息和下单数值一致
    C)提示撤销申请成功，当前委托-计划委托列表订单消失
    D)在历史委托-计划委托中有撤销订单记录，且各项信息和下单数据一致
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
@allure.story('撤销计划委托订单平仓测试')  # 这里填子功能，没有的话就把本行注释掉
class TestUSDTSwapTriggerOrder_013:

    @allure.step('前置条件')
    def setup(self):
        print(''' 不要触发 ''')
        self.contract_code = conf.DEFAULT_CONTRACT_CODE
        self.current_user = LinearServiceAPI(url=URL2, access_key=ACCESS_KEY, secret_key=SECRET_KEY)
        ATP.clean_market()
        time.sleep(1)
        ATP.current_user_make_order(direction='buy')
        time.sleep(1)
        ATP.current_user_make_order(direction='sell')
        time.sleep(1)

    @allure.title('撤销计划委托订单平仓测试')
    @allure.step('测试执行')
    def test_execute(self, symbol):
        with allure.step('1、登录U本位永续界面'):
            # 下计划委托前，获取一遍当前计划委托单列表
            current_plan_orders_before = self.current_user.linear_trigger_openorders(
                contract_code=self.contract_code).get("data").get("orders")


            highest_price_bid = ATP.get_adjust_price()
            trigger_price = highest_price_bid
            order_price = round(trigger_price * 0.9, 1)
            r_order_plan = self.current_user.linear_trigger_order(contract_code=self.contract_code, trigger_type="ge",
                                                                  trigger_price=trigger_price, order_price=order_price,
                                                                  order_price_type="limit", volume=10, direction="buy",
                                                                  offset="close", lever_rate=5)
            assert r_order_plan.get("status") == "ok", f"下计划委托单失败: {r_order_plan}"
            plan_order_id = r_order_plan.get("data").get("order_id")
            time.sleep(3)
        with allure.step('2、选择BTC当周，选择杠杆5X，点击平仓-计划按钮'):
            pass
        with allure.step('3、输入触发价（如：50000）'):
            pass
        with allure.step('4、输入买入价，偏离最新价不要成交（如：40000）'):
            pass
        with allure.step('5、输入买入量10张'):
            pass
        with allure.step('6、点击买入平空按钮后弹框确认后有结果A'):
            pass
        with allure.step('7、查看当前委托列表中的计划委托有结果B'):
            current_plan_orders_after = self.current_user.linear_trigger_openorders(
                contract_code=self.contract_code).get("data").get("orders")
            new_plan_orders = [i for i in current_plan_orders_after if i not in current_plan_orders_before]
            assert len(new_plan_orders) == 1, f"新增计划委托单不止一个或为0个: {new_plan_orders}"
            new_plan_order = new_plan_orders[0]
            expected_info = {"contract_code": self.contract_code, "trigger_type": "ge", "volume": 10,
                             "direction": "buy", "lever_rate": 5, "trigger_price": trigger_price,
                             "order_price": order_price, "order_price_type": "limit", "margin_mode": "isolated",
                             "offset": "close"}
            assert common.util.compare_dict(expected_info, new_plan_order)
        with allure.step('8、点击撤销按钮有结果C'):
            r_cancel = self.current_user.linear_trigger_cancel(order_id=plan_order_id, contract_code=self.contract_code)
            assert r_cancel.get("status") == "ok", f"撤单失败: {r_cancel}"
            time.sleep(4)
        with allure.step('9、检查历史委托-计划委托界面有结果D'):
            trigger_his_orders = self.current_user.linear_trigger_hisorders(contract_code=self.contract_code,
                                                                            status="6", trade_type=3,
                                                                            create_date=7).get("data").get("orders")
            trigger_order = [i for i in trigger_his_orders if i.get("order_id") == plan_order_id]
            assert len(trigger_order) == 1, f"生成的历史计划订单不止一个或为0: {trigger_order}"
            trigger_order = trigger_order[0]
            expected_info = {"contract_code": self.contract_code, "trigger_type": "ge", "margin_mode": "isolated",
                             "volume": 10, "direction": "buy", "offset": "close", "lever_rate": 5, "status": 6,
                             "trigger_price": trigger_price, "order_price_type": "limit"}
            assert common.util.compare_dict(expected_info, trigger_order)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_types_order()


if __name__ == '__main__':
    pytest.main()
