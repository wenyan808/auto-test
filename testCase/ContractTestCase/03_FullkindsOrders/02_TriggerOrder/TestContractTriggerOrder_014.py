#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210917
# @Author : lss
    用例标题
        全部撤销计划委托订单
    前置条件
        不要触发，至少2条以上订单
    步骤/文本
        1、登录交割合约界面
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
    优先级
        0
    用例别名
        TestContractTriggerOrder_014
"""
import common.util
from common.ContractServiceAPI import t as contract_api, ContractServiceAPI
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest, allure, random, time

from config.conf import URL, SECRET_KEY, ACCESS_KEY


@allure.epic('交割')  # 这里填业务线
@allure.feature('计划委托')  # 这里填功能
@allure.story('多个开仓撤单同时撤销')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestContractTriggerOrder_014:

    @allure.step('前置条件')
    def setup(self):
        print(''' 不要触发，至少2条以上订单 ''')

    @allure.title('全部撤销计划委托订单')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('1、登录交割合约界面'):
            pass
        with allure.step('2、选择BTC当周，选择杠杆5X，点击开仓-计划按钮'):
            c = ContractServiceAPI(url=URL, access_key=ACCESS_KEY, secret_key=SECRET_KEY)
            #     获取最新价
            r_contract_trade = c.contract_trade(symbol=symbol_period)
            data_r_tract_trade = r_contract_trade.get("tick").get("data")
            last_price = float(data_r_tract_trade[0].get("price"))
            pprint("\n前置： 获取合约code\n")
            contract_ltc_info = c.contract_contract_info(symbol=symbol).get("data")
            pprint("\n步骤一: 开仓-计划委托单\n")
            contract_type = "this_week"
            contract_code = [i.get("contract_code") for i in contract_ltc_info if i.get("contract_type") == contract_type][0]
            direction = "buy"
            volume_1 = 10
            volume_2 = 1
            trigger_price = last_price
            order_price_1 = round(last_price * 1.1, 1)
            order_price_2 = round(last_price * 1.2, 1)
            trigger_type = "ge"
            offset = "open"
            lever_rate = 5
            order_price_type = "limit"
        with allure.step('3、下单至少2条以上订单'):
            resp_plan_buy_1 = c.contract_trigger_order(symbol=symbol, contract_type=contract_type, contract_code=contract_code, trigger_type=trigger_type, trigger_price=trigger_price, order_price=order_price_1, order_price_type=order_price_type, volume=volume_1,
                                                       direction=direction, offset=offset, lever_rate=lever_rate)
            resp_plan_buy_2 = c.contract_trigger_order(symbol=symbol, contract_type=contract_type, contract_code=contract_code, trigger_type=trigger_type, trigger_price=trigger_price, order_price=order_price_2, order_price_type=order_price_type, volume=volume_2,
                                                       direction=direction, offset=offset, lever_rate=lever_rate)
            assert resp_plan_buy_1.get("status") == "ok", "下单出错: {res}".format(res=resp_plan_buy_1)
            assert resp_plan_buy_2.get("status") == "ok", "下单出错: {res}".format(res=resp_plan_buy_1)
            order_id_1 = resp_plan_buy_1['data']['order_id']
            order_id_2 = resp_plan_buy_2['data']['order_id']
            time.sleep(5)
        with allure.step('4、检查当前委托-计划委托列表有结果A'):
            res_all_his_orders = c.contract_trigger_openorders(symbol=symbol, contract_code=contract_code).get("data").get("orders")
            expected_order_ids = [order_id_1, order_id_2]
            actual_orders = [i for i in res_all_his_orders if i.get("order_id") in expected_order_ids]
            actual_order_ids = [i.get("order_id") for i in actual_orders]
            assert len(actual_orders) == 2, "未找到符合条件的两个订单{expected_order_ids}, 实际订单只有: {actual_order_ids}".format(expected_order_ids=expected_order_ids, actual_order_ids=actual_order_ids)
            for i in range(len(actual_order_ids)):
                if actual_order_ids[i] == order_id_1:
                    expected_order_info = {"trigger_type": trigger_type, "volume": volume_1, "lever_rate": lever_rate, "order_price_type": order_price_type, "trigger_price": trigger_price, "contract_code": contract_code, "symbol": symbol,
                                           "contract_type": contract_type, "direction": direction, "offset": offset}
                else:
                    expected_order_info = {"trigger_type": trigger_type, "volume": volume_2, "lever_rate": lever_rate, "order_price_type": order_price_type, "trigger_price": trigger_price, "contract_code": contract_code, "symbol": symbol,
                                           "contract_type": contract_type, "direction": direction, "offset": offset}
                assert common.util.compare_dict(expected_order_info, actual_orders[i])

        with allure.step('5、点击全部撤销按钮弹框选择计划委托类型,点击确定后有结果B'):
            r_cancel = c.contract_trigger_cancel(symbol=symbol, order_id=",".join([str(i) for i in actual_order_ids]))
            assert r_cancel.get("status") == "ok"
            assert not r_cancel.get("data").get("errors"), "撤单时，发生错误: {r_cancel}".format(r_cancel=r_cancel)
            time.sleep(3)
        with allure.step('6、检查当前委托-计划委托信息有结果C'):
            current_contract_open_orders = c.contract_openorders(symbol=symbol)
            uncanceled_contract_open_orders = current_contract_open_orders.get("data").get("orders")
            assert not uncanceled_contract_open_orders, "订单取消成功后, 在当前委托里订单{uncanceled_contract_open_orders}未消失!".format(uncanceled_contract_open_orders=uncanceled_contract_open_orders)
        with allure.step('7、检查历史委托-计划委托信息有结果D'):
            res_all_trigger_orders = c.contract_trigger_hisorders(symbol=symbol, trade_type=0, contract_code=contract_code, status=0, create_date=7).get("data").get("orders")
            actual_orders = [i for i in res_all_trigger_orders if i.get("order_id") in expected_order_ids]
            actual_order_ids = [i.get("order_id") for i in actual_orders]
            assert len(actual_orders) == 2, "未找到符合条件的两个历史订单{expected_order_ids}, 实际历史订单有: {actual_order_ids}".format(expected_order_ids=expected_order_ids, actual_order_ids=actual_order_ids)
            for i in range(len(actual_order_ids)):
                if actual_order_ids[i] == order_id_1:
                    expected_order_info = {"trigger_type": trigger_type, "volume": volume_1, "lever_rate": lever_rate, "order_price_type": order_price_type, "trigger_price": trigger_price, "contract_code": contract_code, "symbol": symbol,
                                           "contract_type": contract_type, "direction": direction, "offset": offset}
                else:
                    expected_order_info = {"trigger_type": trigger_type, "volume": volume_2, "lever_rate": lever_rate, "order_price_type": order_price_type, "trigger_price": trigger_price, "contract_code": contract_code, "symbol": symbol,
                                           "contract_type": contract_type, "direction": direction, "offset": offset}
                assert common.util.compare_dict(expected_order_info, actual_orders[i])

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
