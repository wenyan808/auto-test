'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20210916
# @Author : chenwei
	用例Id
		
	所属分组
		限价委托
	用例标题
		对手价买入开多卖盘无数据自动撤单
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
		1、盘口无卖盘，对手价买入开多
		2、观察下单是否成功有结果A
		3、观察历史委托-限价委托有结果B
		4、观察资产信息有结果C
	预期结果
		A)订单未成交，盘口买方不展示挂单数据
		B)当前委托-限价委托统计数量无变化
		C)无冻结担保资产
		
		
	标签
		P0
	优先级
		0
	用例别名
		TestCoinswapLimitOrder_009
'''

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api, SwapService
from common.SwapServiceOrder import t as swap_order
from config.conf import COMMON_ACCESS_KEY, COMMON_SECRET_KEY, URL

from pprint import pprint
import pytest, allure, random, time
from tool.atp import ATP

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('功能')  # 这里填功能
@allure.story('子功能')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestCoinswapLimitOrder_009:

	@allure.step('前置条件')
	def setup(self):
		print(''' 初始化环境准备
		1、建议准备两个账户，一个用于初始化环境，一个用于测试下单验证。
		1、建议初始化环境是初始化账户吃掉其他所有买卖挂单，盘口无任何挂单
		2、再根据测试场景进行拿初始化账户进行买一卖一挂单作为对手方
		3、每次完成测试后再还原环境
		4、本次用例场景为无成交下撤单场景 ''')
		# 撤销当前用户 某个品种所有限价挂单
		ATP.cancel_all_order()
		time.sleep(1)
		# 修改当前品种杠杆 默认5倍
		ATP.switch_level()
		# 清除盘口所有卖单
		ATP.clean_market()
		time.sleep(1)
		ATP.current_user_make_order(direction='buy')
		ATP.current_user_make_order(direction='sell')
		time.sleep(1)


	@allure.title('对手价买入开多卖盘无数据自动撤单')
	@allure.step('测试执行')
	def test_execute(self, contract_code):
		""" 对手价买入开多卖盘无数据以对手价买入会报对手价不存在 """
		lever_rate = 5
		pprint("得到最近的价格")
		r = swap_api.swap_history_trade(contract_code=contract_code, size='1')
		pprint(r)
		pprint('\n步骤一:获取盘口(卖)\n')
		r_trend_req = swap_api.swap_depth(contract_code=contract_code, type="step0")
		pprint(r_trend_req)
		current_asks = r_trend_req.get("tick").get("asks")
		# 如果有卖单，则吃掉所有卖单
		if current_asks:
			total_asks = 0
			highest_price = 0
			for each_ask in current_asks:
				each_price, each_amount = each_ask[0], each_ask[1]
				total_asks += each_amount
				# highest_price = max(highest_price, each_price)
				pprint("\n步骤二：用操作账号以当前最高价吃掉(买入)所有卖单\n")
				service = SwapService(URL, COMMON_ACCESS_KEY, COMMON_SECRET_KEY)
				pprint(each_price)
				r = service.swap_order(contract_code=contract_code,
										client_order_id='',
										price=round((each_price * 1.01), 2),
										volume=total_asks,
										direction='buy',
										offset='open',
										lever_rate=lever_rate,
										order_price_type='limit')
				pprint(r)
				time.sleep(1)
			pprint("\n步骤三：再次查询盘口，确认是否已吃掉所有卖单\n")
			r_trend_req_confirm = swap_api.swap_depth(contract_code=contract_code, type="step0")
			pprint(r_trend_req_confirm)
			current_asks = r_trend_req_confirm.get("tick").get("asks")
			assert not current_asks, "卖盘不为空! 当前卖盘: {current_asks}".format(current_asks=current_asks)
		with allure.step('1、盘口无卖盘，对手价买入开多'):
			# 买入开多限价
			r_buy_opponent = swap_api.swap_order(contract_code=contract_code,
													 client_order_id='',
													 price="",
													 volume='1',
													 direction='buy',
													 offset='open',
													 lever_rate=lever_rate,
													 order_price_type='opponent')
			pprint(r_buy_opponent)
		with allure.step('2、观察下单是否成功有结果A'):
			time.sleep(2)
			err_code = r_buy_opponent.get("err_code")
			assert err_code == 1016
		with allure.step('3、观察历史委托-限价委托有结果B'):
			r = swap_api.swap_openorders(contract_code=contract_code, page_index='', page_size='')
			pprint(r)
			totalsize2 = r['data']['total_size']
			assert totalsize2 ==0
		with allure.step('4、观察资产信息有结果C'):
			pass

	@allure.step('恢复环境')
	def teardown(self):
		print('\n恢复环境操作')
		ATP.cancel_all_order()

if __name__ == '__main__':
	pytest.main()
