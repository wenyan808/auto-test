#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211010
# @Author :Alexli
"""
所属分组
    计划委托
用例标题
    计划委托买入平空触发价等于最新价
前置条件
    
步骤/文本
    1、登录合约交易系统
    2、选择币种BTC，选择杠杆5X，点击平仓-计划按钮
    3、输入触发价（如：50000，最新价：50000）
    4、输入买入价（如：45000）
    5、输入买入量10张
    6、点击买入平空按钮，弹框点击确认
预期结果
    A)提示下单成功
    B)当前委托-计划委托列表查询创建订单
优先级
    1
"""

from pprint import pprint
import time

import allure
import pytest

from common.ContractServiceAPI import t as contract_api
from common.util import compare_dict
from tool.atp import ATP


@allure.epic('交割合约')  # 这里填业务线
@allure.feature('计划委托')  # 这里填功能
@allure.story('计划委托买入平空触发价等于最新价')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestContractTriggerCloseBuy_005:

    @allure.step('前置条件')
    @pytest.fixture(scope='function')
    def setup(self):
        ATP.close_all_position()
        print(''' 使当前交易对有交易盘口  ''')
        print(ATP.make_market_depth())
        print(''' 使当前用户有持仓  ''')
        time.sleep(0.5)
        print(ATP.current_user_make_order(order_price_type='limit'))

    @allure.title('计划委托买入平空触发价等于最新价')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step('1、登录合约交易系统'):
            pass
        with allure.step('2、选择币种BTC，选择杠杆5X，点击平仓-计划按钮'):
            pass
        with allure.step('3、输入触发价（如：50000，最新价：50000）'):
            pass
        with allure.step('4、输入卖出价（如：45000）'):
            pass
        with allure.step('5、输入卖出量10张'):
            pass
        with allure.step('6、点击卖出平空按钮，弹框点击确认'):
            current = ATP.get_current_price(contract_code='BTC_CW')
            trigger_price = current
            order_price = round(current * 0.99, 2)
            offset = 'close'
            direction = 'buy'
            res = ATP.current_user_make_trigger_order(contract_code='BTC_CW', trigger_type='ge',
                                                      trigger_price=trigger_price, order_price=order_price, volume=10, direction=direction, offset=offset)
            pprint(res)

            # A)提示下单成功
            assert res['status'] == 'ok', '计划委托单下单失败'
            data = res.get('data', {})
            assert 'order_id' in data and 'order_id_str' in data, '计划委托单下单失败'
            order_id = data['order_id']
            # B)当前委托 - 计划委托列表查询创建订单
            time.sleep(3)
            res = contract_api.contract_trigger_openorders(symbol='BTC', contract_code='BTC_CW',
                                                           page_index='',
                                                           page_size='')
            pprint(res)
            if res['data']['orders']:
                actual_orderinfo = res['data']['orders'][0]
                pprint(actual_orderinfo)
                with allure.step('7、当前委托-计划委托列表查询创建订单B'):
                    expectdic = {'order_price': order_price,
                                 'order_id': order_id,
                                 'trigger_price': trigger_price,
                                 'volume': 10.0,
                                 'offset': 'close'
                                 }
                    assert compare_dict(expectdic, actual_orderinfo)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_trigger_order()
        ATP.cancel_all_order()
        ATP.close_all_position()


if __name__ == '__main__':
    pytest.main()
