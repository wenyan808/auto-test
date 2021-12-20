#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

from common.mysqlComm import mysqlComm as mysqlClient

import pytest, allure, random, time
from schema import Schema, Or
from common.SwapServiceAPI import user01
from config.case_content import epic,features

@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_034:

    @allure.title("母子账户划转")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_master_sub_transfer(contract_code=contract_code,sub_uid='115395803',amount=100,
                                                type='master_to_sub')
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                'data': {
                    'order_id': str
                },
                'status': 'ok',
                'ts': int
            }
            Schema(schema).validate(r)
            pass
