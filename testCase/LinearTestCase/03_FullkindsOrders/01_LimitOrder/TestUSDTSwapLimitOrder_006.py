'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20210917
# @Author : chenwei
	用例Id
		
	所属分组
		限价委托
	用例标题
		IOC卖出开空下单后自动撤单测试
	前置条件
		初始化环境准备
		1、建议准备两个账户，一个用于初始化环境，一个用于测试下单验证。
		1、建议初始化环境是初始化账户吃掉其他所有买卖挂单，盘口无任何挂单
		2、再根据测试场景进行拿初始化账户进行买一卖一挂单作为对手方
		3、每次完成测试后再还原环境
		4、本次用例场景为无成交下撤单场景
	类型
		文本
	步骤/文本
		1、下单IOC卖出开空 ，设置价格低于卖一价
		2、观察下单是否成功有结果A
		3、观察历史委托-限价委托有结果B
		4、观察资产信息有结果C
	预期结果
		A)系统会自动取消下单
		B)历史委托-限价委托最新数据展示的为刚撤单信息，信息置灰，状态为已撤销，列表信息展示合约，倍数，交易类型，委托类型，时间，委托数量，委托价信息和下单数值一致
		C)无冻结担保资产
		
		
	标签
		P0
	优先级
		0
	用例别名
		TestUSDTSwapLimitOrder_006
'''

from pprint import pprint

import allure
import pytest
import time

from common.LinearServiceAPI import t as linear_api
from common.util import compare_dict
from tool.atp import ATP


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('功能')  # 这里填功能
@allure.story('子功能')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestUSDTSwapLimitOrder_006:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, contract_code):
        print(''' 初始化环境准备
		1、建议准备两个账户，一个用于初始化环境，一个用于测试下单验证。
		1、建议初始化环境是初始化账户吃掉其他所有买卖挂单，盘口无任何挂单
		2、再根据测试场景进行拿初始化账户进行买一卖一挂单作为对手方
		3、每次完成测试后再还原环境
		4、本次用例场景为无成交下撤单场景 ''')
        # 撤销当前用户 某个品种所有限价挂单
        ATP.cancel_all_order(contract_code=contract_code)
        # 修改当前品种杠杆 默认5倍
        ATP.switch_level(contract_code=contract_code)
        # 清除盘口所有卖单
        ATP.clean_market(contract_code=contract_code, direction='sell')
        # 清除盘口所有买单
        ATP.clean_market(contract_code=contract_code, direction='buy')

    @allure.title('IOC卖出开空下单后自动撤单测试')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        self.contract_code = contract_code
        self.orderid1 = 0
        self.orderid2 = 0
        lever_rate = 5
        r = linear_api.linear_history_trade(contract_code=contract_code, size='1')
        pprint(r)
        # 得到最近的价格
        lastprice = r['data'][0]['data'][0]['price']
        lastprice = round((lastprice * 0.99), 2)
        # 挂一个买单
        r = linear_api.linear_order(contract_code=contract_code,
                                    client_order_id='',
                                    price=lastprice,
                                    volume='2',
                                    direction='buy',
                                    offset='open',
                                    lever_rate=lever_rate,
                                    order_price_type='limit')
        pprint(r)
        time.sleep(1)
        print('\n步骤一:获取盘口买一价\n')
        r_trend_req = linear_api.linear_depth(contract_code=contract_code, type="step5")
        pprint(r_trend_req)
        data_r_trade_res = r_trend_req.get("tick").get("bids")
        assert len(data_r_trade_res) > 0, "盘口(买入盘)无数据"
        highest_price_buy = max([i[0] for i in data_r_trade_res])
        with allure.step('1、下单IOC卖出开空 ，设置价格低于卖一价'):
            order_price_type = "ioc"
            higher_price = round((highest_price_buy * 1.1), 1)
            r_order_sell = linear_api.linear_order(contract_code=contract_code,
                                                   client_order_id='',
                                                   price=higher_price,
                                                   volume='1',
                                                   direction='sell',
                                                   offset='open',
                                                   lever_rate=lever_rate,
                                                   order_price_type=order_price_type)
            pprint(r_order_sell)
        with allure.step('2、观察下单是否成功有结果A'):
            current_time = int(str(time.time()).split(".")[0])
            pprint(r_order_sell)
            generated_order_id = r_order_sell['data']['order_id']
            time.sleep(4)
        with allure.step('3、观察历史委托-限价委托有结果B'):
            history_orders = linear_api.linear_hisorders(contract_code=contract_code, trade_type=0, type=1, status=0,
                                                         create_date=7)
            pprint(history_orders)
            all_orders = history_orders.get("data").get("orders")
            all_order_ids = [i.get("order_id") for i in all_orders]
        with allure.step('4、观察资产信息有结果C'):
            for order in all_orders:
                current_order_id = order.get("order_id")
                if current_order_id == generated_order_id:
                    expected_info_dic = {"status": 7, "lever_rate": 5, "order_type": 1, "volume": 1,
                                         "price": higher_price}
                    actual_time_from_query = int(str(order.get("create_date"))[0:10])
                    assert (actual_time_from_query - current_time) <= 180, "时间不一致, 限价单%d创建时间: %s, 查询到的时间: %s" % (
                        generated_order_id, current_time, actual_time_from_query)
                    assert compare_dict(expected_info_dic, order)
                    return
            raise BaseException(
                "在{all_order_ids}中未找到历史订单含有订单号: {generated_order_id}".format(all_order_ids=all_order_ids,
                                                                             generated_order_id=generated_order_id))

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_order()


if __name__ == '__main__':
    pytest.main()
