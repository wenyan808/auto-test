#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210923
# @Author : 邱大伟

#script by: lss
用例编号
    TestUSDTSwapTriggerOrder_015
所属分组
    计划委托
用例标题
    下单区域下止盈止损限价单未成交测试
前置条件
    在下单区域下单，下限价委托单不要触发成交
步骤/文本
    1、登录U本位永续界面
    2、选择BTC当周，选择杠杆5X，点击开仓-限价按钮
    3、输入买入价，买入价不要取最新价（如：50000）
    4、输入买入量10张
    5、点击止盈止损按钮
    6、输入止盈价（大于最新价），止损价（低于最新价）
    7、输入卖出价（如：55000，大于最新价）
    8、点击确认按钮
    9、在下单区域点击买入开多按钮下限价单有结果A
    10、在当前委托-限价委托列表的止盈/止损列点击查看按钮有结果B
预期结果
    A)提示下单成功
    B)弹出止盈止损信息框，显示止盈止损订单，且数值正确，状态显示未生效
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
@allure.story('下单区域下止盈止损限价单未成交测试')  # 这里填子功能，没有的话就把本行注释掉
class TestUSDTSwapTriggerOrder_015:

    @allure.step('前置条件')
    def setup(self):
        print(''' 在下单区域下单，下限价委托单不要触发成交 ''')
        self.contract_code = "BTC-USDT"
        self.current_user = LinearServiceAPI(url=URL2, access_key=ACCESS_KEY, secret_key=SECRET_KEY)

    @allure.title('下单区域下止盈止损限价单未成交测试')
    @allure.step('测试执行')
    def test_execute(self, symbol):
        with allure.step('1、登录U本位永续界面'):
            # 获取买一价, 如果买一价不存在, 则手动设置买一价为5
            contract_depth = self.current_user.linear_depth(contract_code=self.contract_code, type="step5")
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
                order_price = 5

            r_order_plan = self.current_user.linear_order(contract_code=self.contract_code, price=price, order_price_type="limit", volume=10, direction="buy", offset="open", lever_rate=5, tp_trigger_price=tp_trigger_price, sl_trigger_price=sl_trigger_price,
                                                          tp_order_price=order_price, sl_order_price=order_price)
            assert r_order_plan.get("status") == "ok", f"下计划委托单失败: {r_order_plan}"
            self.tp_sl_order_id = r_order_plan.get("data").get("order_id")
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
        with allure.step('7、输入卖出价（如：55000，大于最新价）'):
            pass
        with allure.step('8、点击确认按钮'):
            pass
        with allure.step('9、在下单区域点击买入开多按钮下限价单有结果A'):
            pass
        with allure.step('10、在当前委托-限价委托列表的止盈/止损列点击查看按钮有结果B'):
            tp_sl_actual = self.current_user.linear_relation_tpsl_order(contract_code=self.contract_code, order_id=self.tp_sl_order_id).get("data")
            expected_tp_sl_info = {"contract_code": self.contract_code, "volume": 10, "price": price, "order_price_type": "limit", "direction": "buy", "offset": "open"}
            assert common.util.compare_dict(expected_tp_sl_info, tp_sl_actual)
            tp_sl_detail_actual = tp_sl_actual.get("tpsl_order_info")
            for i in tp_sl_detail_actual:
                if i.get("tpsl_order_type") == "tp":
                    trigger_type = "ge"
                    trigger_price = tp_trigger_price
                else:
                    trigger_type = "le"
                    trigger_price = sl_trigger_price
                expected_tp_sl_each = {"volume": 10, "direction": "sell", "trigger_price": trigger_price, "trigger_type": trigger_type, "order_price": order_price, "status": 1}
                assert common.util.compare_dict(expected_tp_sl_each, i)

    @allure.step('恢复环境')
    def teardown(self):
        r_cancel = self.current_user.linear_cancel(contract_code=self.contract_code, order_id=self.tp_sl_order_id)
        assert r_cancel.get("status") == "ok", f"撤单失败: {r_cancel}"


if __name__ == '__main__':
    pytest.main()
