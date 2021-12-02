#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/25 4:08 下午
# @Author  : HuiQing Yu

import allure
import pytest

from common.SwapServiceAPI import user01
from config.conf import DEFAULT_CONTRACT_CODE
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][2])
@allure.tag('Script owner : 余辉青', 'Case owner : ')
@pytest.mark.stable
class TestSwapNoti_restful_overview_004:

    contract_code = DEFAULT_CONTRACT_CODE
    ids = ['TestSwapNoti_restful_overview_004','TestSwapNoti_restful_overview_007']
    params = [
              {'case_name':'restful请求detail接口 不传参合约代码','contract_code':'','exceptMsg':'contract_code cannot be empty'},
              {'case_name':'restful请求detail接口 合约代码不存在','contract_code':'usd-usd','exceptMsg':'invalid contract code'},
              ]

    @classmethod
    def setup_class(cls):
        with allure.step(''):
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title( params['case_name'])
        with allure.step('操作：执行restful-api请求'):
            result = user01.swap_detail_merged(contract_code=params['contract_code'])
            pass
        with allure.step('验证：返回结果错误提示'):
            assert 'invalid-request' in result['err-code']
            assert params['exceptMsg'] in result['err-msg']
            pass