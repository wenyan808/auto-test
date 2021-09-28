#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210923
# @Author : 邱大伟

#script by: lss
用例编号
    TestUSDTSwapTriggerOrder_011
所属分组
    计划委托
用例标题
    触发计划委托订单平仓测试
前置条件
    选择正常限价下单
步骤/文本
    1、登录U本位永续界面
    2、选择BTC当周，选择杠杆5X，点击平仓-计划按钮
    3、输入触发价，可以取买一卖一价格（如：50000）
    4、输入买入价，偏离最新价不要成交（如：40000）
    5、输入买入量10张
    6、点击买入平空按钮有结果A
    7、查看当前委托列表中的计划委托有结果B
    8、最新价达到触发价时，正常触发订单后，检查计划委托列表和限价委托列表有结果C
预期结果
    A)提示下单成功
    B)在当前委托-计划委托统计数量+1，列表数量+1,展示合约交易类型，委托类型，倍数，时间，委托数量，委托价信息和下单数值一致
    C)计划委托列表订单消失，限价委托列表出现触发订单，且各项信息和下单数据一致
用例作者
    邱大伟
自动化作者
    刘双双
"""

import common.util
from common.LinearServiceAPI import LinearServiceAPI
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest, allure, random, time
from config.conf import URL2, ACCESS_KEY, SECRET_KEY, COMMON_ACCESS_KEY, COMMON_SECRET_KEY


@allure.epic('所属分组')  # 这里填业务线
@allure.feature('计划委托')  # 这里填功能
@allure.story('触发计划委托订单平仓测试')  # 这里填子功能，没有的话就把本行注释掉
class TestUSDTSwapTriggerOrder_011:

    @allure.step('前置条件')
    def setup(self):
        print(''' 选择正常限价下单 ''')
        self.contract_code = "BTC-USDT"
        self.current_user = LinearServiceAPI(url=URL2, access_key=ACCESS_KEY, secret_key=SECRET_KEY)

    @allure.title('触发计划委托订单平仓测试')
    @allure.step('测试执行')
    def test_execute(self, symbol):
        with allure.step("0、进行一次买卖，保证可平多量至少为10"):
            position_larger_than_10 = self.current_user.check_positions_larger_than(contract_code=self.contract_code, direction="sell", amount=10, position_type=1)
            price = 5
            if not position_larger_than_10:
                # 获取买一价, 以稍高与买一价的价格进行一次买->卖，制造持仓(逐仓)
                contract_depth = self.current_user.linear_depth(contract_code=self.contract_code, type="step5")
                bids = contract_depth.get("tick").get("bids")
                if bids:
                    highest_price_bid = round(max([i[0] for i in bids]) * 1.1, 1)
                    price = max([price, highest_price_bid])
                o_buy = self.current_user.linear_order(contract_code=self.contract_code, price=price, volume=10, direction="buy", offset="open", lever_rate=5, order_price_type="limit")
                assert o_buy.get("status") == "ok", f"下买单失败: {o_buy}"
                o_sell = self.current_user.linear_order(contract_code=self.contract_code, price=price, volume=10, direction="sell", offset="open", lever_rate=5, order_price_type="limit")
                assert o_sell.get("status") == "ok", f"下卖单失败: {o_sell}"
                time.sleep(3)

        with allure.step('1、登录U本位永续界面'):
            # 下计划委托前，获取一遍当前计划委托单列表
            current_plan_orders_before = self.current_user.linear_trigger_openorders(contract_code=self.contract_code).get("data").get("orders")
            # 获取买一价, 如果买一价不存在, 则手动设置买一价为5
            contract_depth = self.current_user.linear_depth(contract_code=self.contract_code, type="step5")
            bids = contract_depth.get("tick").get("bids")
            if bids:
                highest_price_bid = round(max([i[0] for i in bids]) * 1.1, 1)
                trigger_price = highest_price_bid
            else:
                trigger_price = 5
            order_price = round(trigger_price * 0.9, 1)
            r_order_plan = self.current_user.linear_trigger_order(contract_code=self.contract_code, trigger_type="ge", trigger_price=trigger_price, order_price=order_price, order_price_type="limit", volume=10, direction="buy", offset="close", lever_rate=5)
            assert r_order_plan.get("status") == "ok", f"下计划委托单失败: {r_order_plan}"
            plan_order_id = r_order_plan.get("data").get("order_id")
            time.sleep(3)
        with allure.step('2、选择BTC当周，选择杠杆5X，点击平仓-计划按钮'):
            pass
        with allure.step('3、输入触发价，可以取买一卖一价格（如：50000）'):
            pass
        with allure.step('4、输入买入价，偏离最新价不要成交（如：40000）'):
            pass
        with allure.step('5、输入买入量10张'):
            pass
        with allure.step('6、点击买入平空按钮有结果A'):
            pass
        with allure.step('7、查看当前委托列表中的计划委托有结果B'):
            current_plan_orders_after = self.current_user.linear_trigger_openorders(contract_code=self.contract_code).get("data").get("orders")
            new_plan_orders = [i for i in current_plan_orders_after if i not in current_plan_orders_before]
            assert len(new_plan_orders) == 1, f"新增计划委托单不止一个或为0个: {new_plan_orders}"
            new_plan_order = new_plan_orders[0]
            expected_info = {"contract_code": self.contract_code, "trigger_type": "ge", "volume": 10, "direction": "buy", "lever_rate": 5, "trigger_price": trigger_price, "order_price": order_price, "order_price_type": "limit", "margin_mode": "isolated", "offset": "close"}
            assert common.util.compare_dict(expected_info, new_plan_order)
        with allure.step('8、最新价达到触发价时，正常触发订单后，检查计划委托列表和限价委托列表有结果C'):
            # 用通用账号来下一个成交的买->卖，达到触发价
            before_trigger_current_limit_open_orders = self.current_user.linear_openorders(contract_code=self.contract_code).get("data").get("orders")
            common_user = LinearServiceAPI(url=URL2, access_key=COMMON_ACCESS_KEY, secret_key=COMMON_SECRET_KEY)
            req_common_sell = common_user.linear_order(contract_code=self.contract_code, price=trigger_price, volume=10, direction="sell", offset="open", lever_rate=5, order_price_type="limit")
            assert req_common_sell.get("status") == "ok", f"通用账号下卖单失败: {req_common_sell}"
            req_common_buy = common_user.linear_order(contract_code=self.contract_code, price=trigger_price, volume=10, direction="buy", offset="open", lever_rate=5, order_price_type="limit")
            assert req_common_buy.get("status") == "ok", f"通用账号下买单失败: {req_common_sell}"
            time.sleep(3)
            after_trigger_current_limit_open_orders = self.current_user.linear_openorders(contract_code=self.contract_code).get("data").get("orders")
            new_limit_open_orders = [o for o in after_trigger_current_limit_open_orders if o not in before_trigger_current_limit_open_orders]
            assert len(new_limit_open_orders) == 1, f"新增限价委托单不止一个或为0个: {new_limit_open_orders}"
            new_limit_open_order = new_limit_open_orders[0]
            new_limit_order_id = new_limit_open_order.get("order_id")
            expected_info = {"contract_code": self.contract_code, "price": order_price, "order_price_type": "limit", "direction": "buy", "lever_rate": 5, "status": 3, "order_source": "trigger"}
            assert common.util.compare_dict(expected_info, new_limit_open_order)
        with allure.step("撤单"):
            r_cancel = self.current_user.linear_cancel(order_id=new_limit_order_id, contract_code=self.contract_code)
            assert r_cancel.get("status") == "ok", f"撤单失败: {r_cancel}"

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
