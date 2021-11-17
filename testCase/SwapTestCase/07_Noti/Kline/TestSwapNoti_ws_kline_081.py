#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211013
# @Author : HuiQing Yu

from common.SwapServiceWS import t as swap_service_ws
import pytest, allure, random, time
from config.conf import DEFAULT_CONTRACT_CODE

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('WS订阅(sub)')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_081:
    contract_code = DEFAULT_CONTRACT_CODE
    ids = [
        'TestSwapNoti_ws_kline_081',
        'TestSwapNoti_ws_kline_082',
        'TestSwapNoti_ws_kline_083'
    ]
    params = [
        {'case_name': 'WS订阅K线(sub)-合约代码大写', 'contract_code': contract_code},
        {'case_name': 'WS订阅K线(sub)-合约代码小写', 'contract_code': str(contract_code).lower()},
        {'case_name': 'WS订阅K线(sub)-合约代码大小写', 'contract_code': contract_code.split('-')[0]+'-usd'}
    ]

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：执行sub订阅'):
            subs = {
                "sub": "market.{}.kline.1min".format(params['contract_code']),
                "id": "id4"
            }
            result = swap_service_ws.swap_sub(subs)
            pass
        with allure.step('验证：返回结果无err信息'):
            assert dict(result).get('err-code') is None  #如果有error即失败
            pass


if __name__ == '__main__':
    pytest.main()
