#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211013
# @Author : HuiQing Yu

from common.SwapServiceWS import user01 as ws_user01
import pytest, allure, random, time
from config.conf import DEFAULT_CONTRACT_CODE
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][6])
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_147:
    contract_code = DEFAULT_CONTRACT_CODE
    toTime = int(time.time())
    fromTime = toTime - 60 * 3
    ids = [
        'TestSwapNoti_ws_kline_147',
        'TestSwapNoti_ws_kline_165',
        'TestSwapNoti_ws_kline_166',
        'TestSwapNoti_ws_kline_167',
        'TestSwapNoti_ws_kline_168',
        'TestSwapNoti_ws_kline_169'
    ]
    params = [
        {'case_name': 'WS请求(req)-不传to', 'subs': {"req": "market.{}.kline.1min".format(contract_code),
                                                    "id": "id4",
                                                    "from": fromTime
                                                    }},
        {'case_name': 'WS请求(req)-from=0', 'subs': {"req": "market.{}.kline.1min".format(contract_code),
                                                 "id": "id4",
                                                 "from": 0,
                                                 "to": toTime
                                                 }},
        {'case_name': 'WS请求(req)-to=0', 'subs': {"req": "market.{}.kline.1min".format(contract_code),
                                                    "id": "id4",
                                                    "from": fromTime,
                                                    "to": 0
                                                    }},
        {'case_name': 'WS请求(req)-from为空', 'subs': {"req": "market.{}.kline.1min".format(contract_code),
                                                 "id": "id4",
                                                 "from": None,
                                                 "to": toTime
                                                 }},
        {'case_name': 'WS请求(req)-to为空', 'subs': {"req": "market.{}.kline.1min".format(contract_code),
                                                    "id": "id4",
                                                    "from": fromTime,
                                                    "to": None
                                                    }},
        {'case_name': 'WS请求(req)-不传from', 'subs': {"req": "market.{}.kline.1min".format(contract_code),
                                                 "id": "id4",
                                                 "to": toTime
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
            assert 'invalid to' or 'invalid from' in result['err-msg']
            pass


if __name__ == '__main__':
    pytest.main()
