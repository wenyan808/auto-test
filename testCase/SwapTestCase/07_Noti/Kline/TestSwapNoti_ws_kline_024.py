#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211013
# @Author : HuiQing Yu

from common.SwapServiceWS import user01 as ws_user01
import pytest, allure, random, time
from config.case_content import epic, features
from tool.SwapTools import SwapTool


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][6])
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_024:

    ids = ['TestSwapNoti_ws_kline_024',
           'TestSwapNoti_ws_kline_030',
           'TestSwapNoti_ws_kline_036',
           'TestSwapNoti_ws_kline_042',
           'TestSwapNoti_ws_kline_048',
           'TestSwapNoti_ws_kline_054',
           'TestSwapNoti_ws_kline_060',
           'TestSwapNoti_ws_kline_066',
           'TestSwapNoti_ws_kline_072']
    params = [
              {
                "case_name": "合约交割中-1min",
                "period": "1min"
              },
              {
                "case_name": "合约交割中-5min",
                "period": "5min"
              },
              {
                "case_name": "合约交割中-15min",
                "period": "15min"
              },
              {
                "case_name": "合约交割中-30min",
                "period": "30min"
              },
              {
                "case_name": "合约交割中-60min",
                "period": "60min"
              },
              {
                "case_name": "合约交割中-4hour",
                "period": "4hour"
              },
              {
                "case_name": "合约交割中-1day",
                "period": "1day"
              },
              {
                "case_name": "合约交割中-1week",
                "period": "1week"
              },
              {
                "case_name": "合约交割中-1mon",
                "period": "1mon"
              }
            ]


    @classmethod
    def setup_class(cls):
        with allure.step(''):
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.parametrize('param', params, ids=ids)
    def test_execute(self, param):
        allure.dynamic.title(param['case_name'])
        with allure.step('操作：执行sub请求'):
            contract_info = SwapTool.getContractStatus(trade_status=4)
            if contract_info['isSkip']:
                assert False,'未找到交割中合约'
        with allure.step('操作：执行sub请求'):
            self.contract_code = contract_info['data']['instrument_index_code']
            subs = {
                "sub": "market.{}.kline.{}".format(self.contract_code, param['period']),
                "id": "id1"
            }
            result = ws_user01.swap_sub(subs=subs)
            pass
        with allure.step('校验返回结果'):
            assert result['subbed'] == "market." + self.contract_code + ".kline." + param['period'],'请求topic校验失败'
            assert 'tick' not in result,'tick-校验失败'
            pass



if __name__ == '__main__':
    pytest.main()
