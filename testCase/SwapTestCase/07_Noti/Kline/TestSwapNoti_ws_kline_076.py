#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211013
# @Author :  HuiQing Yu

from common.SwapServiceWS import user01 as ws_user01
import pytest, allure, random, time


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('WS订阅K线(sub)')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_076:

    @allure.title('WS订阅K线(sub) period不存在 合约正确')
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self,contract_code):
        with allure.step('执行sub请求'):
            self.period = '1year'  # 不存在的period
            subs = {
                "sub": "market.{}.kline.{}".format(contract_code, self.period),
                "id": "id4"
            }
            result = ws_user01.swap_sub(subs)
            pass
        with allure.step('验证点：校验返回结果为invalid topic'):
            assert 'invalid topic' in result['err-msg']
            pass



if __name__ == '__main__':
    pytest.main()
