#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211011
# @Author : Donglin Han

所属分组
    合约测试基线用例//02 反向永续//07 行情
用例标题
    请求聚合行情(单个合约，即传参contract_code)
前置条件
    
步骤/文本
    请求聚合行情(单个合约，即传参contract_code),可参考文档：https://docs.huobigroup.com/docs/coin_margined_swap/v1/cn/#websocket-3
预期结果
    open、close、low、high价格正确；amount、vol、count值正确asks、bid值正确,不存在Null,[]
优先级
    0
用例编号
    TestSwapNoti_013
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


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('合约测试基线用例//02 反向永续//07 行情')  # 这里填功能
@allure.story('请求聚合行情(单个合约，即传参contract_code)')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Donglin Han', 'Case owner : Panfeng Liu')
@pytest.mark.stable
class TestSwapNoti_013:

    @allure.step('前置条件')
    def setup(self):
        print(" 清盘 -》 挂单 ")
        ATP.cancel_all_types_order()
        time.sleep(0.5)
        ATP.make_market_depth()
        self.current_price = ATP.get_current_price()
        sell_price = ATP.get_adjust_price(1.02)
        buy_price = ATP.get_adjust_price(0.98)
        ATP.common_user_make_order(price=sell_price, direction='sell')
        ATP.common_user_make_order(price=buy_price, direction='buy')
        time.sleep(1)

    @allure.title('请求聚合行情(单个合约，即传参contract_code)')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('请求聚合行情(单个合约，即传参contract_code),可参考文档：https://docs.huobigroup.com/docs/dm/v1/cn/#websocket-3'):
            # open、close、low、high价格正确；amount、vol、count值正确asks、bid值正确,不存在Null,[]
            res = api.swap_detail_merged(contract_code=contract_code)
            pprint(res)
            tick = Assert.base_check_response(res, 'tick')

            ch = res.get('ch', '')
            assert ch == f'market.{contract_code.upper()}.detail.merged', 'ch 不正确'

            check_keys = ['vol', 'count', 'open', 'close', 'low', 'high', 'amount', 'ask', 'bid',
                          'id',
                          'ts']
            assert isinstance(tick, dict) and set(check_keys) == set(tick.keys()), 'response 中 tick 缺少字段'

            ask = tick.get('ask', [])
            bid = tick.get('bid', [])

            assert isinstance(ask, list) and len(ask) == 2 and ask[0] > 0 and ask[1] == 10 and ask[
                0] > self.current_price, 'ask 价格 或 数量 错误'

            assert isinstance(bid, list) and len(bid) == 2 and bid[0] > 0 and bid[1] == 10 and bid[
                0] < self.current_price, 'bid 价格 或 数量 错误'

            close = float(tick.get('close', 0))
            assert close == self.current_price, 'close 价格 错误'

            high = float(tick.get('high', 0))
            assert high >= close, 'high 价格 错误'

            low = float(tick.get('low', 0))
            assert 0 < low <= close, 'low 价格 错误'

            open = float(tick.get('open', 0))
            assert low <= open <= high, 'open 价格 错误'

            vol = int(tick.get('vol', 0))
            assert vol >= 20, 'vol 错误'

            id = tick.get('id', 0)
            assert int(time.time()) - (48 * 60 * 60) <= id <= int(time.time()), 'id 错误'

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.clean_market()


if __name__ == '__main__':
    pytest.main()
