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
@pytest.mark.stable
class TestContractTriggerOrder_003:
    def setUp(self):
        self.oder_id = None
        self.symbol = None

    @allure.title('{title}')
    def test_contract_account_position_info(self, symbol):
        """ 计划委托最优5挡开仓测试 """
        self.symbol = symbol
        pprint("\n前置： 获取合约code\n")
        contract_ltc_info = contract_api.contract_contract_info(symbol=symbol).get("data")
        pprint("\n步骤一: 开仓-计划委托单\n")
        contract_type = "this_week"
        contract_code = [i.get("contract_code") for i in contract_ltc_info if i.get("contract_type") == contract_type][0]
        direction = "buy"
        volume = 1
        trigger_type = "le"
        trigger_price = 1
        order_price = 1
        offset = "open"
        lever_rate = 5
        order_price_type = "optimal_5"
        resp_plan_buy = contract_api.contract_trigger_order(symbol=symbol, contract_type=contract_type, contract_code=contract_code, trigger_type=trigger_type, trigger_price=trigger_price, order_price=order_price, order_price_type=order_price_type, volume=volume,
                                                            direction=direction, offset=offset, lever_rate=lever_rate)
        assert resp_plan_buy.get("status") == "ok"
        self.order_id = resp_plan_buy.get("data").get("order_id")
        time.sleep(5)
        pprint("\n步骤二: 查询所有当前委托单存在刚才下的单，并且数据校验正确\n")
        res_all_his_orders = contract_api.contract_trigger_openorders(symbol=symbol, contract_code=contract_code).get("data").get("orders")
        for r in res_all_his_orders:
            if r.get("order_id") == self.order_id:
                # 因为用的是最优五档，所以order_price已经没有意义，不需要再校验(后端返回的order_price默认是0)
                expected_did = {"trigger_type": trigger_type, "volume": volume, "lever_rate": lever_rate, "order_price_type": order_price_type, "trigger_price": trigger_price, "contract_code": contract_code, "symbol": symbol,
                                "contract_type": contract_type, "direction": direction, "offset": offset}
                assert common.util.compare_dict(expected_did, r)
                return
        raise BaseException("在{res_all_his_orders}中未找到历史订单含有订单号: {order_id}".format(res_all_his_orders=res_all_his_orders, order_id=self.order_id))

    @allure.step('恢复环境')
    def teardown(self):
        r_cancel = contract_api.contract_cancel(symbol=self.symbol, order_id=self.order_id)
        assert r_cancel.get("status") == "ok", f"撤单失败: r{r_cancel}"


if __name__ == '__main__':
    pytest.main()
