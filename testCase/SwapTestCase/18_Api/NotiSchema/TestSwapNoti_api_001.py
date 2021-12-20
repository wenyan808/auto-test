#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/16 1:57 下午
# @Author  : HuiQing Yu

from common.mysqlComm import mysqlComm as mysqlClient

import pytest, allure, time
from schema import Schema

from common.SwapServiceAPI import user01
from config.conf import DEFAULT_CONTRACT_CODE,DEFAULT_SYMBOL
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][2])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapNoti_api_001:
    ids = ['TestSwapNoti_api_001']
    params = [{'title':'TestSwapNoti_api_001','case_name': 'restful获取深度'}]

    @classmethod
    def setup_class(cls):
        with allure.step('变量初始化'):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.symbol = DEFAULT_SYMBOL
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['title'])
        with allure.step('操作:执行API'):
            r=user01.swap_depth(contract_code=self.contract_code,type='step0')
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                'ch': f'market.{self.contract_code}.depth.step0',
                'status': 'ok',
                'tick': {
                    'asks': list,
                    'bids': list,
                    'ch': f'market.{self.contract_code}.depth.step0',
                    'id': int,
                    'mrid': int,
                    'ts': int,
                    'version': int
                },
                'ts': int
            }
            Schema(schema).validate(r)