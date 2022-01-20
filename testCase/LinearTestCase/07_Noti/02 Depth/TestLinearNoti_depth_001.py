#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211012
# @Author : 张广南

import time
import allure
import pytest

from common.LinearServiceAPI import t as linear_api
from common.LinearServiceWS import t as linear_service_ws
from common.CommonUtils import currentPrice, opponentExist
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL
from tool.atp import ATP


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('行情')  # 这里填功能
@allure.story('深度')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 张广南', 'Case owner : 吉龙')
class TestLinearNoti_depth_001:
    ids = [
        'TestLinearNoti_depth_001',
        'TestLinearNoti_depth_002',
        'TestLinearNoti_depth_003',
        'TestLinearNoti_depth_004',
        'TestLinearNoti_depth_005',
        'TestLinearNoti_depth_006',
        'TestLinearNoti_depth_007',
        'TestLinearNoti_depth_008',
        'TestLinearNoti_depth_009',
        'TestLinearNoti_depth_010',
        'TestLinearNoti_depth_011',
        'TestLinearNoti_depth_012',
        'TestLinearNoti_depth_013',
        'TestLinearNoti_depth_014',
        'TestLinearNoti_depth_015',
        'TestLinearNoti_depth_016',
    ]
    params = [
        {'case_name': 'WS订阅深度 150档不合并)', 'type': 'step0'},
        {'case_name': 'WS订阅深度 150档0.00001不合并)', 'type': 'step1'},
        {'case_name': 'WS订阅深度 150档0.0001不合并)', 'type': 'step2'},
        {'case_name': 'WS订阅深度 150档0.001不合并)', 'type': 'step3'},
        {'case_name': 'WS订阅深度 150档0.01不合并)', 'type': 'step4'},
        {'case_name': 'WS订阅深度 150档0.1不合并)', 'type': 'step5'},
        {'case_name': 'WS订阅深度 150档1不合并)', 'type': 'step14'},
        {'case_name': 'WS订阅深度 150档10不合并)', 'type': 'step15'},
        {'case_name': 'WS订阅深度 20档不合并)', 'type': 'step6'},
        {'case_name': 'WS订阅深度 20档0.00001不合并)', 'type': 'step7'},
        {'case_name': 'WS订阅深度 20档0.0001不合并)', 'type': 'step8'},
        {'case_name': 'WS订阅深度 20档0.001不合并)', 'type': 'step9'},
        {'case_name': 'WS订阅深度 20档0.01不合并)', 'type': 'step10'},
        {'case_name': 'WS订阅深度 20档0.1不合并)', 'type': 'step11'},
        {'case_name': 'WS订阅深度 20档1不合并)', 'type': 'step12'},
        {'case_name': 'WS订阅深度 20档10不合并)', 'type': 'step13'}
    ]

    @classmethod
    def setup_class(cls):
        with allure.step('实始化变量'):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.symbol = DEFAULT_SYMBOL
            pass
        with allure.step('挂单更新深度'):
            ATP.make_market_depth(volume=1, depth_count=5)

    @classmethod
    def teardown_class(cls):
        with allure.step('恢复环境，撤销挂单'):
            ATP.cancel_all_types_order()
            pass

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params, contract_code):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：执行sub订阅'):
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(1, 4):
                result = linear_service_ws.linear_sub_depth(contract_code=contract_code, type=params['type'])
                if 'tick' in result:
                    if result['tick']['asks'] and result['tick']['bids']:
                        flag = True
                        break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i))
            assert flag, '未返回预期结果'
            pass
        with allure.step('验证：返回结果买单卖单不为空'):
            assert result['tick']['bids'] is not None
            assert result['tick']['asks'] is not None
            pass


if __name__ == '__main__':
    pytest.main()
