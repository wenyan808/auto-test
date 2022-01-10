#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/16 1:57 下午
# @Author  : HuiQing Yu

from common.mysqlComm import mysqlComm as mysqlClient

import pytest, allure, time
from schema import Schema
from tool.SwapTools import SwapTool
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
            cls.latest_price = SwapTool.currentPrice(contract_code=cls.contract_code)
            pass
        with allure.step('挂盘'):
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.latest_price * 0.8, 2),
                                  direction='buy')
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.latest_price * 1.2, 2),
                                  direction='sell')
            time.sleep(1)#等待盘口更新

    @classmethod
    def teardown_class(cls):
        with allure.step('恢复环境：撤单'):
            user01.swap_cancelall(contract_code=cls.contract_code)
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