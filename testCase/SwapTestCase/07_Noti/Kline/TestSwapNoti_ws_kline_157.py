#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211013
# @Author : HuiQing  Yu

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
class TestSwapNoti_ws_kline_157:
    ids = [
        'TestSwapNoti_ws_kline_157',
        'TestSwapNoti_ws_kline_158',
    ]
    params = [
        {'case_name': 'WS订阅K线(req)-period大写', 'period': '1MIN'},
        {'case_name': 'WS订阅K线(req)-period大小写', 'period': '1MiN'}
    ]

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：执行请求(req)'):
            self.contract_code = DEFAULT_CONTRACT_CODE
            self.toTime = int(time.time())
            self.fromTime = self.toTime - 60 * 3
            subs = {
                "req": "market.{}.kline.{}".format(self.contract_code, params['period']),
                "id": "id4",
                "from": self.fromTime,
                "to": self.toTime
            }
            result = ws_user01.swap_sub(subs)
            pass
        with allure.step('验证：返回结果正常'):
            assert dict(result).get('err-code') is None  # 如果有error即失败
            pass


if __name__ == '__main__':
    pytest.main()
