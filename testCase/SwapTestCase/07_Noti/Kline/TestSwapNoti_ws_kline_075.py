#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211013
# @Author :  HuiQing Yu

from common.SwapServiceWS import user01
import pytest, allure, random, time
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][6])
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_075:

    def test_execute(self):
        allure.dynamic.title('WS订阅K线(sub) period不存在 合约不存在')
        with allure.step('操作：执行sub请求'):
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
