#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210918
# @Author : 邱大伟

#script by: lss
用例编号
    TestCoinswapTriggerOrder_011
所属分组
    计划委托
用例标题
    触发计划委托订单平仓测试
前置条件
    选择正常限价下单
步骤/文本
    1、登录币本位永续界面
    2、选择BTC/USD，选择杠杆5X，点击平仓-计划按钮
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
from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api, SwapService
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest, allure, random, time

from config.conf import URL, ACCESS_KEY, COMMON_ACCESS_KEY, SECRET_KEY, COMMON_SECRET_KEY


@allure.epic('所属分组')  # 这里填业务线
@allure.feature('计划委托')  # 这里填功能
@allure.story('触发计划委托订单平仓测试')  # 这里填子功能，没有的话就把本行注释掉
class TestCoinswapTriggerOrder_011:

    @allure.step('前置条件')
    def setup(self):
        print(''' 选择正常限价下单 ''')
        self.current_user = SwapService(url=URL, access_key=ACCESS_KEY, secret_key=SECRET_KEY)
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

    @allure.title('触发计划委托订单平仓测试')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('1、登录币本位永续界面'):
            r_plan_close = self.current_user.swap_trigger_order(contract_code=self.contract_code, trigger_type=self.trigger_type, trigger_price=self.trigger_price, order_price=self.order_price, order_price_type="limit", volume=10, direction="buy", offset="close",
                                                                lever_rate=self.lever_rate)
            assert r_plan_close.get("status") == "ok", f"平仓下计划单失败: {r_plan_close}"
            self.order_id = r_plan_close.get("data").get("order_id")
        with allure.step('2、选择BTC/USD，选择杠杆5X，点击平仓-计划按钮'):
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
            time.sleep(3)
            all_order_plans = self.current_user.swap_trigger_openorders(contract_code=self.contract_code).get("data").get("orders")
            checked = False
            for o in all_order_plans:
                if o.get("order_id") == self.order_id:
                    expected_info = {"symbol": self.symbol, "trigger_type": "ge", "volume": 10, "order_type": 1, "direction": "buy", "offset": "close", "trigger_price": self.trigger_price, "order_price": self.order_price, "status": 2}
                    assert common.util.compare_dict(expected_info, o)
                    checked = True
                    break
            if not checked:
                raise BaseException("在当前委托单{all_order_plans}中未找到计划委托单{order_id}".format(all_order_plans=all_order_plans, order_id=self.order_id))
        with allure.step('8、最新价达到触发价时，正常触发订单后，检查计划委托列表和限价委托列表有结果C'):
            print("查询当前限价委托单")
            before_auto_cancel_plan_orders = self.current_user.swap_openorders(contract_code=self.contract_code).get("data").get("orders")
            print("用trigger_price做一次成交，使最新价达到触发价")
            r_temp_sell = self.current_user.swap_order(contract_code=self.contract_code, price=self.trigger_price, volume=10, direction="sell", offset="open", lever_rate=5, order_price_type="limit")
            assert r_temp_sell.get("status") == "ok", f"下临时卖单失败: {r_temp_sell}"
            r_temp_buy = self.current_user.swap_order(contract_code=self.contract_code, price=self.trigger_price, volume=10, direction="buy", offset="open", lever_rate=5, order_price_type="limit")
            assert r_temp_buy.get("status") == "ok", f"下临时卖单失败: {r_temp_buy}"
            time.sleep(3)
            new_all_order_plans = self.current_user.swap_trigger_openorders(contract_code=self.contract_code).get("data").get("orders")
            new_order_ids = [i.get("order_id") for i in new_all_order_plans]
            assert self.order_id not in new_order_ids, "最新价达到触发价后, 计划委托单中的{order_id}未消失".format(order_id=self.order_id)
            print("再次查询当前限价委托单，并与之前的做对比，应该新增一条，并且参数对得上")
            after_auto_cancel_plan_orders = self.current_user.swap_openorders(contract_code=self.contract_code).get("data").get("orders")
            new_orders = [i for i in after_auto_cancel_plan_orders if i not in before_auto_cancel_plan_orders]
            assert len(new_orders) == 1, f"找不到新增的限价委托单或新增的限价委托单多于1个! 新增的限价委托单为{new_orders}"
            new_order = new_orders[0]
            expected_info = {"symbol": self.symbol, "contract_code": self.contract_code, "volume": 10, "order_type": 1, "direction": "buy", "offset": "close", "status": 3}
            assert common.util.compare_dict(expected_info, new_order)
            new_order_id = new_order.get("order_id")
            print('撤单')
            r_cancel = self.current_user.swap_cancel(order_id=new_order_id, contract_code=self.contract_code)
            assert r_cancel.get("status") == "ok", f"撤单失败: {r_cancel}"

    @allure.step('恢复环境')
    def teardown(self):
        pass


if __name__ == '__main__':
    pytest.main()
