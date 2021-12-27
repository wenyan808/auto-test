#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211009
# @Author : HuiQing Yu

from common.SwapServiceWS import user01 as ws_user01
import pytest, allure, random, time
from config.conf import DEFAULT_CONTRACT_CODE
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][0])
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

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self,params):
        with allure.step('操作：执行sub请求'):
            subs = {
                "sub": "market.{}.{}.1min".format(self.contract_code, params['type']),
                "id": "id1"
            }
            result = ws_user01.swap_sub(subs=subs, keyword='tick')
            assert 'tick' in result,'未返回预期结果'
            pass
        with allure.step('验证：返回结果字段ch为请求topic'):
            assert "market.{}.{}.1min".format(self.contract_code, params['type']) == result['ch'], '校验不通过'
            pass
        with allure.step('验证：返回结果字段ts不为空'):
            assert 'ts' in result, '校验不通过'
            pass
        with allure.step('验证：返回结果字段tick不为空'):
            assert 'tick' in result, '返回结果无tick,校验不通过'
            pass
        with allure.step('验证：返回结果字段tick下的其他字段不为空'):
            checked_col = ['id','mrid','open','close','low','high','amount','vol','count']
            for col in checked_col:
                assert result['tick'][col] or result['tick'][col] == 0
            pass



if __name__ == '__main__':
    pytest.main()
