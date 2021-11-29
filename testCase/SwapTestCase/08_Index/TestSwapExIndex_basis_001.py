#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/25 11:25 上午
# @Author  : HuiQing Yu

import time

import allure
import pytest

from common.CommonUtils import currentPrice
from common.SwapServiceWS import user01 as ws_user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic(epic[1])
@allure.feature(features[7])
@allure.story(features[7]['story'][0])
@allure.tag('Script owner : 余辉青', 'Case owner : ')
class TestSwapExIndex_basis_001:
    ids = ['TestSwapExIndex_basis_001']
    params = [{'case_name':'查询基差1min K线','period':'1min'}]

    @classmethod
    def setup_class(cls):
        with allure.step('变量初始化'):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.latest_price = currentPrice()
            pass
        with allure.step(''):
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.skip('因环境问题跳过')
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step(''):
            subs = {
                "sub": "market.{}.basis.{}.open".format(self.contract_code,params['period']),
                "id": "id7"
            }
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(1, 4):
                result = ws_user01.swap_sub_index(subs)
                if 'tick' in result:
                    flag = True
                    break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i))
            assert flag
            pass
