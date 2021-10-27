'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20210916
# @Author : 张广南
	用例Id
		
	所属分组
		限价委托
	用例标题
		最优20档卖出开空买盘无数据自动撤单
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
		1、盘口无买盘，最优20档卖出开空
		2、观察下单是否成功有结果A
		3、观察当前委托-限价委托有结果B
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
		TestCoinswapLimitOrder_016
'''

from common.SwapServiceAPI import t as swap_api
from pprint import pprint
import pytest, allure, random, time

from tool.atp import ATP


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('限价委托')  # 这里填功能
#@allure.story('子功能')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestCoinswapLimitOrder_016:

	@allure.step('前置条件')
	@pytest.fixture(scope='function', autouse=True)
	def setup(self, contract_code):
		print(''' 初始化环境准备
		1、建议准备两个账户，一个用于初始化环境，一个用于测试下单验证。
		1、建议初始化环境是初始化账户吃掉其他所有买卖挂单，盘口无任何挂单
		2、再根据测试场景进行拿初始化账户进行买一卖一挂单作为对手方
		3、每次完成测试后再还原环境
		4、本次用例场景为无成交下撤单场景 ''')
		ATP.cancel_all_types_order()
		time.sleep(1)
		ATP.clean_market()
		time.sleep(1)
		ATP.current_user_make_order(direction='buy')
		ATP.current_user_make_order(direction='sell')
		time.sleep(1)


	@allure.title('最优20档卖出开空买盘无数据自动撤单')
	@allure.step('测试执行')
	def test_execute(self, contract_code):
		leverrate = '5'
		with allure.step('1、盘口无买盘，最优20档卖出开空'):
			r = swap_api.swap_account_info(contract_code=contract_code)
			frozen1 = r['data'][0]['margin_frozen']

			r = swap_api.swap_openorders(contract_code=contract_code, page_index='', page_size='')
			totalsize1 = r['data']['total_size']

			r = swap_api.swap_order(contract_code=contract_code, volume='20', direction='sell', offset='open',
									lever_rate=leverrate, order_price_type='optimal_20')
			pprint(r)

		with allure.step('2、观察下单是否成功有结果A'):
			assert r['err_msg'] == '盘口无数据,请稍后再试'
		with allure.step('3、观察当前委托-限价委托有结果B'):
			time.sleep(2)
			r = swap_api.swap_openorders(contract_code=contract_code, page_index='', page_size='')
			totalsize2 = r['data']['total_size']
			
			assert totalsize2 == totalsize1
		with allure.step('4、观察资产信息有结果C'):
			r = swap_api.swap_account_info(contract_code=contract_code)

			frozen2 = r['data'][0]['margin_frozen']
			assert frozen2 == frozen1

	@allure.step('恢复环境')
	def teardown(self):
		print('\n恢复环境操作')

if __name__ == '__main__':
	pytest.main()
