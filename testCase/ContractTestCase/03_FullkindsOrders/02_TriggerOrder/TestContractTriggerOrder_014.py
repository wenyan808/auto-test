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
from common.ContractServiceAPI import t as contract_api

from pprint import pprint
import pytest
import allure
import time

from tool.atp import ATP


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('计划委托')  # 这里填功能
@allure.story('多个开仓撤单同时撤销')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestContractTriggerOrder_014:

    @allure.step('前置条件')
    def setup(self):
        ATP.cancel_all_types_order()
        print(''' 不要触发，至少2条以上订单 ''')

    @allure.title('全部撤销计划委托订单')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('1、登录交割合约界面'):
            pass
        with allure.step('2、选择BTC当周，选择杠杆5X，点击开仓-计划按钮'):
            contract_type = "this_week"

            # 获取最新价
            current_price = ATP.get_current_price(contract_code=symbol_period)

            pprint("\n前置： 获取合约code\n")
            contract_info = contract_api.contract_contract_info(
                symbol=symbol, contract_type=contract_type).get("data")[0]
            print(contract_info)
            pprint("\n步骤一: 开仓-计划委托单\n")
            contract_code = contract_info["contract_code"]
            direction = "buy"
            volume_1 = 1
            volume_2 = 1
            trigger_price = current_price
            order_price_1 = round(current_price * 1.03, 2)
            order_price_2 = round(current_price * 1.02, 2)
            trigger_type = "ge"
            offset = "open"
            lever_rate = 5
            order_price_type = "limit"
        with allure.step('3、下单至少2条以上订单'):
            resp_plan_buy_1 = contract_api.contract_trigger_order(symbol=symbol, contract_type=contract_type, contract_code=contract_code, trigger_type=trigger_type, trigger_price=trigger_price, order_price=order_price_1, order_price_type=order_price_type, volume=volume_1,
                                                                  direction=direction, offset=offset, lever_rate=lever_rate)
            resp_plan_buy_2 = contract_api.contract_trigger_order(symbol=symbol, contract_type=contract_type, contract_code=contract_code, trigger_type=trigger_type, trigger_price=trigger_price, order_price=order_price_2, order_price_type=order_price_type, volume=volume_2,
                                                                  direction=direction, offset=offset, lever_rate=lever_rate)
            assert resp_plan_buy_1.get(
                "status") == "ok", "下单出错: {res}".format(res=resp_plan_buy_1)
            assert resp_plan_buy_2.get(
                "status") == "ok", "下单出错: {res}".format(res=resp_plan_buy_1)
            order_id_1 = resp_plan_buy_1['data']['order_id']
            order_id_2 = resp_plan_buy_2['data']['order_id']
            time.sleep(5)
        with allure.step('4、检查当前委托-计划委托列表有结果A'):
            res_all_his_orders = contract_api.contract_trigger_openorders(
                symbol=symbol, contract_code=contract_code).get("data").get("orders")
            expected_order_ids = [order_id_1, order_id_2]
            actual_orders = [i for i in res_all_his_orders if i.get(
                "order_id") in expected_order_ids]
            actual_order_ids = [i.get("order_id") for i in actual_orders]
            assert len(actual_orders) == 2, "未找到符合条件的两个订单{expected_order_ids}, 实际订单只有: {actual_order_ids}".format(
                expected_order_ids=expected_order_ids, actual_order_ids=actual_order_ids)
            for i in range(len(actual_order_ids)):
                if actual_order_ids[i] == order_id_1:
                    expected_order_info = {"trigger_type": trigger_type, "volume": volume_1, "lever_rate": lever_rate, "order_price_type": order_price_type, "trigger_price": trigger_price, "contract_code": contract_code, "symbol": symbol,
                                           "contract_type": contract_type, "direction": direction, "offset": offset}
                else:
                    expected_order_info = {"trigger_type": trigger_type, "volume": volume_2, "lever_rate": lever_rate, "order_price_type": order_price_type, "trigger_price": trigger_price, "contract_code": contract_code, "symbol": symbol,
                                           "contract_type": contract_type, "direction": direction, "offset": offset}
                assert common.util.compare_dict(
                    expected_order_info, actual_orders[i])

        with allure.step('5、点击全部撤销按钮弹框选择计划委托类型,点击确定后有结果B'):
            r_cancel = contract_api.contract_trigger_cancel(
                symbol=symbol, order_id=",".join([str(i) for i in actual_order_ids]))
            assert r_cancel.get("status") == "ok"
            assert not r_cancel.get("data").get(
                "errors"), "撤单时，发生错误: {r_cancel}".format(r_cancel=r_cancel)
            time.sleep(3)

        with allure.step('6、检查历史委托-计划委托信息有结果D'):
            res_all_trigger_orders = contract_api.contract_trigger_hisorders(
                symbol=symbol, trade_type=0, contract_code=contract_code, status=0, create_date=7).get("data").get("orders")
            actual_orders = [i for i in res_all_trigger_orders if i.get(
                "order_id") in expected_order_ids]
            actual_order_ids = [i.get("order_id") for i in actual_orders]
            assert len(actual_orders) == 2, "未找到符合条件的两个历史订单{expected_order_ids}, 实际历史订单有: {actual_order_ids}".format(
                expected_order_ids=expected_order_ids, actual_order_ids=actual_order_ids)
            for i in range(len(actual_order_ids)):
                if actual_order_ids[i] == order_id_1:
                    expected_order_info = {"trigger_type": trigger_type, "volume": volume_1, "lever_rate": lever_rate, "order_price_type": order_price_type, "trigger_price": trigger_price, "contract_code": contract_code, "symbol": symbol,
                                           "contract_type": contract_type, "direction": direction, "offset": offset}
                else:
                    expected_order_info = {"trigger_type": trigger_type, "volume": volume_2, "lever_rate": lever_rate, "order_price_type": order_price_type, "trigger_price": trigger_price, "contract_code": contract_code, "symbol": symbol,
                                           "contract_type": contract_type, "direction": direction, "offset": offset}
                assert common.util.compare_dict(
                    expected_order_info, actual_orders[i])

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
