#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : lss
import datetime

import common.util
from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.ContractServiceAPI import ContractServiceAPI
from config.conf import *
from schema import Schema, And, Or, Regex, SchemaError
from pprint import pprint
import pytest, allure, random, time
from tool.get_test_data import case_data


@allure.epic('反向交割')
@allure.feature('')
class TestContractTriggerOrder_0012:

    def setUp(self):
        pass

    @allure.title('{title}')
    def test_contract_account_position_info(self, symbol, symbol_period):
        """ 撤销计划委托订单开仓测试 """
        self.setUp()
        c = ContractServiceAPI(url=URL, access_key=LSS_ACCESS_KEY, secret_key=LSS_SECRET_KEY)
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
        volume = 10

        trigger_price = last_price
        order_price = round(last_price * 1.1, 1)
        trigger_type = "ge"
        offset = "open"
        lever_rate = 5
        order_price_type = "limit"
        resp_plan_buy = c.contract_trigger_order(symbol=symbol, contract_type=contract_type, contract_code=contract_code, trigger_type=trigger_type, trigger_price=trigger_price, order_price=order_price, order_price_type=order_price_type, volume=volume,
                                                 direction=direction, offset=offset, lever_rate=lever_rate)
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
        if order_created:
            print("步骤二： 撤销计划委托订单")
            r_cancel = c.contract_trigger_cancel(symbol=symbol, order_id=order_id)
            assert r_cancel.get("status") == "ok"
            assert not r_cancel.get("data").get("errors"), "撤单时，发生错误: {r_cancel}".format(r_cancel=r_cancel)
            time.sleep(3)
            """
            symbol	             True    String	品种代码	"BTC","ETH"...
            contract_code	     false   String	合约代码,"BTC180914" ...
            trade_type	         true	 number	交易类型		0:全部,1:买入开多,2: 卖出开空,3: 买入平空,4: 卖出平多；后台是根据该值转换为offset和direction，然后去查询的； 其他值无法查询出结果
            status	             true	 String	订单状态		多个以英文逗号隔开，计划委托单状态：0:全部（表示全部结束状态的订单）、4:已委托、5:委托失败、6:已撤单
            create_date        	 true	 number	日期		可随意输入正整数，如果参数超过90则默认查询90天的数据
            """
            res_all_orders = c.contract_trigger_hisorders(symbol=symbol, trade_type=0, contract_code=contract_code, status=0, create_date=7).get("data").get("orders")
            print("步骤三: 确认订单存在历史订单中且是已撤销状态")
            expected_dic = {"symbol": symbol, "order_price_type": order_price_type, "trigger_price": trigger_price, "lever_rate": lever_rate, "volume": volume, "order_price": order_price, "status": 6}
            for r in res_all_orders:
                if r.get("order_id") == order_id:
                    assert common.util.compare_dict(expected_dic, r)
                    created_time = datetime.datetime.fromtimestamp(r.get("created_at") / 1000)
                    now = datetime.datetime.now()
                    assert (now + datetime.timedelta(seconds=180) >= created_time >= now) or (created_time + datetime.timedelta(seconds=180) >= now >= created_time), "时间过长对不上(时间差超过180s)"
                    return
            raise BaseException("在历史订单：{res_all_orders}中未找到订单号: {order_id}".format(res_all_orders=res_all_orders, order_id=order_id))
        else:
            raise BaseException("在{res_all_his_orders}中未找到历史订单含有订单号: {order_id}".format(res_all_his_orders=res_all_his_orders, order_id=order_id))


if __name__ == '__main__':
    pytest.main()
