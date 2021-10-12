#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211011
# @Author : Donglin Han

所属分组
    合约测试基线用例//03 正向永续//07 行情
用例标题
    请求K线(传参from,to)
前置条件
    
步骤/文本
    请求K线(传参from,to)，可参考文档：https://docs.huobigroup.com/docs/usdt_swap/v1/cn/#websocket-3
预期结果
    id、open、close、low、high价格正确；amount、vol、count值正确,不存在Null,[]
优先级
    0
用例编号
    TestLinearNoti_010
自动化作者
    韩东林
"""

from pprint import pprint

import allure
import pytest
import time

from common.LinearServiceAPI import t as api
from tool.atp import ATP


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('合约测试基线用例//03 正向永续//07 行情')  # 这里填功能
@allure.story('请求K线(传参from,to)')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Donglin Han', 'Case owner : Panfeng Liu')
@pytest.mark.stable
class TestLinearNoti_010:
    from_time = None
    to_time = None
    current_price = None

    @allure.step('前置条件')
    def setup(self):
        ATP.cancel_all_types_order()
        self.from_time = int(time.time())
        print(''' 制造成交数据 ''')
        ATP.make_market_depth()
        time.sleep(0.5)
        ATP.clean_market()
        time.sleep(1)
        self.current_price = ATP.get_current_price()
        self.to_time = int(time.time())

    @allure.title('请求K线(传参from,to)')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('请求K线(传参from,to)，可参考文档：https://docs.huobigroup.com/docs/usdt_swap/v1/cn/#websocket-3'):
            # id、open、close、low、high价格正确；amount、vol、count值正确,不存在Null,[]
            res = api.linear_kline(contract_code=contract_code, period='1min', FROM=self.from_time, to=self.to_time)
            pprint(res)
            # id、open、close、low、high价格正确；amount、vol、count值正确,不存在Null,[]
            data = res.get('data', [])
            assert isinstance(data, list) and 1 <= len(data) <= 2, 'K 线数据不正确'

            # 检查字段
            include_keys = ['amount', 'close', 'count', 'high', 'id', 'low', 'open', 'vol', 'trade_turnover']
            for record in data:
                assert set(include_keys) == set(record.keys()), 'K 线数据 缺少字段'

            merge_record = {}
            # 如果是两条数据 进行合并
            if len(data) == 2:
                merge_record['amount'] = data[0]['amount'] + data[1]['amount']
                merge_record['trade_turnover'] = data[0]['trade_turnover'] + data[1]['trade_turnover']
                merge_record['close'] = data[1]['close']
                merge_record['count'] = data[0]['count'] + data[1]['count']
                merge_record['high'] = max([data[0]['high'], data[1]['high']])
                merge_record['id'] = min([data[0]['id'], data[1]['id']])
                merge_record['low'] = min([data[0]['low'], data[1]['low']])
                merge_record['open'] = data[0]['open']
                merge_record['vol'] = data[0]['vol'] + data[1]['vol']
            else:
                merge_record = data[0]
            # 检查字段数值
            assert merge_record['trade_turnover'] > 0, 'K 线数据 trade_turnover 不正确'
            assert merge_record['amount'] > 0, 'K 线数据 amount 不正确'
            assert merge_record['close'] == self.current_price, 'K 线数据 close 不正确'
            assert merge_record['count'] >= 2, 'K 线数据 amount 不正确'
            assert merge_record['high'] >= self.current_price, 'K 线数据 high 不正确'
            assert merge_record['id'] - 60 <= self.from_time, 'K 线数据 id 不正确'
            assert merge_record['id'] + 120 >= self.from_time, 'K 线数据 id 不正确'
            assert merge_record['low'] >= 0, 'K 线数据 low 不正确'
            assert merge_record['low'] <= merge_record['open'] <= merge_record['high'], 'K 线数据 open 不正确'
            assert merge_record['vol'] >= 40, 'K 线数据 vol 不正确'

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
