#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211012
# @Author : 张广南
    用例标题
        WS订阅深度 不传合约代码
    前置条件
        
    步骤/文本
        参考官方文档
    预期结果
        订阅失败
    优先级
        3
    用例别名
        TestLinearNoti_depth_038
"""
import allure
import pytest

from common.LinearServiceWS import t as linear_service_ws
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('行情')  # 这里填功能
@allure.story('深度')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 张广南', 'Case owner : 吉龙')
class TestLinearNoti_depth_038:
    contract_code = DEFAULT_CONTRACT_CODE
    ids = [
        'TestLinearNoti_depth_038',
        'TestLinearNoti_depth_039',
        'TestLinearNoti_depth_040',
        'TestLinearNoti_depth_041',
        'TestLinearNoti_depth_042',
        'TestLinearNoti_depth_043',
    ]
    params = [
        {'case_name': 'WS订阅深度 不传合约代码)','contract_code':'', 'type': 'step0'},
        {'case_name': 'WS订阅深度 传空合约代码)','contract_code':' ', 'type': 'step0'},
        {'case_name': 'WS订阅深度 传空合约代码)','contract_code':'UDS-USD', 'type': 'step0'},
        {'case_name': 'WS订阅深度 不传深度)', 'contract_code': contract_code, 'type': ''},
        {'case_name': 'WS订阅深度 深度传空)', 'contract_code': contract_code, 'type': ' '},
        {'case_name': 'WS订阅深度 深度不存在)', 'contract_code': contract_code, 'type': 'step99'},
    ]


    @classmethod
    def setup_class(cls):
        with allure.step('实始化变量'):
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params, contract_code):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：执行sub订阅'):
            subs = {
                "sub": "market.{}.depth.{}".format(params['contract_code'], params['type']),
                "id": "id5"
            }
            result = linear_service_ws.linear_sub(subs)

        with allure.step('验证：返回结果提示invalid topic'):
            assert 'bad-request' in result['err-code']


if __name__ == '__main__':
    pytest.main()
