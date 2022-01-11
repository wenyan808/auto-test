#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210917
# @Author : lss
用例标题
    下单区域下止盈止损最优5/10/20档限价单成交测试
前置条件
    在下单区域下单，下限价委托单触发成交
步骤/文本
    1、登录交割合约界面
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
优先级
    0
用例别名
    TestContractTriggerOrder_018
"""

import common.util
from common.ContractServiceAPI import t as contract_api
from common.ContractServiceAPI import ContractServiceAPI
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest
import allure
import random
import time

from config.conf import URL, ACCESS_KEY, SECRET_KEY, COMMON_ACCESS_KEY, COMMON_SECRET_KEY


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('止盈止损')  # 这里填功能
@allure.story('下单区域下止盈止损最优5/10/20档限价单成交测试')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestContractTriggerOrder_018:

    @allure.step('前置条件')
    def setup(self):
        print(''' 在下单区域下单，下限价委托单触发成交 ''')
        self.symbol = None
        self.contract_code = None

    @allure.title('下单区域下止盈止损最优5/10/20档限价单成交测试')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('1、登录交割合约界面'):
            self.symbol = symbol
            self.current_user = ContractServiceAPI(
                url=URL, access_key=ACCESS_KEY, secret_key=SECRET_KEY)
            self.common_user = ContractServiceAPI(
                url=URL, access_key=COMMON_ACCESS_KEY, secret_key=COMMON_SECRET_KEY)
            #     获取最新价
            r_contract_trade = self.current_user.contract_trade(
                symbol=symbol_period)
            data_r_tract_trade = r_contract_trade.get("tick").get("data")
            contract_ltc_info = self.current_user.contract_contract_info(
                symbol=symbol).get("data")
            last_price = float(data_r_tract_trade[0].get("price"))
            # 开仓价
            open_price = round(last_price * 0.99, 1)
            # 止盈触发价
            tp_trigger_price = round(last_price * 1.01, 1)
            # 止盈委托价
            tp_order_price = tp_trigger_price
            # 止盈类型
            tp_sl_order_price_type = "optimal_5"
            # 止损触发价
            sl_trigger_price = round(open_price * 0.99, 1)
            # 止损委托价
            sl_order_price = sl_trigger_price
            # 止损类型
            pprint("\n前置： 获取合约code\n")
            contract_type = "this_week"
            self.contract_code = [i.get("contract_code") for i in contract_ltc_info if i.get(
                "contract_type") == contract_type][0]
            volume = 10
            direction = "buy"
            offset = "open"
            lever_rate = 5
            order_price_type = "limit"
            r_contract_order = self.current_user.contract_order(symbol=symbol, contract_type=contract_type, contract_code=self.contract_code, price=open_price, volume=volume, direction=direction, offset=offset, lever_rate=lever_rate, order_price_type=order_price_type,
                                                                tp_trigger_price=tp_trigger_price, tp_order_price=tp_order_price, tp_order_price_type=tp_sl_order_price_type, sl_trigger_price=sl_trigger_price, sl_order_price=sl_order_price, sl_order_price_type=tp_sl_order_price_type)
            assert r_contract_order.get("status") == "ok", "下单失败: {r_contract_order}".format(
                r_contract_order=r_contract_order)
            order_id = r_contract_order.get("data").get("order_id")
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
            time.sleep(3)
            r_contract_order_history_data = self.current_user.contract_relation_tpsl_order(
                symbol=symbol, order_id=order_id).get("data")
            # 获取成交之前的止盈止损单
            before_deal_contract_tpsl_openorders = self.current_user.contract_tpsl_openorders(
                symbol=symbol, contract_code=self.contract_code).get("data").get("orders")
        with allure.step('10、限价单成交后，在当前委托-止盈止损列表查看下单数据有结果B'):
            expected_info = {"symbol": symbol, "contract_code": self.contract_code, "contract_type": contract_type, "volume": volume,
                             "price": open_price, "order_price_type": order_price_type, "direction": direction, "offset": offset, "lever_rate": lever_rate}
            assert common.util.compare_dict(
                expected_info, r_contract_order_history_data)
            direction_tp_sl = "sell"
            expected_tp_info = {"volume": volume, "direction": direction_tp_sl, "tpsl_order_type": "tp", "trigger_type": "ge",
                                "trigger_price": tp_trigger_price, "order_price": 0, "order_price_type": tp_sl_order_price_type, "status": 1}
            expected_sl_info = {"volume": volume, "direction": direction_tp_sl, "tpsl_order_type": "sl", "trigger_type": "le",
                                "trigger_price": sl_trigger_price, "order_price": 0, "order_price_type": tp_sl_order_price_type, "status": 1}
            for tp_sl in r_contract_order_history_data.get("tpsl_order_info"):
                if tp_sl.get("tpsl_order_type") == "tp":
                    assert common.util.compare_dict(expected_tp_info, tp_sl)
                else:
                    assert common.util.compare_dict(expected_sl_info, tp_sl)
        with allure.step("11、做一个卖单促成成交"):
            res_sell = self.common_user.contract_order(symbol=symbol, contract_type=contract_type, contract_code=self.contract_code,
                                                       price=open_price, volume=volume, direction="sell", offset="open", lever_rate=lever_rate, order_price_type="limit")
            assert res_sell.get("status") == "ok", "下开仓卖单失败: {res_sell}".format(
                res_sell=res_sell)
            time.sleep(5)
        with allure.step("12. 检查止盈止损单状态"):
            after_contract_tpsl_openorders = self.current_user.contract_tpsl_openorders(
                symbol=symbol, contract_code=self.contract_code).get('data').get('orders')
            new_orders = [
                o for o in after_contract_tpsl_openorders if o not in before_deal_contract_tpsl_openorders]
            after_deal_expected_tp_info = {"volume": volume, "direction": direction_tp_sl, "tpsl_order_type": "tp", "trigger_type": "ge",
                                           "trigger_price": tp_trigger_price, "order_price": 0, "order_price_type": tp_sl_order_price_type, "status": 2}
            after_deal_expected_sl_info = {"volume": volume, "direction": direction_tp_sl, "tpsl_order_type": "sl", "trigger_type": "le",
                                           "trigger_price": sl_trigger_price, "order_price": 0, "order_price_type": tp_sl_order_price_type, "status": 2}
            for tp_sl in new_orders:
                if tp_sl.get("tpsl_order_type") == "tp":
                    assert common.util.compare_dict(
                        after_deal_expected_tp_info, tp_sl)
                else:
                    assert common.util.compare_dict(
                        after_deal_expected_sl_info, tp_sl)

    @allure.step('恢复环境')
    def teardown(self):
        r_cancel_all = self.current_user.contract_tpsl_cancelall(
            symbol=self.symbol, contract_code=self.contract_code)
        assert r_cancel_all.get('status') == "ok", "撤单失败"


if __name__ == '__main__':
    pytest.main()
