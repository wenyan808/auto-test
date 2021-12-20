#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211012
# @Author : 张广南

import time
import allure
import pytest

from common.SwapServiceWS import user01 as ws_user01
from common.SwapServiceAPI import user01 as api_user01
from tool.SwapTools import SwapTool,opponentExist
from config.conf import DEFAULT_CONTRACT_CODE,DEFAULT_SYMBOL
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][4])
@pytest.mark.stable
@allure.tag('Script owner : 张广南', 'Case owner : 吉龙')
class TestSwapNoti_depth_001:
    ids = [
        'TestSwapNoti_depth_001',
        'TestSwapNoti_depth_002',
        'TestSwapNoti_depth_003',
        'TestSwapNoti_depth_004',
        'TestSwapNoti_depth_005',
        'TestSwapNoti_depth_006',
        'TestSwapNoti_depth_007',
        'TestSwapNoti_depth_008',
        'TestSwapNoti_depth_009',
        'TestSwapNoti_depth_010',
        'TestSwapNoti_depth_011',
        'TestSwapNoti_depth_012',
        'TestSwapNoti_depth_013',
        'TestSwapNoti_depth_014',
        'TestSwapNoti_depth_015',
        'TestSwapNoti_depth_016',
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
            cls.currentPrice = currentPrice()  # 最新价
            pass
        with allure.step('挂单更新深度'):
            for i in range (5):
                api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice * (1-0.01*i), 2), direction='buy')
                api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice * (1+0.01*i), 2), direction='sell')
            pass
        with allure.step('查询redis深度更新'):
            for i in range (5):
                if opponentExist(symbol=cls.symbol,asks='asks',bids='bids'):
                    break
                else:
                    print('深度未更新,第{}次重试……'.format(i+1))
                    time.sleep(1)



    @classmethod
    def teardown_class(cls):
        with allure.step('恢复环境，撤销挂单'):
            api_user01.swap_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：执行sub订阅'):
            subs = {
                "sub": "market.{}.depth.{}".format(self.contract_code, params['type']),
                "id": "id5"
            }
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(1, 4):
                result = ws_user01.swap_sub(subs)
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
