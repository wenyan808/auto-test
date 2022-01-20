#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211220
# @Author : 
    用例标题
        restful批量聚合行情
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        字段值正确，数据类型正确
    优先级
        0
    用例别名
        TestLinearNoti_api_003
"""

from common.LinearServiceAPI import t as linear_api
from schema import Schema, Or
from tool.atp import ATP
from pprint import pprint
import pytest, allure, random, time


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('API')  # 这里填功能
@allure.story('schema校验')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 张广南', 'Case owner : 吉龙')
@pytest.mark.stable
class TestLinearNoti_api_003:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')
        ATP.make_market_depth(volume=1, depth_count=2)
    @allure.title('restful批量聚合行情')
    @allure.step('测试执行')
    def test_execute(self, contract_code, symbol):
        with allure.step('详见官方文档'):
            trade_partition = linear_api.get_trade_partition(contract_code)
            r = linear_api.linear_detail_batch_merged(contract_code=contract_code)
            pprint(r)
            schema = {'status': 'ok',
                      'ticks': [{'contract_code': contract_code,
                                 'business_type': 'swap',
                                 'amount': str,
                                 'ask': list,
                                 'bid': list,
                                 'close': str,
                                 'count': int,
                                 'high': str,
                                 'id': int,
                                 'low': str,
                                 'open': str,
                                 'trade_turnover': str,
                                 'trade_partition': trade_partition,
                                 'ts': int,
                                 'vol': str}],
                      'ts': int}

            Schema(schema).validate(r)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_types_order()


if __name__ == '__main__':
    pytest.main()
