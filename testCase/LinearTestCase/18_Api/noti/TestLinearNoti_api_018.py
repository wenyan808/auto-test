#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211220
# @Author : 
    用例标题
        ws 深度图
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        字段值正确，数据类型正确
    优先级
        0
    用例别名
        TestLinearNoti_api_018
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
class TestLinearNoti_api_018:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('ws 深度图')
    @allure.step('测试执行')
    def test_execute(self, contract_code, symbol):
        with allure.step('详见官方文档'):
            percent = 'percent10'
            r = linear_service_ws.linear_sub_depth_chart(contract_code=contract_code, percent=percent)
            pprint(r)
            schema = {'ch': f'market.{contract_code}.depth.{percent}',
                      'tick': {'ch': f'market.{contract_code}.depth.{percent}',
                               'asks': list,
                               'bids': list,
                               'id': int,
                               'mrid': int,
                               'ts': int,
                               'version': int},
                      'ts': int}

            Schema(schema).validate(r)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
