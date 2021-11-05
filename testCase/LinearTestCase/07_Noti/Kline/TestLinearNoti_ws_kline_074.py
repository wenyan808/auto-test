#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211013
# @Author : HuiQing Yu

from common.LinearServiceWS import t as linear_service_ws
import pytest, allure, random, time

@allure.epic('正向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('WS订阅K线(sub) 合约不存在 ')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestLinearNoti_ws_kline_074:

    ids=['TestLinearNoti_ws_kline_026',
         'TestLinearNoti_ws_kline_032',
         'TestLinearNoti_ws_kline_038',
         'TestLinearNoti_ws_kline_044',
         'TestLinearNoti_ws_kline_050',
         'TestLinearNoti_ws_kline_056',
         'TestLinearNoti_ws_kline_062',
         'TestLinearNoti_ws_kline_068',
         'TestLinearNoti_ws_kline_074']
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
        allure.dynamic.title('WS订阅K线(sub)' + params['period'] + '合约不存在')
        with allure.step('发送请求'):
            self.contract_code = 'BTC-BTC'
            subs = {
                "sub": "market.{}.kline.{}".format(self.contract_code, params['period']),
                "id": "id1"
            }
            result = linear_service_ws.linear_sub(subs)
            pass
        with allure.step('校验响应'):
            # 请求topic校验
            assert 'invalid topic' in result['err-msg']
            pass



if __name__ == '__main__':
    pytest.main()
