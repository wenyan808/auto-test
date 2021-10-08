#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211008
# @Author : Donglin Han

所属分组
    合约测试基线用例//02 反向永续//03 全部策略订单//02 计划委托//正常限价平仓
用例标题
    计划委托买入平空触发价大于最新价
前置条件
    
步骤/文本
    1、登录合约交易系统
    2、选择币种BTC，选择杠杆5X，点击平仓-计划按钮
    3、输入触发价（如：50000，最新价：49999）
    4、输入买入价（如：45000）
    5、输入买入量10张
    6、点击买入平空按钮，弹框点击确认
预期结果
    A)提示下单成功
    B)当前委托-计划委托列表查询创建订单
优先级
    1
用例编号
    TestSwapTriggerCloseBuy_004
自动化作者
    韩东林
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order
from common.SwapServiceAPI import common_user_swap_service_api
from pprint import pprint
import pytest, allure, random, time


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('合约测试基线用例//02 反向永续//03 全部策略订单//02 计划委托//正常限价平仓')  # 这里填功能
@allure.story('计划委托买入平空触发价大于最新价')  # 这里填子功能，没有的话就把本行注释掉
class TestSwapTriggerCloseBuy_004:

    @allure.step('前置条件')
    def setup(self, contract_code):
        print(''' 使当前交易对有交易盘口  ''')
        print(''' 使当前用户有持仓  ''')

    @allure.title('计划委托买入平空触发价大于最新价')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('1、登录合约交易系统'):
            pass
        with allure.step('2、选择币种BTC，选择杠杆5X，点击平仓-计划按钮'):
            pass
        with allure.step('3、输入触发价（如：50000，最新价：49999）'):
            pass
        with allure.step('4、输入买入价（如：45000）'):
            pass
        with allure.step('5、输入买入量10张'):
            pass
        with allure.step('6、点击买入平空按钮，弹框点击确认'):
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
