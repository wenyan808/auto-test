#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211013
# @Author :  HuiQing Yu

from common.SwapServiceWS import user01
import pytest, allure, random, time


@allure.epic('反向永续')
@allure.feature('WS订阅')
@allure.story('WS订阅K线(sub)')
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_075:

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self):
        allure.dynamic.title('WS订阅K线(sub) period不存在 合约不存在')
        with allure.step('执行sub请求'):
            self.contract_code = 'BTC-BTC'  # 不存在的合约
            self.period = '1year'  # 不存在的period
            self.toTime = int(time.time())
            self.fromTime = self.toTime - 60 * 3
            subs = {
                "sub": "market.{}.kline.{}".format(self.contract_code, self.period),
                "id": "id4"
            }
            result = user01.swap_sub(subs)
            pass
        with allure.step('验证点：返回结果为invalid topic'):
            assert 'invalid topic' in result['err-msg']
            pass


if __name__ == '__main__':
    pytest.main()
