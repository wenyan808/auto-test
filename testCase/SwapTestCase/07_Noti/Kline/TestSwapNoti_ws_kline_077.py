#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211013
# @Author  : HuiQing Yu

from common.SwapServiceWS import user01 as ws_user01
import pytest, allure, random, time

@allure.epic('反向永续')
@allure.feature('WS订阅')
@allure.story('WS订阅K线(sub)')
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_077:

    @allure.title('WS订阅K线(sub) period为空')
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, contract_code):
        with allure.step('操作：执行sub订阅'):
            subs = {
                "sub": "market.{}.kline.".format(contract_code),
                "id": "id4"
            }
            result = ws_user01.swap_sub(subs)
            pass
        with allure.step('验证:校验返回结果为'):
            assert 'invalid topic' in result['err-msg']
            pass

if __name__ == '__main__':
    pytest.main()
