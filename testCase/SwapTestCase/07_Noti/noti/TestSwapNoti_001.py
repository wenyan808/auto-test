#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211009
# @Author : HuiQing Yu

from common.SwapServiceWS import user01 as ws_user01
import pytest, allure, random, time
from config.conf import DEFAULT_CONTRACT_CODE
from common.CommonUtils import retryUtil


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('WebSocket')  # 这里填功能
@allure.story('市场行情')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_001:
    ids = ['TestSwapNoti_001']
    params = [{'case_name': '请求K线', 'type': 'kline'}]
    contract_code = DEFAULT_CONTRACT_CODE
    @classmethod
    def setup_class(cls):
        with allure.step(''):
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.flaky(reruns=3, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self,params):
        with allure.step('执行请求'):
            subs = {
                "sub": "market.{}.{}.1min".format(self.contract_code, params['type']),
                "id": "id1"
            }
            result = retryUtil(ws_user01.swap_sub,subs,'tick')
            pass
        with allure.step('校验返回结果'):
            assert "market.{}.{}.1min".format(self.contract_code, params['type']) == result['ch'], '校验不通过'
            assert 'ts' in result, '校验不通过'
            assert 'tick' in result, '返回结果无tick,校验不通过'
            checked_col = ['id','mrid','open','close','low','high','amount','vol','count']
            for col in checked_col:
                assert result['tick'][col] is not None
            pass



if __name__ == '__main__':
    pytest.main()
