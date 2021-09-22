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
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest, allure, random, time


@allure.epic('业务线')  # 这里填业务线
@allure.feature('功能')  # 这里填功能
@allure.story('子功能')  # 这里填子功能，没有的话就把本行注释掉
class TestUSDTSwapLimitOrder_010:

	@allure.step('前置条件')
	def setup(self):
		print(''' 初始化环境准备
		1、建议准备两个账户，一个用于初始化环境，一个用于测试下单验证。
		1、建议初始化环境是初始化账户吃掉其他所有买卖挂单，盘口无任何挂单
		2、再根据测试场景进行拿初始化账户进行买一卖一挂单作为对手方
		3、每次完成测试后再还原环境
		4、本次用例场景为无成交下撤单场景 ''')

	@allure.title('对手价卖出开空买盘无数据自动撤单')
	@allure.step('测试执行')
	def test_execute(self, symbol):
		with allure.step('1、盘口无买盘，对手价卖出开空'):
			pass
		with allure.step('2、观察下单是否成功有结果A'):
			pass
		with allure.step('3、观察历史委托-限价委托有结果B'):
			pass
		with allure.step('4、观察资产信息有结果C'):
			pass

	@allure.step('恢复环境')
	def teardown(self):
		print('\n恢复环境操作')

if __name__ == '__main__':
    pytest.main()
