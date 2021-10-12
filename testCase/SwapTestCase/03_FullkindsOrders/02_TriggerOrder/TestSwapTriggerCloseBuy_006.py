#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211008
# @Author : Donglin Han

所属分组
    合约测试基线用例//02 反向永续//03 全部策略订单//02 计划委托//正常限价平仓
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
    B)当前委托-计划委托列表查询创建订单（可能会触发订单）
优先级
    1
用例编号
    TestSwapTriggerCloseBuy_006
自动化作者
    韩东林
"""

import allure
import pytest
import time

from common.SwapServiceAPI import t as swap_api
from tool.atp import ATP


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('合约测试基线用例//02 反向永续//03 全部策略订单//02 计划委托//正常限价平仓')  # 这里填功能
@allure.story('计划委托买入平空触发价等于最新价')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Donglin Han', 'Case owner : Donglin Han')
@pytest.mark.stable
class TestSwapTriggerCloseBuy_006:

    @allure.step('前置条件')
    def setup(self):
        ATP.cancel_all_types_order()
        time.sleep(0.5)
        ATP.close_all_position()
        time.sleep(0.5)
        print(''' 使当前交易对有交易盘口  ''')
        print(ATP.make_market_depth())
        print(''' 使当前用户有持仓  ''')
        time.sleep(0.5)
        print(ATP.current_user_make_order(order_price_type='opponent'))
        time.sleep(0.5)

    @allure.title('计划委托买入平空触发价等于最新价')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('1、登录合约交易系统'):
            pass
        with allure.step('2、选择币种BTC，选择杠杆5X，点击平仓-计划按钮'):
            pass
        with allure.step('3、输入触发价（如：50000，最新价：50000）'):
            trigger_price = current = ATP.get_current_price()
            offset = 'close'
            direction = 'buy'
            res = ATP.current_user_make_trigger_order(trigger_price=trigger_price, direction=direction, offset=offset)
            print(res)

            # 提示下单成功
            assert res['status'] == 'ok', '计划委托单下单失败'
            data = res.get('data', {})
            assert 'order_id' in data and 'order_id_str' in data, '计划委托单下单失败'
            order_id = data['order_id']
        with allure.step('4、输入买入价（如：45000）'):
            pass
        with allure.step('5、输入买入量10张'):
            pass
        with allure.step('6、点击买入平空按钮，弹框点击确认'):
            # B)当前委托 - 计划委托列表查询创建订单
            time.sleep(3)
            res = swap_api.swap_trigger_openorders(contract_code=contract_code)
            print(res)

            assert res['status'] == 'ok', '查询计划委托单失败'
            data = res.get('data', {})
            assert 'orders' in data, '查询计划委托单失败'
            assert isinstance(data['orders'], list) and len(data['orders']) > 0, '未查询到计划委托单'
            assert isinstance(data['orders'][0], dict) and 'order_id' in data['orders'][0], '未查询到计划委托单'
            assert data['orders'][0]['order_id'] == order_id, '查询到的计划委托单 与 下单不相符'
            assert data['orders'][0]['offset'] == offset, '查询到的计划委托单 与 下单不相符'
            assert data['orders'][0]['direction'] == direction, '查询到的计划委托单 与 下单不相符'

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_trigger_order()
        ATP.cancel_all_order()
        ATP.close_all_position()


if __name__ == '__main__':
    pytest.main()
