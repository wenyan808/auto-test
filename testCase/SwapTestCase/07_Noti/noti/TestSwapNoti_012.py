#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211011
# @Author : Donglin Han

所属分组
    合约测试基线用例//02 反向永续//07 行情
用例标题
    请求BBO(单个合约，即传参code)
前置条件
    
步骤/文本
    请求BBO(单个合约，即传参code),可参考文档：https://docs.huobigroup.com/docs/coin_margined_swap/v1/cn/#websocket-3
预期结果
    asks,bids 数据正确,不存在Null,[]
优先级
    0
用例编号
    TestSwapNoti_012
自动化作者
    韩东林
"""

from common.SwapServiceAPI import t as api

from pprint import pprint
import pytest, allure, random, time

from tool.atp import ATP


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('合约测试基线用例//02 反向永续//07 行情')  # 这里填功能
@allure.story('请求BBO(单个合约，即传参code)')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Donglin Han', 'Case owner : Panfeng Liu')
@pytest.mark.stable
class TestSwapNoti_012:
    current_price = None

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
        time.sleep(2)

    @allure.title('请求BBO(单个合约，即传参code)')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step(
                '请求BBO(单个合约，即传参code),可参考文档：https://docs.huobigroup.com/docs/coin_margined_swap/v1/cn/#websocket-3'):
            # asks,bids 数据正确,不存在Null,[]
            res = api.swap_bbo(contract_code)
            print(res)
            status = res.get('status', 'error')
            assert status == 'ok', '获取bbo 返回状态错误'
            ticks = res.get('ticks', [])
            assert isinstance(ticks, list) and len(ticks) == 1, '获取bbo ticks 错误'
            record = ticks[0]
            contract_code = record.get('contract_code', '')
            assert contract_code.upper() == contract_code, '获取bbo contract_code 错误'
            ask = record.get('ask', [])
            bid = record.get('bid', [])
            mrid = record.get('mrid', -1)
            assert isinstance(ask, list) and len(ask) == 2 and ask[0] > 0 and ask[1] == 10 and ask[
                0] > self.current_price, '获取bbo ask 错误'
            assert isinstance(bid, list) and len(bid) == 2 and bid[0] > 0 and bid[1] == 10 and bid[
                0] < self.current_price, '获取bbo bid 错误'
            assert isinstance(mrid, int) and mrid >= 0, '获取bbo mrid 错误'

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.clean_market()


if __name__ == '__main__':
    pytest.main()
