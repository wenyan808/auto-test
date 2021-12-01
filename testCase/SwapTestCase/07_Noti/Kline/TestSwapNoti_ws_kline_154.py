#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211013
# @Author : HuiQing Yu

from common.SwapServiceWS import t as swap_service_ws
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order
from tool import atp
from pprint import pprint
import pytest, allure, random, time
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][6])
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_154:
    ids = [
        'TestSwapNoti_ws_kline_154',
        'TestSwapNoti_ws_kline_155',
        'TestSwapNoti_ws_kline_156',
        ]
    params = [
        {'case_name': 'WS请求(req)-1day 超2000条数据', 'period': '1day'},
        {'case_name': 'WS请求(req)-1week 超2000条数据', 'period': '1week'},
        {'case_name': 'WS请求(req)-1mon 超2000条数据', 'period': '1mon'},
    ]

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
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
        with allure.step('验证：返回结果(由于数据原因返回正常即可)'):
            assert  len(result['data'])<2000 and 'ok' in result['status']
            pass



if __name__ == '__main__':
    pytest.main()
