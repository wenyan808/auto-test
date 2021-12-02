#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211012
# @Author : 张广南

import time
import allure
import pytest

from common.SwapServiceWS import user01 as ws_user01
from common.SwapServiceAPI import user01 as api_user01
from common.CommonUtils import currentPrice,opponentExist
from config.conf import DEFAULT_CONTRACT_CODE,DEFAULT_SYMBOL
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][4])
@pytest.mark.stable
@allure.tag('Script owner : 张广南', 'Case owner : 吉龙')
class TestSwapNoti_depth_038:
    contract_code = DEFAULT_CONTRACT_CODE
    ids = [
        'TestSwapNoti_depth_038',
        'TestSwapNoti_depth_039',
        'TestSwapNoti_depth_040',
        'TestSwapNoti_depth_041',
        'TestSwapNoti_depth_042',
        'TestSwapNoti_depth_043',
    ]
    params = [
        {'case_name': 'WS订阅深度 不传合约代码)','contract_code':'', 'type': 'step0'},
        {'case_name': 'WS订阅深度 传空合约代码)','contract_code':' ', 'type': 'step0'},
        {'case_name': 'WS订阅深度 传空合约代码)','contract_code':'UDS-USD', 'type': 'step0'},
        {'case_name': 'WS订阅深度 不传深度)', 'contract_code': contract_code, 'type': ''},
        {'case_name': 'WS订阅深度 深度传空)', 'contract_code': contract_code, 'type': ' '},
        {'case_name': 'WS订阅深度 深度不存在)', 'contract_code': contract_code, 'type': 'step99'},
    ]

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：执行sub订阅'):
            subs = {
                "sub": "market.{}.depth.{}".format(params['contract_code'], params['type']),
                "id": "id5"
            }
            result = ws_user01.swap_sub(subs)
            pass
        with allure.step('验证：返回结果提示invalid topic'):
            assert 'bad-request' in result['err-code']
            pass


if __name__ == '__main__':
    pytest.main()
