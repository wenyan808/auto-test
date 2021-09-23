'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20210916
# @Author : 
	用例Id
		
	所属分组
		限价委托
	用例标题
		限价委托输入价格下单买入开多后撤单测试
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
		1、买入开多限价手动输入价格低于卖一价
		2、观察盘口有结果A
		3、观察当前委托-限价委托页面有结果B
		4、观察资产信息有结果C
		5、在当前委托-限价委托点击撤单
		6、观察历史委托-限价委托有结果D
		7、观察资产信息有结果E
	预期结果
		A)订单未成交，盘口买方展示挂单数据
		B)当前委托-限价委托统计数量+1，列表数量+1,展示合约交易类型，委托类型，倍数，时间，委托数量，委托价信息和下单数值一致
		C)资产信息冻结相应资产
		D)撤单后，历史委托-限价委托最新数据展示的为刚撤单信息，信息置灰，状态为已撤销，列表信息展示合约交易类型，委托类型倍数，时间，委托数量，委托价信息
		E)释放冻结担保资产
		
	标签
		P0
	优先级
		0
	用例别名
		TestCoinswapLimitOrder_001
'''

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest, allure, random, time


@allure.epic('业务线')  # 这里填业务线
@allure.feature('功能')  # 这里填功能
@allure.story('子功能')  # 这里填子功能，没有的话就把本行注释掉
class TestCoinswapLimitOrder_001:

	@allure.step('前置条件')
	def setup(self):
		print(''' 初始化环境准备
		1、建议准备两个账户，一个用于初始化环境，一个用于测试下单验证。
		1、建议初始化环境是初始化账户吃掉其他所有买卖挂单，盘口无任何挂单
		2、再根据测试场景进行拿初始化账户进行买一卖一挂单作为对手方
		3、每次完成测试后再还原环境
		4、本次用例场景为无成交下撤单场景 ''')

	@allure.title('限价委托输入价格下单买入开多后撤单测试')
	@allure.step('测试执行')
	def test_execute(self, symbol):
		with allure.step('1、买入开多限价手动输入价格低于卖一价'):
			pass
		with allure.step('2、观察盘口有结果A'):
			pass
		with allure.step('3、观察当前委托-限价委托页面有结果B'):
			pass
		with allure.step('4、观察资产信息有结果C'):
			pass
		with allure.step('5、在当前委托-限价委托点击撤单'):
			pass
		with allure.step('6、观察历史委托-限价委托有结果D'):
			pass
		with allure.step('7、观察资产信息有结果E'):
			pass

	@allure.step('恢复环境')
	def teardown(self):
		print('\n恢复环境操作')

if __name__ == '__main__':
    pytest.main()
