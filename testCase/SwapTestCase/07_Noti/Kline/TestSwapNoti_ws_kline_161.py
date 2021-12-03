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
        'TestSwapNoti_ws_kline_161',
        'TestSwapNoti_ws_kline_162'
    ]
    params = [
        {'case_name': 'WS请求(req)-from>to', 'subs': {"req": "market.{}.kline.1min".format(contract_code),
                                                 "id": "id4",
                                                 "from": toTime,
                                                 "to": fromTime
                                                 }},
        {'case_name': 'WS请求(req)-from=to', 'subs': {"req": "market.{}.kline.1min".format(contract_code),
                                                    "id": "id4",
                                                    "from": fromTime,
                                                    "to": fromTime
                                                    }},
    ]

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self,params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：执行req请求'):
            result = ws_user01.swap_sub(params['subs'])
            pass
        with allure.step('验证：返回结果正常'):
            assert 'ok' in result['status']
            pass


if __name__ == '__main__':
    pytest.main()
