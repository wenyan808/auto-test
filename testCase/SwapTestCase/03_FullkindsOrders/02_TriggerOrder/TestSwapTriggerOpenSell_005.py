#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211008
# @Author : Donglin Han

所属分组
    合约测试基线用例//02 反向永续//03 全部策略订单//02 计划委托//正常限价开仓
用例标题
    计划委托卖出开空触发价小于最新价
前置条件
    
步骤/文本
    1、登录合约交易系统
    2、选择币种BTC，选择杠杆5X，点击开仓-计划按钮
    3、输入触发价（如：50000，最新价：50500）
    4、输入卖出价（如：55000）
    5、输入卖出量10张
    6、点击卖出开空按钮，弹框点击确认
预期结果
    A)提示下单成功
    B)当前委托-计划委托列表查询创建订单
优先级
    1
用例编号
    TestSwapTriggerOpenSell_005
自动化作者
    韩东林
"""

import allure
import pytest
import time

from common.SwapServiceAPI import t as swap_api
from tool.atp import ATP


@allure.epic('所属分组')  # 这里填业务线
@allure.feature('合约测试基线用例//02 反向永续//03 全部策略订单//02 计划委托//正常限价开仓')  # 这里填功能
@allure.story('计划委托卖出开空触发价小于最新价')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Donglin Han', 'Case owner : Donglin Han')
@pytest.mark.stable
class TestSwapTriggerOpenSell_005:

    @allure.step('前置条件')
    def setup(self):
        print(''' 初始化 ''')

    @allure.title('计划委托卖出开空触发价小于最新价')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('1、登录合约交易系统'):
            pass
        with allure.step('2、选择币种BTC，选择杠杆5X，点击开仓-计划按钮'):
            pass
        with allure.step('3、输入触发价（如：50000，最新价：50500）'):
            current = ATP.get_current_price()
            trigger_price = round(current * 0.99, 1)
            offset = 'open'
            direction = 'sell'
            res = ATP.current_user_make_trigger_order(trigger_price=trigger_price, direction=direction, offset=offset)
            print(res)

            # 提示下单成功
            assert res['status'] == 'ok', '计划委托单下单失败'
            data = res.get('data', {})
            assert 'order_id' in data and 'order_id_str' in data, '计划委托单下单失败'
            order_id = data['order_id']
        with allure.step('4、输入卖出价（如：55000）'):
            pass
        with allure.step('5、输入卖出量10张'):
            pass
        with allure.step('6、点击卖出开空按钮，弹框点击确认'):
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


if __name__ == '__main__':
    pytest.main()
