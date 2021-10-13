'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20210916
# @Author : chenwei
	用例Id
		
	所属分组
		限价委托
	用例标题
		限价委托输入价格下单卖出开空后撤单测试
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
		1、卖出开空限价手动输入价格高于买一价
		2、观察盘口有结果A
		3、观察当前委托-限价委托页面有结果B
		4、观察资产信息有结果C
		5、在当前委托-限价委托点击撤单
		6、观察历史委托-限价委托有结果D
		7、观察资产信息有结果E
	预期结果
		A)订单未成交，盘口卖方展示挂单数据
		B)当前委托-限价委托统计数量+1，列表数量+1,展示合约交易类型，委托类型，倍数，时间，委托数量，委托价信息和下单数值一致
		C)资产信息冻结相应资产
		D)撤单后，历史委托-限价委托最新数据展示的为刚撤单信息，信息置灰，状态为已撤销，列表信息展示合约交易类型，委托类型倍数，时间，委托数量，委托价信息
		E)释放冻结担保资产
		
	标签
		P0
	优先级
		0
	用例别名
		TestCoinswapLimitOrder_002
'''

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest, allure, random, time
from tool.atp import ATP

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('功能')  # 这里填功能
@allure.story('子功能')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestCoinswapLimitOrder_002:

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

	@allure.title('限价委托输入价格下单卖出开空后撤单测试')
	@allure.step('测试执行')
	def test_execute(self, contract_code):
		flag = True
		leverrate = '5'
		print('\n获取最近价\n')
		r = swap_api.swap_history_trade(contract_code=contract_code, size='1')
		pprint(r)
		# 得到最近的价格
		lastprice1 = r['data'][0]['data'][0]['price']
		lastprice = round((lastprice1 * 0.99), 2)
		print('\n下一个买单\n')
		r = swap_api.swap_order(contract_code=contract_code,
									client_order_id='',
									price=lastprice,
									volume='1',
									direction='buy',
									offset='open',
									lever_rate=leverrate,
									order_price_type='limit')
		pprint(r)
		orderid1 = r['data']['order_id']  # 890261793653673984
		time.sleep(2)
		"""获取当前冻结保证金"""
		r = swap_api.swap_account_info(contract_code=contract_code)
		pprint(r)
		frozen1 = r['data'][0]['margin_frozen']  # 15832.73774
		time.sleep(2)
		"""获取当前委托数量及详情"""
		r = swap_api.swap_openorders(contract_code=contract_code, page_index='', page_size='')
		totalsize1 = r['data']['total_size']
		pprint(totalsize1)
		with allure.step('1、卖出开空限价手动输入价格高于买一价'):
			# 生成一个卖出开空下单价(高于买一价)
			orderprice = round((lastprice1 * 1.01), 2)
			# 卖出开空限价下单
			r = swap_api.swap_order(contract_code=contract_code,
										client_order_id='',
										price=orderprice,
										volume='1',
										direction='sell',
										offset='open',
										lever_rate=leverrate,
										order_price_type='limit')
			pprint(r)
			time.sleep(4)
			orderid2 = r['data']['order_id']  # 890261795566276608
		with allure.step('2、观察盘口有结果A'):
			"""获取当前冻结保证金"""
			r = swap_api.swap_account_info(contract_code=contract_code)
			pprint(r)
			frozen2 = r['data'][0]['margin_frozen']  # 15832.9633
			if frozen2 <= frozen1:
				print("冻结资金没有增加，不符合预期")
				flag = False
				assert frozen2 >= frozen1
			time.sleep(2)
		with allure.step('3、观察当前委托-限价委托页面有结果B'):
			"""获取当前委托数量及详情"""
			r = swap_api.swap_openorders(contract_code=contract_code, page_index='', page_size='')
			totalsize2 = r['data']['total_size']
			actual_orderinfo = r['data']['orders'][0]
		with allure.step('4、观察资产信息有结果C'):
			pprint(totalsize1)
			pprint(totalsize2)
			if totalsize2 - totalsize1 != 1:
				print("当前委托数量增量不为1，不符合预期")
				flag = False
				print(actual_orderinfo)
		with allure.step('5、在当前委托-限价委托点击撤单'):
			print('\n撤掉刚才下的买入单\n')
			r = swap_api.swap_cancel(order_id=orderid2, contract_code=contract_code)
			time.sleep(1)
		with allure.step('6、观察历史委托-限价委托有结果D'):
			"""获取历史订单"""
			r = swap_api.swap_hisorders_exact(contract_code=contract_code, trade_type='1', type='2', status='7')
			actual_orderinfo2 = r['data']['orders'][0]
		with allure.step('7、观察资产信息有结果E'):
			"""获取当前冻结保证金"""
			r = swap_api.swap_account_info(contract_code=contract_code)
			pprint(r)
			frozen3 = r['data'][0]['margin_frozen']  # 15821.46
			if frozen3 != frozen1:
				print("冻结资金没有恢复到初始状态，不符合预期")
				flag = False
			print('\n恢复环境:撤单\n')
			# 回撤卖单
			r = swap_api.swap_cancel(contract_code=contract_code, order_id=orderid1)
			pprint(r)
			assert flag == True

	@allure.step('恢复环境')
	def teardown(self):
		print('\n恢复环境操作')

if __name__ == '__main__':
    pytest.main()
