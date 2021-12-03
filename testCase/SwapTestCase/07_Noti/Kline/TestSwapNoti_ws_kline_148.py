#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211013
# @Author : HuiQing Yu

import allure
import pytest
import time

from common.SwapServiceWS import t as swap_service_ws
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][6])
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_148:
    ids = [
        'TestSwapNoti_ws_kline_148',
        'TestSwapNoti_ws_kline_149',
        'TestSwapNoti_ws_kline_150',
        'TestSwapNoti_ws_kline_151',
        'TestSwapNoti_ws_kline_152',
        'TestSwapNoti_ws_kline_153',
    ]
    params = [
        {'case_name': 'WS请求(req)-1min 超2000条数据', 'period': '1min'},
        {'case_name': 'WS请求(req)-5min 超2000条数据', 'period': '5min'},
        {'case_name': 'WS请求(req)-15min 超2000条数据', 'period': '15min'},
        {'case_name': 'WS请求(req)-30min 超2000条数据', 'period': '30min'},
        {'case_name': 'WS请求(req)-60min 超2000条数据', 'period': '60min'},
        {'case_name': 'WS请求(req)-4hour 超2000条数据', 'period': '4hour'},
    ]

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, contract_code,params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：执行req请求'):
            self.toTime = int(time.time())
            self.fromTime = self.toTime - 60 * 60 * 24 * 30 * 12
            subs = {
                "req": "market.{}.kline.{}".format(contract_code, params['period']),
                "id": "id4",
                "from": self.fromTime,
                "to": self.toTime
            }
            result = swap_service_ws.swap_sub(subs)
            pass
        with allure.step('验证：返回结果提示time gap too large'):
            assert 'time gap too large' in result['err-msg']
            pass



if __name__ == '__main__':
    pytest.main()
