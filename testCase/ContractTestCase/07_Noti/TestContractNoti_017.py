#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211011
# @Author : Donglin Han

所属分组
    合约测试基线用例//01 交割合约//07 行情
用例标题
    请求批量成交记录(单个合约，即传参contract_code)
前置条件
    
步骤/文本
    请求批量成交记录(单个合约，即传参contract_code),可参考文档：https://docs.huobigroup.com/docs/dm/v1/cn/#websocket-3
预期结果
    amount\quantity\turnover\direction\price显示正确,不存在Null,[]
优先级
    0
用例编号
    TestContractNoti_017
自动化作者
    韩东林
"""

from pprint import pprint

import allure
import pytest
import time

from common.ContractServiceAPI import t as api
from tool.atp import ATP
from tool.common_assert import Assert
from tool.atp import ATP

@allure.epic('反向交割')  # 这里填业务线
@allure.feature('合约测试基线用例//01 交割合约//07 行情')  # 这里填功能
@allure.story('请求批量成交记录(单个合约，即传参contract_code)')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Donglin Han', 'Case owner : Panfeng Liu')
@pytest.mark.stable
class TestContractNoti_017:

    @allure.step('前置条件')
    def setup(self):
        print(" 清盘 -》 挂单 ")
        ATP.cancel_all_types_order()
        time.sleep(0.5)
        self.current_price = ATP.get_current_price()
        ATP.common_user_make_order(price=self.current_price, direction='sell')
        time.sleep(1)
        ATP.common_user_make_order(price=self.current_price, direction='buy')
        time.sleep(1)
        ATP.common_user_make_order(price=self.current_price, direction='sell')
        time.sleep(1)
        ATP.common_user_make_order(price=self.current_price, direction='buy')
        time.sleep(1)

    @allure.title('请求批量成交记录(单个合约，即传参contract_code)')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step(
                '请求批量成交记录(单个合约，即传参contract_code),可参考文档：https://docs.huobigroup.com/docs/dm/v1/cn/#websocket-3'):
            # amount\quantity\turnover\direction\price显示正确,不存在Null,[]
            res = api.contract_history_trade(symbol_period, 2)
            print()
            pprint(res)

            data = Assert.base_check_response(res, 'data')
            assert isinstance(data, list) and len(data) == 2, 'response data is incorrect'
            for tick in data:
                check_keys = ['data', 'id', 'ts']
                assert set(check_keys) == set(tick.keys()), 'response tick is incorrect'

                ch = Assert.base_check_response(res, 'ch')
                assert ch == f'market.{symbol_period.upper()}.trade.detail', 'response ch is incorrect'

                data = tick.get('data', [])
                assert isinstance(data, list) and len(data) == 1, 'response data is incorrect'

                trade_record = data[0]
                check_keys = ['amount', 'direction', 'id', 'price', 'quantity', 'ts']
                assert set(check_keys) == set(trade_record.keys()), 'response trade_record is incorrect'

                amount = int(trade_record.get('amount', '0'))
                direction = trade_record.get('direction', '')
                id = trade_record.get('id', 0)
                price = float(trade_record.get('price', '0'))
                quantity = float(trade_record.get('quantity', '0'))

                assert amount == 20, 'amount is incorrect'
                assert direction == 'buy', 'direction is incorrect'
                assert id > 0, 'id is incorrect'
                assert price == self.current_price, 'price is incorrect'
                assert quantity > 0, 'quantity is incorrect'

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_order()


if __name__ == '__main__':
    pytest.main()
