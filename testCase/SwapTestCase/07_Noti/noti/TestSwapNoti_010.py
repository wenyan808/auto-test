#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211011
# @Author : DongLin Han

from common.SwapServiceAPI import user01 as api_user01
import pytest, allure, random, time


@allure.epic('反向永续')
@allure.feature('行情')
@allure.story('请求K线')
@allure.tag('Script owner : 韩东林', 'Case owner : 柳攀峰')
@pytest.mark.stable
class TestSwapNoti_010:

    @allure.title('请求K线(传参from,to)')
    @pytest.mark.flaky(reruns=3, reruns_delay=1)
    def test_execute(self, contract_code):
        with allure.step('操作：执行api-restful请求'):
            toTime = int(time.time())
            formTime = toTime - 60 * 60
            result = api_user01.swap_kline(contract_code=contract_code, period='1min', From=formTime, to=toTime)
            pass
        with allure.step('验证：返回结果data下所有字段不为空'):
            checked_col = ['amount', 'close', 'count', 'high', 'id', 'low', 'open', 'vol']
            for data in result['data']:
                for col in checked_col:
                    assert data[col] is not None,str(col)+'为None,不符合预期'


if __name__ == '__main__':
    pytest.main()
