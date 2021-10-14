#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210923
# @Author : 邱大伟

#script by: lss
用例编号
    TestUSDTSwapTriggerOrder_008
所属分组
    计划委托
用例标题
    计划止损正常限价
前置条件
    有持仓且大于等于10张，
    触发价小于最新价
步骤/文本
    1、登录U本位永续界面
    2、在当前持仓tab选择持仓BTC当周多单，点击计划委托按钮
    3、选择计划止损按钮
    4、输入触发价，触发价高于开仓均价和收益率自动计算（如：50000）
    4、输入卖出价51000
    5、输入卖出量10张
    6、点击止损按钮有结果A
    7、查看当前委托列表中的计划委托有结果B
预期结果
    A)提示下单成功
    B)在当前委托-计划委托统计数量+1，列表数量+1,展示合约交易类型，委托类型，倍数，时间，委托数量，委托价信息和下单数值一致
用例作者
    邱大伟
自动化作者
    刘双双
"""

import time

import allure
import pytest

import common.util
from common.LinearServiceAPI import LinearServiceAPI
from config import conf
from config.conf import URL2, ACCESS_KEY, SECRET_KEY
from tool.atp import ATP


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('计划委托')  # 这里填功能
@allure.story('计划止损正常限价')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestUSDTSwapTriggerOrder_008:

    @allure.step('前置条件')
    def setup(self):
        print(''' 有持仓且大于等于10张， 触发价小于最新价 ''')
        self.contract_code = conf.DEFAULT_CONTRACT_CODE
        self.current_user = LinearServiceAPI(url=URL2, access_key=ACCESS_KEY, secret_key=SECRET_KEY)
        position_larger_than_10 = self.current_user.check_positions_larger_than(contract_code=self.contract_code,
                                                                                direction="buy", amount=10,
                                                                                position_type=1)
        price = ATP.get_current_price()
        if not position_larger_than_10:
            # 获取买一价, 以稍高与买一价的价格进行一次买->卖，制造持仓(逐仓)
            contract_depth = self.current_user.linear_depth(contract_code=self.contract_code, type="step5")
            bids = contract_depth.get("tick").get("bids")
            if bids:
                highest_price_bid = round(max([i[0] for i in bids]) * 1.1, 1)
                price = max([price, highest_price_bid])
            o_buy = self.current_user.linear_order(contract_code=self.contract_code, price=price, volume=10,
                                                   direction="buy", offset="open", lever_rate=5,
                                                   order_price_type="limit")
            assert o_buy.get("status") == "ok", f"下买单失败: {o_buy}"
            o_sell = self.current_user.linear_order(contract_code=self.contract_code, price=price, volume=10,
                                                    direction="sell", offset="open", lever_rate=5,
                                                    order_price_type="limit")
            assert o_sell.get("status") == "ok", f"下卖单失败: {o_sell}"
            time.sleep(3)
        self.open_price = price

    @allure.title('计划止损正常限价')
    @allure.step('测试执行')
    def test_execute(self, symbol):
        with allure.step('1、登录U本位永续界面'):
            # 获取最新价
            latest_trades = self.current_user.linear_trade(contract_code=self.contract_code)
            last_price = float(latest_trades.get("tick").get("data")[0].get("price"))
            trigger_price = round(last_price * 0.9, 1)
            order_price = trigger_price
            current_plan_orders_before = self.current_user.linear_trigger_openorders(
                contract_code=self.contract_code).get("data").get("orders")
            r_order_plan = self.current_user.linear_trigger_order(contract_code=self.contract_code, trigger_type="le",
                                                                  trigger_price=trigger_price, order_price=order_price,
                                                                  order_price_type="limit", volume=10, direction="sell",
                                                                  offset="close")
            assert r_order_plan.get("status") == "ok", f"下计划委托单失败: {r_order_plan}"
            order_id = r_order_plan.get("data").get("order_id")
            time.sleep(3)
        with allure.step('2、在当前持仓tab选择持仓BTC当周多单，点击计划委托按钮'):
            pass
        with allure.step('3、选择计划止损按钮'):
            pass
        with allure.step('4、输入触发价，触发价高于开仓均价和收益率自动计算（如：50000）'):
            pass
        with allure.step('4、输入卖出价51000'):
            pass
        with allure.step('5、输入卖出量10张'):
            pass
        with allure.step('6、点击止损按钮有结果A'):
            pass
        with allure.step('7、查看当前委托列表中的计划委托有结果B'):
            current_plan_orders_after = self.current_user.linear_trigger_openorders(
                contract_code=self.contract_code).get("data").get("orders")
            new_plan_orders = [i for i in current_plan_orders_after if i not in current_plan_orders_before]
            assert len(new_plan_orders) == 1, f"新增计划委托单不止一个或为0个: {new_plan_orders}"
            new_plan_order = new_plan_orders[0]
            expected_info = {"contract_code": self.contract_code, "trigger_type": "le", "volume": 10,
                             "direction": "sell", "lever_rate": 5, "trigger_price": trigger_price,
                             "order_price": order_price, "order_price_type": "limit", "margin_mode": "isolated"}
            assert common.util.compare_dict(expected_info, new_plan_order)

    @allure.step('恢复环境')
    def teardown(self):
        r_cancel = self.current_user.linear_trigger_cancelall(contract_code=self.contract_code)
        assert r_cancel.get('status') == "ok", f"撤单失败: {r_cancel}"
        ATP.cancel_all_types_order()



if __name__ == '__main__':
    pytest.main()
