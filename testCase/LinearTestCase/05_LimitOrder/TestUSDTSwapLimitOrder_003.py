'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20210917
# @Author : 
	用例Id
		
	所属分组
		限价委托
	用例标题
		只做maker 买入开多下单后自动撤单测试
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
		1、下单只做maker 买入开多，设置的挂单价格盘口已存在
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
		TestUSDTSwapLimitOrder_003
'''

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order
from common.util import compare_dict
from pprint import pprint
import pytest, allure, random, time


@allure.epic('业务线')  # 这里填业务线
@allure.feature('功能')  # 这里填功能
@allure.story('子功能')  # 这里填子功能，没有的话就把本行注释掉
class TestUSDTSwapLimitOrder_003:

	@allure.step('前置条件')
	def setup(self):
		print(''' 初始化环境准备
		1、建议准备两个账户，一个用于初始化环境，一个用于测试下单验证。
		1、建议初始化环境是初始化账户吃掉其他所有买卖挂单，盘口无任何挂单
		2、再根据测试场景进行拿初始化账户进行买一卖一挂单作为对手方
		3、每次完成测试后再还原环境
		4、本次用例场景为无成交下撤单场景 ''')

	@allure.title('只做maker 买入开多下单后自动撤单测试')
	@allure.step('测试执行')
	def test_execute(self, contract_code):
		""" 只做maker 买入开多下单后自动撤单测试 """
		lever_rate = 5
		self.setup()
		print('\n步骤一:获取盘口卖一价\n')
		r_trend_req = linear_api.linear_depth(contract_code=contract_code, type="step5")
		pprint(r_trend_req)
		data_r_trade_res = r_trend_req.get("tick").get("asks")

		assert len(data_r_trade_res) > 0, "盘口(卖出盘)无数据"
		lowest_price_sell = min([i[0] for i in data_r_trade_res])
		with allure.step('1、下单只做maker 买入开多，设置的挂单价格盘口已存在'):
			order_price_type = "post_only"
			r_order_buy = linear_api.linear_order(contract_code=contract_code,
									client_order_id='',
									price=lowest_price_sell,
									volume='1',
									direction='buy',
									offset='open',
									lever_rate=lever_rate,
									order_price_type=order_price_type)
			pprint(r_order_buy)
			current_time = int(str(time.time()).split(".")[0])
			time.sleep(2)
		with allure.step('2、观察下单是否成功有结果A'):
			generated_order_id = r_order_buy['data']['order_id']
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
										 "price": lowest_price_sell}
					actual_time_from_query = int(str(order.get("create_date"))[0:10])
					assert (actual_time_from_query - current_time) <= 180, "时间不一致, 限价单%d创建时间: %s, 查询到的时间: %s" % (
					generated_order_id, current_time, actual_time_from_query)
					# assert compare_dict(expected_info_dic, order)
					return
			raise BaseException(
				"在{all_order_ids}中未找到历史订单含有订单号: {generated_order_id}".format(all_order_ids=all_order_ids,
																			 generated_order_id=generated_order_id))

		with allure.step(''):
			pass

	@allure.step('恢复环境')
	def teardown(self):
		print('\n恢复环境操作')

if __name__ == '__main__':
    pytest.main()
