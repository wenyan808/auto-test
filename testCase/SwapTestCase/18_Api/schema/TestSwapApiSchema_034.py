#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu
from pprint import pprint

import allure
import pytest
from schema import Schema

from common.SwapServiceAPI import user01
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_034:

    @allure.title("母子账户划转")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            a = user01.swap_sub_account_list(contract_code=contract_code)
            sub_uid = a['data'][0]['sub_uid']
            r = user01.swap_master_sub_transfer(contract_code=contract_code, sub_uid=sub_uid, amount=1,
                                                type='master_to_sub')
            pprint(r)
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
