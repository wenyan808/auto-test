#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211011
# @Author : Donglin Han

所属分组
    合约测试基线用例//02 反向永续//07 行情
用例标题
    请求深度(150档不合并)
前置条件
    
步骤/文本
    请求深度(150档不合并),可参考文档：https://docs.huobigroup.com/docs/coin_margined_swap/v1/cn/#websocket-3
预期结果
    asks,bids 数据正确,不存在Null,[]
优先级
    0
用例编号
    TestSwapNoti_011
自动化作者
    韩东林
"""
import time
from pprint import pprint

import allure
import pytest

from common.SwapServiceAPI import t as api
from tool.atp import ATP
from tool.common_assert import Assert


@allure.epic('所属分组')  # 这里填业务线
@allure.feature('合约测试基线用例//02 反向永续//07 行情')  # 这里填功能
@allure.story('请求深度(150档不合并)')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Donglin Han', 'Case owner : Panfeng Liu')
@pytest.mark.stable
class TestSwapNoti_011:

    @allure.step('前置条件')
    def setup(self):
        print(''' cancel all types orders ''')
        ATP.cancel_all_types_order()
        time.sleep(1)
        self.current_price = ATP.get_current_price()
        print(''' make market depth ''')
        ATP.make_market_depth()
        sell_price = ATP.get_adjust_price(1.02)
        buy_price = ATP.get_adjust_price(0.98)
        ATP.common_user_make_order(price=sell_price, direction='sell')
        ATP.common_user_make_order(price=buy_price, direction='buy')
        time.sleep(2)

    @allure.title('请求深度(150档不合并)')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('请求深度(150档不合并),可参考文档：https://docs.huobigroup.com/docs/usdt_swap/v1/cn/#0737c93bf7'):
            # asks,bids 数据正确,不存在Null,[]
            res = api.swap_depth(contract_code=contract_code, type='step0')
            print('深度(150档不合并) response : ')
            pprint(res)
            tick = Assert.base_check_response(res, 'tick')
            check_keys = ['asks', 'bids', 'ch', 'id', 'mrid', 'ts', 'version']
            assert isinstance(tick, dict) and set(check_keys) == set(tick.keys()), 'response 中 tick 缺少字段'

            ch = tick.get('ch', '')
            assert ch == f'market.{contract_code.upper()}.depth.step0', 'ch 不正确'

            asks = tick.get('asks', [])
            bids = tick.get('bids', [])
            mrid = tick.get('mrid', -1)
            assert isinstance(asks, list) and len(asks) == 2, 'asks 不正确'
            for ask in asks:
                assert isinstance(ask, list) and len(ask) == 2 and ask[0] > 0 and ask[1] == 10 and ask[
                    0] > self.current_price, 'ask 价格 或 数量 错误'

            assert isinstance(bids, list) and len(bids) == 2, 'bids 不正确'
            for bid in bids:
                assert isinstance(bid, list) and len(bids) == 2 and bid[0] > 0 and bid[1] == 10 and bid[
                    0] < self.current_price, 'bid 价格 或 数量 错误'

            assert isinstance(mrid, int) and mrid >= 0, '获取bbo mrid 错误'

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
