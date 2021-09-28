#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210918
# @Author : 邱大伟

#script by: lss
用例编号
    TestCoinswapTriggerOrder_016
所属分组
    计划委托
用例标题
    下单区域下止盈止损限价单成交测试
前置条件
    在下单区域下单，下限价委托单触发成交
步骤/文本
    1、登录币本位永续界面
    2、选择BTC/USD，选择杠杆5X，点击开仓-限价按钮
    3、输入买入价，买入价不要取最新价（如：50000）
    4、输入买入量10张
    5、点击止盈止损按钮
    6、输入止盈价（大于最新价），止损价（低于最新价）
    7、输入卖出价（如：55000，大于最新价）
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


@allure.epic('所属分组')  # 这里填业务线
@allure.feature('计划委托')  # 这里填功能
@allure.story('下单区域下止盈止损限价单成交测试')  # 这里填子功能，没有的话就把本行注释掉
class TestCoinswapTriggerOrder_016:

    @allure.step('前置条件')
    def setup(self):
        print(''' 在下单区域下单，下限价委托单触发成交 ''')

    @allure.title('下单区域下止盈止损限价单成交测试')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step("0、判断盘口有无数据，么有的话，挂一个买单"):
            contract_code = "EOS-USD"
            current_user = SwapService(url=URL, access_key=ACCESS_KEY, secret_key=SECRET_KEY)
            print("步骤一(0): 为了不要成交，找出卖盘的最低价, 并以低于卖1价的价格下单")
            r_trend_req = current_user.swap_depth(contract_code=contract_code, type="step5")
            asks = r_trend_req.get("tick").get("asks", None)
            bids = r_trend_req.get("tick").get("bids", None)
            common_user = SwapService(url=URL, access_key=COMMON_ACCESS_KEY, secret_key=COMMON_SECRET_KEY)
            if asks and bids:
                lowest_price = min([i[0] for i in asks])
            else:
                lowest_price = 5
                r_common_temp_buy = common_user.swap_order(contract_code=contract_code, price=round(lowest_price*0.9, 1), volume=1, direction="buy", offset="open", lever_rate=5, order_price_type="limit")
                assert r_common_temp_buy.get("status") == "ok", f"造盘口(买)失败: {r_common_temp_buy}"
                r_common_temp_sell = common_user.swap_order(contract_code=contract_code, price=lowest_price, volume=1, direction="sell", offset="open", lever_rate=5, order_price_type="limit")
                assert r_common_temp_sell.get("status") == "ok", f"造盘口(卖)失败: {r_common_temp_sell}"
                time.sleep(3)
        with allure.step('1、登录币本位永续界面'):
            price_buy = round(lowest_price * 0.9, 1)
            latest_swap_trade = current_user.swap_trade(contract_code=contract_code)
            print("步骤一(1): 获取最新价")
            data_r_swap_trade = latest_swap_trade.get("tick").get("data")
            last_price = float(data_r_swap_trade[0].get("price"))
            volume = 10
            direction = "buy"
            offset = "open"
            lever_rate = 5
            order_price_type = "limit"
            tp_trigger_price = round(last_price * 1.1, 1)
            # 止损价必须低于开仓价
            sl_trigger_price = round(price_buy * 0.9, 1)
            tp_order_price = tp_trigger_price
            sl_order_price = tp_order_price
            req_tp_sl_order = current_user.swap_order(contract_code=contract_code, price=price_buy, volume=volume, direction=direction, offset=offset, lever_rate=lever_rate, order_price_type=order_price_type, tp_trigger_price=tp_trigger_price, sl_trigger_price=sl_trigger_price,
                                                      tp_order_price=tp_order_price, sl_order_price=sl_order_price)
            time.sleep(3)
        with allure.step('2、选择BTC/USD，选择杠杆5X，点击开仓-限价按钮'):
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
            assert req_tp_sl_order.get("status") == "ok", f"下单失败: {req_tp_sl_order}"
            order_id = req_tp_sl_order.get("data").get("order_id")
        with allure.step('10.0、获取成交前的止盈止损单'):
            tp_sl_orders_before_deal = current_user.swap_tpsl_openorders(contract_code=contract_code).get("data").get("orders")
        with allure.step('10.1、限价单成交后，在当前委托-止盈止损列表查看下单数据有结果B'):
            common_user = SwapService(url=URL, access_key=COMMON_ACCESS_KEY, secret_key=COMMON_SECRET_KEY)
            r_temp_sell = common_user.swap_order(contract_code=contract_code, direction="sell", price=price_buy, volume=volume, offset=offset, lever_rate=lever_rate, order_price_type=order_price_type)
            assert r_temp_sell.get("status") == "ok", f"用通用账号下卖单失败: {r_temp_sell}"
            time.sleep(3)
            tp_sl_orders_after_deal = current_user.swap_tpsl_openorders(contract_code=contract_code).get("data").get("orders")
            new_tp_sl_orders = [o for o in tp_sl_orders_after_deal if o not in tp_sl_orders_before_deal]
            tp_sl_direction = "sell"
            assert len(new_tp_sl_orders) == 2, f"止盈止损下单数量错误, 期望2条，实际: {new_tp_sl_orders}"
            for o in new_tp_sl_orders:
                if o.get("tpsl_order_type") == "sl":
                    trigger_type = "le"
                    order_price = sl_order_price
                    trigger_price = sl_trigger_price
                else:
                    trigger_type = "ge"
                    order_price = tp_order_price
                    trigger_price = tp_trigger_price
                expected_info = {"contract_code": contract_code, "volume": volume, "order_type": 1, "direction": tp_sl_direction, "trigger_type": trigger_type, "order_price": order_price, "trigger_price": trigger_price, "status": 2}
                assert common.util.compare_dict(expected_info, o)
        with allure.step("撤掉止盈止损单"):
            r_cancel = current_user.swap_tpsl_cancelall(contract_code=contract_code)
            assert r_cancel.get("status") == "ok", f"撤止盈止损单失败: {r_cancel}"

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
