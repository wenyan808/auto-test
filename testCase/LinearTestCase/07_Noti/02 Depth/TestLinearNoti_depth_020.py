#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211012
# @Author : 张广南
    用例标题
        WS订阅深度 非SHIB 20档step19
    前置条件
        
    步骤/文本
        参考官方文档
    预期结果
        订阅失败
    优先级
        3
    用例别名
        TestLinearNoti_depth_020
"""

import allure
import pytest

from common.LinearServiceWS import t as linear_service_ws
from tool.atp import ATP


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('行情')  # 这里填功能
@allure.story('深度')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 张广南', 'Case owner : 吉龙')
class TestLinearNoti_depth_020:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, contract_code, lever_rate, offsetO, directionB, directionS):
        ATP.clean_market()

        ATP.make_market_depth(volume=1, depth_count=1)

    @allure.title('WS订阅深度 非SHIB 20档step19')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('参考官方文档'):
            depth_type = 'step19'
            subs = {
                "sub": "market.{}.depth.{}".format(contract_code, depth_type),
                "id": "id5"
            }
            result = linear_service_ws.linear_sub(subs)
            result_str = '\nDepth返回结果 = ' + str(result)
            print('\033[1;32;49m%s\033[0m' % result_str)
            assert result['err-msg'] == 'invalid topic market.%s.depth.step19' % contract_code

    @allure.step('恢复环境')
    def teardown(self):
        ATP.cancel_all_types_order()
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
