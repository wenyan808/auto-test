#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211013
# @Author : HuiQing Yu
from common.SwapServiceWS import t as swap_service_ws
import pytest, allure, random, time


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('WS订阅(sub)')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_078:

    @allure.title('WS订阅K线(sub) 不传period')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('操作：执行sub订阅'):
            self.contract_code = contract_code  # 不存在的合约
            self.toTime = int(time.time())
            self.fromTime = self.toTime - 60 * 3
            subs = {
                "sub": "market.{}.kline".format(self.contract_code),
                "id": "id4"
            }
            result = swap_service_ws.swap_sub(subs)
            pass
        with allure.step('验证：返回结果提示invalid topic'):
            assert 'invalid topic' in result['err-msg']
            pass


if __name__ == '__main__':
    pytest.main()
