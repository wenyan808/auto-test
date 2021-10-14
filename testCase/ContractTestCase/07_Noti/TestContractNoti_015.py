#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211011
# @Author : 

#script by: lss
所属分组
    合约测试基线用例//01 交割合约//07 行情
用例标题
    请求批量Overview(所有合约，即不传contract_code)
前置条件
    
步骤/文本
    请求批量Overview(所有合约，即不传contract_code),可参考文档：https://docs.huobigroup.com/docs/dm/v1/cn/#websocket-3
预期结果
    open、close、low、high价格正确；amount、vol、count值正确,不存在Null,[]
优先级
    0
用例编号
    TestContractNoti_015
自动化作者
    韩东林
"""

from common.ContractServiceAPI import t as api

from pprint import pprint
import pytest, allure, random, time

from tool.common_assert import Assert


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('合约测试基线用例//01 交割合约//07 行情')  # 这里填功能
@allure.story('请求批量Overview(所有合约，即不传contract_code)')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Donglin Han', 'Case owner : Panfeng Liu')
@pytest.mark.stable
class TestContractNoti_015:

    @allure.title('请求批量Overview(所有合约，即不传contract_code)')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period, contract_type):
        with allure.step(
                '请求批量Overview(所有合约，即不传contract_code),可参考文档：https://docs.huobigroup.com/docs/dm/v1/cn/#websocket-3'):
            # open、close、low、high价格正确；amount、vol、count值正确,不存在Null,[]
            res = api.contract_market_over_view()
            pprint(res)
            print()
            pprint(res)
            ch = Assert.base_check_response(res, 'ch')
            assert ch == 'market.overview', 'ch is incorrect'

            data = Assert.base_check_response(res, 'data')
            assert isinstance(data, list) and len(data) > 1, 'data is incorrect'

            check_keys = ['amount', 'close', 'count', 'high', 'low', 'open', 'symbol', 'vol']

            for tick in data:
                assert set(check_keys) == set(tick.keys()), 'missing keys in data'

                act_symbol: str = tick.get('symbol', '')
                assert '_' in act_symbol and act_symbol[-2:] in ['CW', 'NW', 'NQ', 'CQ'], 'symbol is incorrect'

                close = float(tick.get('close', 0))
                assert close > 0, 'close 价格 错误'

                high = float(tick.get('high', 0))
                assert high >= close, 'high 价格 错误'

                low = float(tick.get('low', 0))
                assert 0 < low <= close, 'low 价格 错误'

                open = float(tick.get('open', 0))
                assert low <= open <= high, 'open 价格 错误'

                amount = float(tick.get('amount', -1))
                if high != low:
                    assert amount > 0, 'amount or  trade_turnover incorrect'
                elif amount == 0:
                    assert close == open, 'close or open incorrect'

    if __name__ == '__main__':
        pytest.main()
