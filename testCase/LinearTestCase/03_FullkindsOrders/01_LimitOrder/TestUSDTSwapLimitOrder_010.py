'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20210917
# @Author : 
	用例Id
		
	所属分组
		限价委托
	用例标题
		对手价卖出开空买盘无数据自动撤单
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
		1、盘口无买盘，对手价卖出开空
		2、观察下单是否成功有结果A
		3、观察历史委托-限价委托有结果B
		4、观察资产信息有结果C
	预期结果
		A)订单未成交，盘口卖方不展示挂单数据
		B)当前委托-限价委托统计数量无变化
		C)无冻结担保资产
		
		
	标签
		P0
	优先级
		0
	用例别名
		TestUSDTSwapLimitOrder_010
'''

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api,LinearServiceAPI
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order
from config.conf import COMMON_ACCESS_KEY, COMMON_SECRET_KEY, URL
from pprint import pprint
import pytest, allure, random, time
from tool.atp import ATP

@allure.epic('正向永续')  # 这里填业务线
@allure.feature('功能')  # 这里填功能
@allure.story('子功能')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestUSDTSwapLimitOrder_010:

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

	@allure.title('对手价卖出开空买盘无数据自动撤单')
	@allure.step('测试执行')
	def test_execute(self, contract_code):
		self.contract_code = contract_code;
		self.orderid1 = 0;
		self.orderid2 = 0;
		lever_rate = 5
		r = linear_api.linear_history_trade(contract_code=contract_code, size='1')
		pprint(r)
		# 得到最近的价格
		lastprice = r['data'][0]['data'][0]['price']
		lastprice = round((lastprice * 0.98), 2)
		#挂一个买单
		r = linear_api.linear_order(contract_code=contract_code,
											  client_order_id='',
											  price=lastprice,
											  volume='1',
											  direction='buy',
											  offset='open',
											  lever_rate=lever_rate,
											  order_price_type="limit")
		time.sleep(3)
		pprint('\n步骤一:获取盘口(买)\n')
		r_trend_req = linear_api.linear_depth(contract_code=contract_code, type="step0")
		pprint(r_trend_req)
		current_bids = r_trend_req.get("tick").get("bids")
		# 如果有买单，则吃掉所有买单;如果没有，则不需要吃盘，直接卖出
		if current_bids:
			total_bids = 0
			lowest_price = []
			for each_bids in current_bids:
				each_price, each_amount = each_bids[0], each_bids[1]
				total_bids += each_amount
				lowest_price.append(each_price)
			lowest_price = min(lowest_price)
			pprint("\n步骤二：用操作账号以当前最低价吃掉所有买单(卖出)\n")
			# service = LinearServiceAPI(URL, COMMON_ACCESS_KEY, COMMON_SECRET_KEY)
			r = linear_api.linear_order(contract_code=contract_code,
										client_order_id='',
										price=lowest_price,
										volume=total_bids,
										direction='sell',
										offset='open',
										lever_rate=lever_rate,
										order_price_type='limit')
			pprint(r)
			time.sleep(3)
			pprint("\n步骤三：再次查询盘口，确认是否已吃掉所有买单\n")
			r_trend_req_confirm = linear_api.linear_depth(contract_code=contract_code, type="step0")
			current_bids = r_trend_req_confirm.get("tick").get("bids")
			assert not current_bids, "买盘不为空! 当前买盘: {current_bids}".format(current_bids=current_bids)
		with allure.step('1、盘口无买盘，对手价卖出开空'):
			r_sell_opponent = linear_api.linear_order(contract_code=contract_code,
									 client_order_id='',
									 price="",
									 volume=1,
									 direction='sell',
									 offset='open',
									 lever_rate=lever_rate,
									 order_price_type='opponent')
		with allure.step('2、观察下单是否成功有结果A'):
			actual_status = r_sell_opponent.get("status")
			actual_msg = r_sell_opponent.get("err_msg")
			assert actual_status == 'error' and actual_msg == "对手价不存在", "预期: `error`+`对手价不存在`, 实际: `{actual_status}+{actual_msg}`".format(
				actual_status=actual_status, actual_msg=actual_msg)
		with allure.step('3、观察历史委托-限价委托有结果B'):
			pass
		with allure.step('4、观察资产信息有结果C'):
			pass

	@allure.step('恢复环境')
	def teardown(self):
		print('\n恢复环境操作')
		r = linear_api.linear_cancel(contract_code=self.contract_code, order_id=self.orderid1)
		pprint(r)
		time.sleep(1)
		r = linear_api.linear_cancel(contract_code=self.contract_code, order_id=self.orderid2)
		pprint(r)

if __name__ == '__main__':
	pytest.main()
