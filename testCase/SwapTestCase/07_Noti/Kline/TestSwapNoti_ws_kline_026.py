#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211013
# @Author : HuiQing Yu

from common.SwapServiceWS import user01 as ws_user01
import pytest, allure, random, time
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][6])
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_026:

    ids = ['TestSwapNoti_ws_kline_026',
           'TestSwapNoti_ws_kline_032',
           'TestSwapNoti_ws_kline_038',
           'TestSwapNoti_ws_kline_044',
           'TestSwapNoti_ws_kline_050',
           'TestSwapNoti_ws_kline_056',
           'TestSwapNoti_ws_kline_062',
           'TestSwapNoti_ws_kline_068',
           'TestSwapNoti_ws_kline_074']
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

    @pytest.mark.parametrize('param', params, ids=ids)
    def test_execute(self, param):
        allure.dynamic.title(param['case_name'])
        with allure.step('操作：执行sub请求'):
            self.contract_code = 'BTC-BTC'
            subs = {
                "sub": "market.{}.kline.{}".format(self.contract_code, param['period']),
                "id": "id1"
            }
            result = ws_user01.swap_sub(subs=subs)
            pass
        with allure.step('验证：返回结果提示invalid topic'):
            # 请求topic校验
            assert 'invalid topic' in result['err-msg']
            pass



if __name__ == '__main__':
    pytest.main()
