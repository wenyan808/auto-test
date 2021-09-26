#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : lss
import common.util
from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order

from schema import Schema, And, Or, Regex, SchemaError
from pprint import pprint
import pytest, allure, random, time
from tool.get_test_data import case_data


@allure.epic('反向交割')
@allure.feature('')
class TestContractTriggerOrder_002:
    def setUp(self):
        print('\n')

    @allure.title('{title}')
    def test_contract_account_position_info(self, symbol):
        """ 计划委托正常限价平仓测试 """
        self.setUp()

        pprint("\n前置： 获取合约code\n")
        contract_ltc_info = contract_api.contract_contract_info(symbol=symbol).get("data")

        pprint("\n步骤一: 平仓-计划委托单\n")

        contract_type = "this_week"
        contract_code = [i.get("contract_code") for i in contract_ltc_info if i.get("contract_type") == contract_type][0]
        direction = "buy"
        volume = 1
        trigger_type = "le"
        trigger_price = 1
        order_price = 1
        offset = "close"
        lever_rate = 5
        order_price_type = "limit"
        resp_plan_buy = contract_api.contract_trigger_order(symbol=symbol, contract_type=contract_type, contract_code=contract_code, trigger_type=trigger_type, trigger_price=trigger_price, order_price=order_price, order_price_type=order_price_type, volume=volume,
                                                            direction=direction, offset=offset, lever_rate=lever_rate)
        assert resp_plan_buy.get("status") == "ok"
        order_id = resp_plan_buy.get("data").get("order_id")
        time.sleep(5)
        pprint("\n步骤二: 查询所有当前委托单存在刚才下的单，并且数据校验正确\n")
        res_all_his_orders = contract_api.contract_trigger_openorders(symbol=symbol, contract_code=contract_code).get("data").get("orders")
        for r in res_all_his_orders:
            if r.get("order_id") == order_id:
                expected_did = {"trigger_type": trigger_type, "volume": volume, "lever_rate": lever_rate, "order_price_type": order_price_type, "trigger_price": trigger_price, "order_price": order_price, "contract_code": contract_code, "symbol": symbol,
                                "contract_type": contract_type, "direction": direction, "offset": offset}
                assert common.util.compare_dict(expected_did, r)
                pprint("\n步骤三: 撤单\n")
                r_cancel = contract_api.contract_cancel(symbol=symbol, order_id=order_id)
                assert r_cancel.get("status") == "ok", f"撤单失败: r{r_cancel}"
                return
        raise BaseException("在{res_all_his_orders}中未找到历史订单含有订单号: {order_id}".format(res_all_his_orders=res_all_his_orders, order_id=order_id))


if __name__ == '__main__':
    pytest.main()
