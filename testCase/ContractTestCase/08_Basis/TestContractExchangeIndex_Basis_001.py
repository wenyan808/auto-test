#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211012
# @Author : chenwei
    用例标题
        查询基差1min K线
    前置条件
        
    步骤/文本
        参考官方文档
    预期结果
        180条数据,K线不间断,最后一根是当前时间
    优先级
        0
    用例别名
        TestContractExchangeIndex_Basis_001
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest, allure, random, time
from tool.atp import ATP
from common.ContractServiceWS import t as contract_service_ws


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('功能')  # 这里填功能
@allure.story('子功能')  # 这里填子功能，没有的话就把本行注释掉

class TestContractExchangeIndex_Basis_001:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print(''' 初始化环境准备
    	1、建议准备两个账户，一个用于初始化环境，一个用于测试下单验证。
    	1、建议初始化环境是初始化账户吃掉其他所有买卖挂单，盘口无任何挂单
    	2、再根据测试场景进行拿初始化账户进行买一卖一挂单作为对手方
    	3、每次完成测试后再还原环境
    	4、本次用例场景为无成交下撤单场景 ''')
        # 撤销当前用户 某个品种所有限价挂单
        ATP.cancel_all_order(contract_code=symbol)
        # 修改当前品种杠杆 默认5倍
        ATP.switch_level(contract_code=symbol)
        # 清除盘口所有卖单
        ATP.clean_market(contract_code=symbol, direction='sell')
        # 清除盘口所有买单
        ATP.clean_market(contract_code=symbol, direction='buy')

    @allure.title('查询基差1min K线')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('参考官方文档'):
            peroid = "1min"
            r = contract_service_ws.contract_sub_index(symbol_period,peroid)
            pprint(r)
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.clean_market()


if __name__ == '__main__':
    pytest.main()
