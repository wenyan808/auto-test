#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/10/18
# @Author  : Alex Li
"""
所属分组
    合约测试基线用例//03 正向永续//06 撮合//委托单
用例标题
    撮合 卖出平仓部分成交 撤单     
前置条件
    
步骤/文本
    详见官方文档

预期结果
    正确撮合
优先级
    0
"""
from common.LinearServiceAPI import t as linear_api
from pprint import pprint
import pytest
import allure
from tool.atp import ATP


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('撮合//委托单')  # 这里填功能
@allure.story('撮合 卖出平仓部分成交 撤单  ')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestLinearEx_076:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, contract_code):
        print("前置条件  {}".format(contract_code))

    @allure.title('撮合 卖出平仓部分成交 撤单  ')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('1、 撮合 卖出平仓部分成交 撤单 '):
            pass
        with allure.step('2、点击“确定按钮”'):

            current = ATP.get_current_price(contract_code=contract_code)
            offset = 'close'
            direction = 'sell'
            order_price_type = "limit"

            ATP.common_user_make_order(
                contract_code=contract_code, price=current, direction='sell', offset='open')

            ATP.current_user_make_order(order_price_type=order_price_type, contract_code=contract_code,
                                        price=current, volume=10, direction='buy', offset='open')
            # 对手方买5
            ATP.common_user_make_order(
                contract_code=contract_code, volume=5, price=current, direction='buy', offset='close')
            # 自己卖10，部分成交
            res = ATP.current_user_make_order(order_price_type=order_price_type, contract_code=contract_code,
                                              price=current, volume=10, direction=direction, offset=offset)
            pprint(res)
            assert res['status'] == 'ok', "撮合失败！"

            res_cancle = linear_api.linear_cancel(
                order_id=res['data']['order_id_str'], contract_code=contract_code)
            pprint(res_cancle)
            assert res_cancle['status'] == 'ok' and res_cancle['data']['successes'] == res['data']['order_id_str'], "撤单失败"

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        print(ATP.clean_market())
        # 撤销当前用户 某个品种所有限价挂单
        print(ATP.cancel_all_order())
        print(ATP.make_market_depth())


if __name__ == '__main__':
    pytest.main()
