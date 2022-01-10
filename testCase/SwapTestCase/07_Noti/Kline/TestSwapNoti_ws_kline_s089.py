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
class TestSwapNoti_ws_kline_s089:

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
            "period": "1min",
            "title": ids[0],
        },
        {
            "case_name": "合约不存在-5min",
            "period": "5min",
            "title": ids[1],
        },
        {
            "case_name": "合约不存在-15min",
            "period": "15min",
            "title": ids[2],
        },
        {
            "case_name": "合约不存在-30min",
            "period": "30min",
            "title": ids[3],
        },
        {
            "case_name": "合约不存在-60min",
            "period": "60min",
            "title": ids[4],
        },
        {
            "case_name": "合约不存在-4hour",
            "period": "4hour",
            "title": ids[5],
        },
        {
            "case_name": "合约不存在-1day",
            "period": "1day",
            "title": ids[6],
        },
        {
            "case_name": "合约不存在-1week",
            "period": "1week",
            "title": ids[7],
        },
        {
            "case_name": "合约不存在-1mon",
            "period": "1mon",
            "title": ids[8],
        }
    ]

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：发送req请求'):
            self.toTime = int(time.time())
            self.fromTime = self.toTime - 60 * 60 * 24
            subs = {
                "req": f"market.BTC-BTC.kline.{params['period']}",
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
