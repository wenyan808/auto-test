#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211013
# @Author : HuiQing Yu

from common.LinearServiceWS import t as linear_service_ws
import pytest, allure, random, time
from config.conf import DEFAULT_CONTRACT_CODE

@allure.epic('正向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('WS订阅K线(sub) 合约代码大写')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestLinearNoti_ws_kline_081:

    contract_code = DEFAULT_CONTRACT_CODE
    ids = ['TestLinearNoti_ws_kline_081',
           'TestLinearNoti_ws_kline_082',
           'TestLinearNoti_ws_kline_083']
    params = [
              {
                "case_name": "大写",
                "contract_code": contract_code
              },
              {
                "case_name": "小写",
                "contract_code": str(contract_code).lower()
              },
              {
                "case_name": "大小写",
                "contract_code": contract_code.split('-')[0]+'-usdt'
              }
            ]

    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self,params):
        with allure.step('发送请求'):
            subs = {
                "sub": "market.{}.kline.1min".format(params['contract_code']),
                "id": "id1"
            }
            result = linear_service_ws.linear_sub(subs)
            pass
        with allure.step('校验结果'):
            # 请求topic校验
            assert 'err-msg' not in result, '返回错误信息'
            pass



if __name__ == '__main__':
    pytest.main()
