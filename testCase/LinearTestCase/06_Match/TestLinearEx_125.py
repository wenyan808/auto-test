#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/10/18
# @Author  : Alex Li
"""
所属分组
    合约测试基线用例//03 正向永续//06 撮合//委托单
用例标题
    撮合 闪电平仓最优30档 卖出
前置条件

步骤/文本
    详见官方文档

预期结果
    正确撮合
优先级
    0
"""

import time
from pprint import pprint
import pytest
import allure
from tool.atp import ATP
from common.LinearServiceAPI import t as linear_api


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('撮合//委托单')  # 这里填功能
@allure.story('撮合 闪电平仓最优30档 卖出')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestLinearEx_125:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, contract_code):
        print("前置条件  {}".format(contract_code))

        ATP.make_market_depth()

    @allure.title('撮合 闪电平仓最优30档 卖出')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('1、撮合 闪电平仓最优30档 卖出'):
            pass
        with allure.step('2、点击“确定按钮”'):
            current = ATP.get_current_price(contract_code=contract_code)

            ATP.common_user_make_order(
                contract_code=contract_code, price=current, volume=10, direction='sell', offset='open')
            # time.sleep(1)

            res = ATP.current_user_make_order(
                contract_code=contract_code, price=current, volume=10, direction='buy', offset='open')
            pprint(res)

            pprint(linear_api.linear_account_position_info(
                contract_code=contract_code))

            direction = 'sell'
            order_price_type = 'lightning'
            res = linear_api.linear_lightning_close_position(
                contract_code=contract_code, volume=10, direction=direction, order_price_type=order_price_type)
            pprint(res)
            assert res['status'] == 'ok', "撮合失败！"

    @ allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        
        # 撤销当前用户 某个品种所有限价挂单
        print(ATP.cancel_all_types_order())


if __name__ == '__main__':
    pytest.main()
