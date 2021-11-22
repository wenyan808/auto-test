#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211013
# @Author : HuiQing  Yu

from common.SwapServiceWS import user01 as ws_user01
import pytest, allure, random, time
from config.conf import DEFAULT_CONTRACT_CODE

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('WS请求(req)')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_159:
    contract_code = DEFAULT_CONTRACT_CODE
    ids = [
        'TestSwapNoti_ws_kline_159',
        'TestSwapNoti_ws_kline_160',
    ]
    params = [
        {'case_name': 'WS订阅K线(sub)-period大写', 'period': '1MIN'},
        {'case_name': 'WS订阅K线(sub)-period大小写', 'period': '1MiN'}
    ]

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：执行请求(req)'):
            self.toTime = int(time.time())
            self.fromTime = self.toTime - 60 * 3
            subs = {
                "sub": "market.{}.kline.{}".format(self.contract_code, params['period']),
                "id": "id4"
            }
            result = ws_user01.swap_sub(subs)
            pass
        with allure.step('验证：返回结果正常'):
            assert dict(result).get('err-code') is None  #如果有error即失败
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
