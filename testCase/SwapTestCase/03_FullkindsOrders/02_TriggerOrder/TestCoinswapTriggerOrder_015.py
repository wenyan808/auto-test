#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210918
# @Author : 邱大伟

#script by: lss
用例编号
    TestCoinswapTriggerOrder_015
所属分组
    计划委托
用例标题
    下单区域下止盈止损限价单未成交测试
前置条件
    在下单区域下单，下限价委托单不要触发成交
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
    10、在当前委托-限价委托列表的止盈/止损列点击查看按钮有结果B
预期结果
    A)提示下单成功
    B)弹出止盈止损信息框，显示止盈止损订单，且数值正确，状态显示未生效
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


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('计划委托')  # 这里填功能
@allure.story('下单区域下止盈止损限价单未成交测试')  # 这里填子功能，没有的话就把本行注释掉
class TestCoinswapTriggerOrder_015:

    @allure.step('前置条件')
    def setup(self):
        print(''' 在下单区域下单，下限价委托单不要触发成交 ''')

    @allure.title('下单区域下止盈止损限价单未成交测试')
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
        with allure.step('10、在当前委托-限价委托列表的止盈/止损列点击查看按钮有结果B'):
            swap_open_orders = current_user.swap_openorders(contract_code=contract_code)
            swap_open_orders = [i for i in swap_open_orders.get("data").get('orders') if i.get("order_id") == order_id]
            assert len(swap_open_orders) == 1, f"未成交合约: {swap_open_orders}"
            order_detail = swap_open_orders[0]
            contract_size = current_user.swap_contract_info(contract_code=contract_code).get("data")[0].get("contract_size")
            expected_freeze_balance = Decimal(contract_size) / Decimal(price_buy) / 5 * volume
            expected_info = {"contract_code": contract_code, "volume": volume, "price": price_buy, "order_price_type": order_price_type, "direction": direction, "offset": offset, "lever_rate": lever_rate, "status": 3}
            actual_margin_frozen = order_detail.get("margin_frozen")
            assert common.util.compare_dict(expected_info, order_detail)
            assert abs(Decimal(actual_margin_frozen) - expected_freeze_balance) < 0.0001, f"冻结资产错误, 期望: {expected_freeze_balance}, 实际: {actual_margin_frozen}"
        with allure.step("11. 撤单"):
            r_cancel = current_user.swap_cancel(order_id=order_id, contract_code=contract_code)
            assert r_cancel.get("status") == "ok", f"撤单失败: {r_cancel}"

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
