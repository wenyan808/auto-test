#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211018
# @Author : chenwei
    用例标题
        restful请求聚合行情 不传合约代码(日期格式)
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        返回合约代码必填
    优先级
        2
    用例别名
        TestContractNoti_restful_detail_007
"""

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
class TestContractNoti_restful_detail_007:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('restful请求聚合行情 不传合约代码(日期格式)')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('详见官方文档'):
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
