#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210917
# @Author : 
    用例标题
        撤销计划委托订单平仓测试
    前置条件
        不要触发
    步骤/文本
        1、登录交割合约界面
        2、选择BTC当周，选择杠杆5X，点击平仓-计划按钮
        3、输入触发价（如：50000）
        4、输入买入价，偏离最新价不要成交（如：40000）
        5、输入买入量10张
        6、点击买入平空按钮后弹框确认后有结果A
        7、查看当前委托列表中的计划委托有结果B
        8、点击撤销按钮有结果C
        9、检查历史委托-计划委托界面有结果D
    预期结果
        A)提示下单成功
        B)在当前委托-计划委托统计数量+1，列表数量+1,展示合约交易类型，委托类型，倍数，时间，委托数量，委托价信息和下单数值一致
        C)提示撤销申请成功，当前委托-计划委托列表订单消失
        D)在历史委托-计划委托中有撤销订单记录，且各项信息和下单数据一致
    优先级
        0
    用例别名
        TestContractTriggerOrder_013
"""
import datetime

from common.ContractServiceAPI import t as contract_api, ContractServiceAPI
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order
import common.util
from pprint import pprint
import pytest, allure, random, time

from config.conf import URL, LSS_ACCESS_KEY, LSS_SECRET_KEY


@allure.epic('交割')  # 这里填业务线
@allure.feature('计划委托')  # 这里填功能
@allure.story('平仓撤单')  # 这里填子功能，没有的话就把本行注释掉
class TestContractTriggerOrder_013:

    @allure.step('前置条件')
    def setup(self):
        pass

    @allure.title('撤销计划委托订单平仓测试')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('1、登录交割合约界面'):
            c = ContractServiceAPI(url=URL, access_key=LSS_ACCESS_KEY, secret_key=LSS_SECRET_KEY)
        with allure.step('2、选择BTC当周，选择杠杆5X，点击平仓-计划按钮'):
            contract_ltc_info = c.contract_contract_info(symbol=symbol).get("data")
            contract_type = "this_week"
            contract_code = [i.get("contract_code") for i in contract_ltc_info if i.get("contract_type") == contract_type][0]
            lever_rate = 5
            offset = "close"
        with allure.step('3、输入触发价（如：50000）'):
            #     获取最新价
            r_contract_trade = c.contract_trade(symbol=symbol_period)
            data_r_tract_trade = r_contract_trade.get("tick").get("data")
            last_price = float(data_r_tract_trade[0].get("price"))
            trigger_price = last_price
        with allure.step('4、输入买入价，偏离最新价不要成交（如：40000）'):
            direction = "buy"
            order_price = round(last_price * 1.1, 1)
            trigger_type = "ge"

        with allure.step('5、输入买入量10张'):
            volume = 10
        with allure.step('6、点击买入平空按钮后弹框确认后有结果A'):
            order_price_type = "limit"
            resp_plan_buy = c.contract_trigger_order(symbol=symbol, contract_type=contract_type, contract_code=contract_code, trigger_type=trigger_type, trigger_price=trigger_price, order_price=order_price, order_price_type=order_price_type, volume=volume,
                                                     direction=direction, offset=offset, lever_rate=lever_rate)
            time.sleep(3)
        with allure.step('7、查看当前委托列表中的计划委托有结果B'):
            assert resp_plan_buy.get("status") == "ok", "下单出错: {res}".format(res=resp_plan_buy)
            order_id = resp_plan_buy['data']['order_id']
            time.sleep(5)
            res_all_his_orders = c.contract_trigger_openorders(symbol=symbol, contract_code=contract_code).get("data").get("orders")
            order_created = False
            for r in res_all_his_orders:
                if r.get("order_id") == order_id:
                    expected_did = {"trigger_type": trigger_type, "volume": volume, "lever_rate": lever_rate, "order_price_type": order_price_type, "trigger_price": trigger_price, "contract_code": contract_code, "symbol": symbol,
                                    "contract_type": contract_type, "direction": direction, "offset": offset}
                    assert common.util.compare_dict(expected_did, r)
                    order_created = True
                    break
        with allure.step('8、点击撤销按钮有结果C'):
            if order_created:
                r_cancel = c.contract_trigger_cancel(symbol=symbol, order_id=order_id)
                assert r_cancel.get("status") == "ok"
                assert not r_cancel.get("data").get("errors"), "撤单时，发生错误: {r_cancel}".format(r_cancel=r_cancel)
                time.sleep(3)
            else:
                raise BaseException("在{res_all_his_orders}中未找到历史订单含有订单号: {order_id}".format(res_all_his_orders=res_all_his_orders, order_id=order_id))
        with allure.step('9、检查历史委托-计划委托界面有结果D'):
            res_all_orders = c.contract_trigger_hisorders(symbol=symbol, trade_type=0, contract_code=contract_code, status=0, create_date=7).get("data").get("orders")
            expected_dic = {"symbol": symbol, "order_price_type": order_price_type, "trigger_price": trigger_price, "lever_rate": lever_rate, "volume": volume, "order_price": order_price, "status": 6}
            for r in res_all_orders:
                if r.get("order_id") == order_id:
                    assert common.util.compare_dict(expected_dic, r)
                    created_time = datetime.datetime.fromtimestamp(r.get("created_at") / 1000)
                    now = datetime.datetime.now()
                    assert (now + datetime.timedelta(seconds=180) >= created_time >= now) or (created_time + datetime.timedelta(seconds=180) >= now >= created_time), "时间过长对不上(时间差超过180s)"
                    return
            raise BaseException("在历史订单：{res_all_orders}中未找到订单号: {order_id}".format(res_all_orders=res_all_orders, order_id=order_id))


    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
