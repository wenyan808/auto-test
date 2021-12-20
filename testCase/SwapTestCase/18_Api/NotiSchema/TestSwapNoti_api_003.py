#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/16 2:09 下午
# @Author  : HuiQing Yu

from common.mysqlComm import mysqlComm as mysqlClient

import pytest, allure, time
from schema import Or, Schema

from common.SwapServiceAPI import user01
from config.conf import DEFAULT_CONTRACT_CODE,DEFAULT_SYMBOL
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][2])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapNoti_api_003:
    ids = ['TestSwapNoti_api_003']
    params = [{'title': 'TestSwapNoti_api_003', 'case_name': 'restful获取批量聚合行情'}]

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
        with allure.step('操作:执行请求'):
            r = user01.swap_batch_merged(contract_code=self.contract_code)
            pass
        with allure.step('验证:schema响应字段校验'):
            schema = {
                'status': 'ok',
                'ticks': [{
                    'contract_code': self.contract_code,
                    'amount': str,
                    'ask': list,
                    'bid': list,
                    'close': str,
                    'count': int,
                    'high': str,
                    'id': int,
                    'low': str,
                    'open': str,
                    'ts': int,
                    'vol': str
                }],
                'ts': int
            }
            Schema(schema).validate(r)
            pass