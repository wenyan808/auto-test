#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20220212
# @Author : 
    用例标题
        切换持仓模式（全仓）
    前置条件
        
    步骤/文本
        1.调用接口 linear-swap-api/v1/swap_cross_switch_position_mode，有结果A
    预期结果
        A)接口返回的json格式、字段名、字段值正确
    优先级
        0
    用例别名
        TestLinearApiSchema_114
"""

import time
from pprint import pprint

import allure
import pytest
from schema import Schema, Or

from common.LinearServiceAPI import common_user_linear_service_api as linear_api


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('api')  # 这里填功能
@allure.story('schema校验')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 张广南', 'Case owner : 张让翰')
@pytest.mark.stable
class TestLinearApiSchema_114:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('切换持仓模式（全仓）')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('1.调用接口 linear-swap-api/v1/swap_cross_switch_position_mode，有结果A'):
            margin_account = contract_code.split('-')[-1]
            r = linear_api.linear_cross_switch_position_mode(margin_account=margin_account,
                                                             position_mode='single_side')  # single_side dual_side
            pprint(r)
            schema = {"data": {"margin_account": margin_account,
                               "position_mode": "single_side"
                               },
                      "status": "ok",
                      "ts": int
                      }

            Schema(schema).validate(r)

            time.sleep(5)

            r = linear_api.linear_cross_switch_position_mode(margin_account=margin_account,
                                                             position_mode='dual_side')  # single_side dual_side
            pprint(r)
            schema = {"data": {"margin_account": margin_account,
                               "position_mode": "dual_side"
                               },
                      "status": "ok",
                      "ts": int
                      }

            Schema(schema).validate(r)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
