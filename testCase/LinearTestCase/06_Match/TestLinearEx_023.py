#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/10/18
# @Author  : Alex Li
"""
所属分组
    合约测试基线用例//03 正向永续//06 撮合//委托单
用例标题
    撮合 only_maker 买入 平仓     
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


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('撮合//委托单')  # 这里填功能
@allure.story('撮合 only_maker 买入 平仓')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestLinearEx_023:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, contract_code):
        print("前置条件  {}".format(contract_code))

        ATP.make_market_depth()

    @allure.title('撮合 only_maker 买入 平仓')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('1、 撮合 only_maker 卖出 开仓'):
            pass
        with allure.step('2、点击“确定按钮”'):

            # 先买入，才能卖出
            current = ATP.get_current_price(contract_code=contract_code)
            offset = 'open'
            direction = 'sell'
            order_price_type = "post_only"
            res = ATP.current_user_make_order(order_price_type=order_price_type, contract_code=contract_code,
                                              price=current, volume=10, direction=direction, offset=offset)
            pprint(res)
            assert res['status'] == 'ok', "撮合失败！"
           # 撮合成交
            ATP.common_user_make_order(
                price=current, direction='buy', offset=offset)
            time.sleep(1)
            # 买入 平仓
            current1 = ATP.get_current_price(contract_code=contract_code)
            offset1 = 'close'
            direction1 = 'buy'
            res1 = ATP.current_user_make_order(order_price_type=order_price_type, contract_code=contract_code,
                                               price=current1, volume=10, direction=direction1, offset=offset1)
            pprint(res1)

            assert res1['status'] == 'ok', "撮合失败！"

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        
        # 撤销当前用户 某个品种所有限价挂单
        print(ATP.cancel_all_types_order())
        print('\n恢复环境操作结束')


if __name__ == '__main__':
    pytest.main()
