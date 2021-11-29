#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/25 4:08 下午
# @Author  : HuiQing Yu

import allure
import pytest
from common.SwapServiceAPI import user01
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic('反向永续')
@allure.feature('行情')
@allure.story('深度图&Overview')
@allure.tag('Script owner : 余辉青', 'Case owner : ')
@pytest.mark.stable
class TestSwapNoti_restful_overview_001:

    contract_code = DEFAULT_CONTRACT_CODE
    ids = ['TestSwapNoti_restful_overview_001','TestSwapNoti_restful_overview_002']
    params = [{'case_name':'restful请求overview 传合约代码','contract_code':contract_code},
              {'case_name':'restful请求overview 不传合约代码','contract_code':''}]

    @classmethod
    def setup_class(cls):
        with allure.step(''):
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title( params['case_name'])
        with allure.step('操作：执行restful-api请求'):
            result = user01.swap_market_over_view(contract_code=params['contract_code'])
            pass
        with allure.step('验证：返回结果各字段不为空'):
            checked_col = ['open','close','low','high']
            for col in checked_col:
                for data in result['data']:
                    assert data[col],col+'为空校验失败'
            pass