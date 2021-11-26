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
class TestSwapApiSchema_035:

    @allure.title("获取母账户下的所有母子账户划转记录")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_master_sub_transfer_record(contract_code=contract_code,create_date=7, transfer_type='34', page_index=1,
                                                       page_size=1)
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                'data': {
                    'current_page': int,
                    'total_page': int,
                    'total_size': int,
                    'transfer_record': [{
                        'amount': float,
                        'contract_code': contract_code,
                        'id': int,
                        'sub_account_name': str,
                        'sub_uid': str,
                        'symbol': symbol,
                        'transfer_type': 34,
                        'ts': int
                    }]
                },
                'status': 'ok',
                'ts': int
            }
            Schema(schema).validate(r)
            pass
