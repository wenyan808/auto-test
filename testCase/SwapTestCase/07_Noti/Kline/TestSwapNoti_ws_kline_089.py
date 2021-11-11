#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211014
# @Author : HuiQing Yu
from common.LinearServiceWS import t as linear_service_ws
import pytest, allure, random, time

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('WS订阅K线(req) 合约不存在')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_089:

    ids = ['TestSwapNoti_ws_kline_089',
           'TestSwapNoti_ws_kline_095',
           'TestSwapNoti_ws_kline_101',
           'TestSwapNoti_ws_kline_107',
           'TestSwapNoti_ws_kline_113',
           'TestSwapNoti_ws_kline_119',
           'TestSwapNoti_ws_kline_125',
           'TestSwapNoti_ws_kline_131',
           'TestSwapNoti_ws_kline_137']
    params = [
        {
            "case_name": "1min",
            "period": "1min"
        },
        {
            "case_name": "5min",
            "period": "5min"
        },
        {
            "case_name": "15min",
            "period": "15min"
        },
        {
            "case_name": "30min",
            "period": "30min"
        },
        {
            "case_name": "60min",
            "period": "60min"
        },
        {
            "case_name": "4hour",
            "period": "4hour"
        },
        {
            "case_name": "1day",
            "period": "1day"
        },
        {
            "case_name": "1week",
            "period": "1week"
        },
        {
            "case_name": "1mon",
            "period": "1mon"
        }
    ]

    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title('WS订阅K线(req)' + params['period'] + '合约不存在')
        with allure.step('发送请求'):
            self.contract_code = 'BTC-BTC'
            self.toTime = int(time.time())
            self.fromTime = self.toTime - 60 * 60 * 24
            subs = {
                "req": "market.{}.kline.{}".format(self.contract_code, params['period']),
                "id": "id4",
                "from": self.fromTime,
                "to": self.toTime
            }
            result = linear_service_ws.linear_sub(subs)
            pass
        with allure.step('校验返回'):
            assert 'invalid topic' in result['err-msg']
            pass


if __name__ == '__main__':
    pytest.main()
