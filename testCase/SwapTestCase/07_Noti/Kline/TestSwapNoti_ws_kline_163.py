#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211013
# @Author : HuiQing Yu

from common.SwapServiceWS import user01 as ws_user01
import pytest, allure, random, time
from config.conf import DEFAULT_CONTRACT_CODE

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('WS请求(req)')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_147:
    contract_code = DEFAULT_CONTRACT_CODE
    toTime = int(time.time())
    fromTime = toTime - 60 * 3
    ids = [
        'TestSwapNoti_ws_kline_163',
        'TestSwapNoti_ws_kline_164'
    ]
    params = [
        {'case_name': 'WS请求(req)-from格式不合法', 'subs': {"req": "market.{}.kline.1min".format(contract_code),
                                                 "id": "id4",
                                                 "from": 'invalid',
                                                 "to": toTime
                                                 }},
        {'case_name': 'WS请求(req)-to格式不合法', 'subs': {"req": "market.{}.kline.1min".format(contract_code),
                                                    "id": "id4",
                                                    "from": fromTime,
                                                    "to": 'invalid'
                                                    }},
    ]

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self,params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：执行req请求'):
            result = ws_user01.swap_sub(params['subs'])
            pass
        with allure.step('验证：返回结果提示invalid to(from)'):
            assert 'Connection is already closed' in result['msg']
            pass


if __name__ == '__main__':
    pytest.main()
