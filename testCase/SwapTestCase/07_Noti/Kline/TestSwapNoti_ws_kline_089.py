#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211014
# @Author : HuiQing Yu
from common.SwapServiceWS import user01 as ws_user01
import pytest, allure, random, time
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][6])
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
            "case_name": "合约不存在-1min",
            "period": "1min"
        },
        {
            "case_name": "合约不存在-5min",
            "period": "5min"
        },
        {
            "case_name": "合约不存在-15min",
            "period": "15min"
        },
        {
            "case_name": "合约不存在-30min",
            "period": "30min"
        },
        {
            "case_name": "合约不存在-60min",
            "period": "60min"
        },
        {
            "case_name": "合约不存在-4hour",
            "period": "4hour"
        },
        {
            "case_name": "合约不存在-1day",
            "period": "1day"
        },
        {
            "case_name": "合约不存在-1week",
            "period": "1week"
        },
        {
            "case_name": "合约不存在-1mon",
            "period": "1mon"
        }
    ]

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：发送req请求'):
            self.contract_code = 'BTC-BTC'
            self.toTime = int(time.time())
            self.fromTime = self.toTime - 60 * 60 * 24
            subs = {
                "req": "market.{}.kline.{}".format(self.contract_code, params['period']),
                "id": "id4",
                "from": self.fromTime,
                "to": self.toTime
            }
            result = ws_user01.swap_sub(subs)
            pass
        with allure.step('验证：返回结果提示invalid topic'):
            assert 'invalid topic' in result['err-msg']
            pass


if __name__ == '__main__':
    pytest.main()
