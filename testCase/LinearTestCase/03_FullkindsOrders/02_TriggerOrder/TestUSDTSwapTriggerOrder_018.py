#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210923
# @Author : 邱大伟

#script by: lss
用例编号
    TestUSDTSwapTriggerOrder_018
所属分组
    计划委托
用例标题
    下单区域下止盈止损最优5/10/20档限价单成交测试
前置条件
    在下单区域下单，下限价委托单触发成交
步骤/文本
    1、登录U本位永续界面
    2、选择BTC当周，选择杠杆5X，点击开仓-限价按钮
    3、输入买入价，买入价不要取最新价（如：50000）
    4、输入买入量10张
    5、点击止盈止损按钮
    6、输入止盈价（大于最新价），止损价（低于最新价）
    7、输入卖出价最优5/10/20档，任意一档
    8、点击确认按钮
    9、在下单区域点击买入开多按钮下限价单有结果A
    10、限价单成交后，在当前委托-止盈止损列表查看下单数据有结果B
预期结果
    A)提示下单成功
    B)在当前委托-止盈止损列表有订单，且数值正确，状态显示等待委托
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
@allure.story('下单区域下止盈止损最优5/10/20档限价单成交测试')  # 这里填子功能，没有的话就把本行注释掉
class TestUSDTSwapTriggerOrder_018:

    @allure.step('前置条件')
    def setup(self):
        print(''' 在下单区域下单，下限价委托单触发成交 ''')
        self.contract_code = "BTC-USDT"
        self.current_user = LinearServiceAPI(url=URL2, access_key=ACCESS_KEY, secret_key=SECRET_KEY)

    @allure.title('下单区域下止盈止损最优5/10/20档限价单成交测试')
    @allure.step('测试执行')
    def test_execute(self, symbol):
        with allure.step('1、登录U本位永续界面'):
            # 获取买一价, 如果买一价不存在, 则手动设置买一价为5
            contract_depth = self.current_user.linear_depth(contract_code=self.contract_code, type="step5")
            print("contract_depth is: ", contract_depth)
            bids = contract_depth.get("tick").get("bids")
            if bids:
                current_highest_price = max([i[0] for i in bids])
                highest_price_bid = round(current_highest_price * 1.1, 1)
                tp_trigger_price = highest_price_bid
                sl_trigger_price = round(current_highest_price * 0.9, 1)
                order_price = highest_price_bid
                price = current_highest_price
            else:
                tp_trigger_price = 5
                sl_trigger_price = 4
                price = 5
            order_price_type = "optimal_5"

            r_order_plan = self.current_user.linear_order(contract_code=self.contract_code, price=price, order_price_type="limit", volume=10, direction="buy", offset="open", lever_rate=5, tp_trigger_price=tp_trigger_price, sl_trigger_price=sl_trigger_price,
                                                          tp_order_price_type=order_price_type, sl_order_price_type=order_price_type)
            assert r_order_plan.get("status") == "ok", f"下计划委托单失败: {r_order_plan}"
            tp_sl_order_id = r_order_plan.get("data").get("order_id")
            time.sleep(3)

        with allure.step('2、选择BTC当周，选择杠杆5X，点击开仓-限价按钮'):
            pass
        with allure.step('3、输入买入价，买入价不要取最新价（如：50000）'):
            pass
        with allure.step('4、输入买入量10张'):
            pass
        with allure.step('5、点击止盈止损按钮'):
            pass
        with allure.step('6、输入止盈价（大于最新价），止损价（低于最新价）'):
            pass
        with allure.step('7、输入卖出价最优5/10/20档，任意一档'):
            pass
        with allure.step('8、点击确认按钮'):
            pass
        with allure.step('9、在下单区域点击买入开多按钮下限价单有结果A'):
            pass
        with allure.step('10、限价单成交后，在当前委托-止盈止损列表查看下单数据有结果B'):
            current_tp_sl_orders_before_deal = self.current_user.linear_tpsl_openorders(contract_code=self.contract_code).get("data").get("orders")
            common_user = LinearServiceAPI(url=URL2, access_key=COMMON_ACCESS_KEY, secret_key=COMMON_SECRET_KEY)
            r_common_sell = common_user.linear_order(contract_code=self.contract_code, price=price, volume=10, direction="sell", offset="open", lever_rate=5, order_price_type="limit")
            assert r_common_sell.get("status") == "ok", f"通用账号下卖单失败: {r_common_sell}"
            time.sleep(3)
            current_tp_sl_orders_after_deal = self.current_user.linear_tpsl_openorders(contract_code=self.contract_code).get('data').get("orders")
            new_tp_sl_order = [i for i in current_tp_sl_orders_after_deal if i not in current_tp_sl_orders_before_deal]
            for i in new_tp_sl_order:
                if i.get("tpsl_order_type") == "tp":
                    trigger_type = "ge"
                    trigger_price = tp_trigger_price
                else:
                    trigger_type = "le"
                    trigger_price = sl_trigger_price
                expected_tp_sl_each = {"volume": 10, "direction": "sell", "trigger_price": trigger_price, "trigger_type": trigger_type, "order_price": 0, "status": 2}
                assert common.util.compare_dict(expected_tp_sl_each, i)
        with allure.step("撤单"):
            r_cancel_limit = self.current_user.linear_cancelall(contract_code=self.contract_code)
            assert r_cancel_limit.get("status") == "ok", f"撤单失败: {r_cancel_limit}"

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
