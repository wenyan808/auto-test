#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211220
# @Author : 
    用例标题
        ws 增量20档
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        字段值正确，数据类型正确
    优先级
        0
    用例别名
        TestLinearNoti_api_011
"""

from common.LinearServiceWS import t as linear_service_ws
from schema import Schema, Or
from tool.atp import ATP
from pprint import pprint
import pytest, allure, random, time


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('API')  # 这里填功能
@allure.story('schema校验')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 张广南', 'Case owner : 吉龙')
@pytest.mark.stable
class TestLinearNoti_api_s011:
    ids = ['TestLinearNoti_api_011',
           'TestLinearNoti_api_012']
    params = [{'title': 'TestLinearNoti_api_011', 'case_name': 'ws 增量20档', 'size': '20'},
              {'title': 'TestLinearNoti_api_012', 'case_name': 'ws 增量150档', 'size': '150'}]

    @classmethod
    def setup_class(cls):
        print('''  ''')
        ATP.make_market_depth(volume=1, depth_count=150)

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, contract_code, params):
        allure.dynamic.title(params['title'])
        with allure.step('详见官方文档'):
            time.sleep(1)
            size = params['size']
            r = linear_service_ws.linear_sub_depth_high_freq(contract_code=contract_code, size=size)
            pprint(r)
            schema = {'ch': f'market.{contract_code}.depth.size_{size}.high_freq',
                      'tick': {'ch': f'market.{contract_code}.depth.size_{size}.high_freq',
                               'asks': Or(list, None),
                               'bids': Or(list, None),
                               'event': Or('update', 'snapshot'),
                               'id': int,
                               'mrid': int,
                               'ts': int,
                               'version': int},
                      'ts': int}
            Schema(schema).validate(r)

    @classmethod
    def teardown_class(cls):
        print('\n恢复环境操作')
        print(ATP.cancel_all_types_order())


if __name__ == '__main__':
    pytest.main()
