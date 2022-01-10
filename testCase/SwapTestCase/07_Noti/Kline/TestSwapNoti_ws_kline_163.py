#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211013
# @Author : HuiQing Yu

import allure
import pytest
import time

from common.SwapServiceWS import user01 as ws_user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][6])
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_163:
    contract_code = DEFAULT_CONTRACT_CODE
    toTime = int(time.time())
    fromTime = toTime - 60 * 3
    ids = [
        'TestSwapNoti_ws_kline_163',
        'TestSwapNoti_ws_kline_164'
    ]
    params = [
        {'case_name': 'WS请求(req)-from格式不合法', 'subs': {"req": f"market.{contract_code}.kline.1min",
                                                 "id": "id4",
                                                 "from": 'invalid',
                                                 "to": toTime
                                                 }},
        {'case_name': 'WS请求(req)-to格式不合法', 'subs': {"req": f"market.{contract_code}.kline.1min",
                                                    "id": "id4",
                                                    "from": fromTime,
                                                    "to": 'invalid'
                                                    }},
    ]

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
