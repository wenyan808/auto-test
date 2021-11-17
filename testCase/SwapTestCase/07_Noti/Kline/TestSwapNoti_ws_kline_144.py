#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211013
# @Author : 
    用例标题
        WS订阅K线(req) 合约代码大写
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        
    优先级
        2
    用例别名
        TestSwapNoti_ws_kline_144
"""

from common.SwapServiceWS import user01 as ws_user01
import pytest, allure, random, time
from config.conf import DEFAULT_CONTRACT_CODE

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('WS请求(req)')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_144:
    contract_code = DEFAULT_CONTRACT_CODE
    ids = [
        'TestSwapNoti_ws_kline_144',
        'TestSwapNoti_ws_kline_145',
        'TestSwapNoti_ws_kline_146'
    ]
    params = [
        {'case_name': 'WS请求(req)-合约代码大写', 'contract_code': contract_code},
        {'case_name': 'WS请求(req)-合约代码小写', 'contract_code': str(contract_code).lower()},
        {'case_name': 'WS请求(req)-合约代码大小写', 'contract_code': contract_code.split('-')[0] + '-usd'}
    ]

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：发送req请求'):
            self.toTime = int(time.time())
            self.fromTime = self.toTime - 60 * 3
            subs = {
                "req": "market.{}.kline.1min".format(params['contract_code']),
                "id": "id4",
                "from": self.fromTime,
                "to": self.toTime
            }
            result = ws_user01.swap_sub(subs)
            pass
        with allure.step('验证：返回结果无err信息'):
            assert dict(result).get('err-code') is None  # 如果有error即失败
            pass


if __name__ == '__main__':
    pytest.main()
