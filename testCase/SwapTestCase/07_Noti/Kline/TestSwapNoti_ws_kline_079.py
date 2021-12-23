#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211013
# @Author : HuiQing Yu

import allure
import pytest
import time

from common.SwapServiceWS import t as swap_service_ws
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][6])
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_079:

    @allure.title('WS订阅K线(sub) 合约代码为空')
    def test_execute(self, contract_code):
        with allure.step('操作：执行sub订阅'):
            self.toTime = int(time.time())
            self.fromTime = self.toTime - 60 * 3
            subs = {
                "sub": "market. .kline.1min",
                "id": "id4"
            }
            result = swap_service_ws.swap_sub(subs)
            pass
        with allure.step('验证：返回结果提示invalid topic'):
            assert 'invalid topic' in result['err-msg']
            pass

if __name__ == '__main__':
    pytest.main()
