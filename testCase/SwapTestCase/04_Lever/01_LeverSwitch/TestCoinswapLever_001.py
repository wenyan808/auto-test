'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20210916
# @Author : 
	用例Id
		
	所属分组
		杠杆
	用例标题
		当前无挂单切换杠杆倍数测试
	前置条件
		1、用户在该业务线下已开户
		2、用户在合约下没有任何挂单
		
	类型
		文本
	步骤/文本
		1、在交割合约交易页，选择BTC/USD合约
		2、观察杠杆倍数指示按钮有结果A
		3、点击杠杆切换按钮有结果B
		4、在杠杆滑动条上，点击30X后再点击"确定"按钮有结果C
		5、将杠杆倍数切换为任意值
	预期结果
		A)杠杆倍数显示正常(如:5X)
		B)弹起杠杆切换框，杠杆滑动条停留在当前杠杆倍数的位置（如：5X）
		C)杠杆倍数切换为30X，杠杆切换框消失，杠杆切换icon上杠杆倍数显示为30X，杠杆切换成功
	标签
		P0
	优先级
		0
	用例别名
		TestCoinswapLever_001
'''

from common.SwapServiceAPI import t as swap_api
from pprint import pprint
import pytest, allure, random, time


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('杠杆')  # 这里填功能
@allure.story('杠杆调节')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestCoinswapLever_001:

	@allure.step('前置条件')
	@pytest.fixture(scope='function', autouse=True)
	def setup(self, contract_code):
		print(''' 1、用户在该业务线下已开户
		2、用户在合约下没有任何挂单
		 ''')
		r = swap_api.swap_cancelall(contract_code=contract_code)
		pprint(r)
		r = swap_api.swap_tpsl_cancelall(contract_code=contract_code)
		pprint(r)
		r = swap_api.swap_trigger_cancelall(contract_code=contract_code)
		pprint(r)
		r = swap_api.swap_cancelall(contract_code=contract_code)
		pprint(r)
		time.sleep(2)

	@allure.title('当前无挂单切换杠杆倍数测试')
	@allure.step('测试执行')
	def test_execute(self, contract_code):
		with allure.step('1、在交割合约交易页，选择BTC/USD合约'):
			pass
		with allure.step('2、观察杠杆倍数指示按钮有结果A'):
			r = swap_api.swap_available_level_rate(contract_code=contract_code)
			availableleverlist = r['data'][0]['available_level_rate'].split(',')
			time.sleep(0.1)
		with allure.step('3、点击杠杆切换按钮有结果B'):
			pass
		with allure.step('4、在杠杆滑动条上，点击30X后再点击"确定"按钮有结果C'):
			pass
		with allure.step('5、将杠杆倍数切换为任意值'):
			i = random.choice(availableleverlist)
			r = swap_api.swap_switch_lever_rate(contract_code=contract_code, lever_rate=i)
			pprint(r)
			assert r['status'] == 'ok'

	@allure.step('恢复环境')
	def teardown(self):
		print('\n恢复环境操作')

if __name__ == '__main__':
	pytest.main()
