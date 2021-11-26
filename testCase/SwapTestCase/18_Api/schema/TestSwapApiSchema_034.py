#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from schema import Schema, Or
from common.SwapServiceAPI import user01


@allure.epic('反向永续')
@allure.feature('18API')
@allure.story('schema校验')
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_034:

    @allure.title("母子账户划转")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
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
