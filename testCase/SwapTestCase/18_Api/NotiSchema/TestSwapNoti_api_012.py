#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/16 2:09 下午
# @Author  : HuiQing Yu

import allure
import pytest
import time
from schema import Schema

from common.SwapServiceAPI import user01 as api_user01
from common.SwapServiceWS import user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL
from tool.SwapTools import SwapTool


@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][2])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapNoti_api_012:
    ids = ['TestSwapNoti_api_012']
    params = [{'title': 'TestSwapNoti_api_012', 'case_name': 'WS 增量150档'}]

    @classmethod
    def setup_class(cls):
        with allure.step('变量初始化'):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.symbol = DEFAULT_SYMBOL
            cls.latest_price = SwapTool.currentPrice(contract_code=cls.contract_code)
        with allure.step('挂盘'):
            api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.latest_price * 0.8, 2),
                                  direction='buy')
            api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.latest_price * 1.2, 2),
                                  direction='sell')
            time.sleep(1)  # 等待盘口更新

    @classmethod
    def teardown_class(cls):
        with allure.step('恢复环境：撤单'):
            api_user01.swap_cancelall(contract_code=cls.contract_code)
            pass


    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['title'])
        with allure.step('操作:执行请求'):
            subs = {
                "sub": f"market.{self.contract_code}.depth.size_150.high_freq",
                "data_type": "incremental",
                "id": "id generated by client"
            }
            r = user01.swap_sub(subs=subs)
            pass
        with allure.step('验证:schema响应字段校验'):
            schema = {
                "ch": f"market.{self.contract_code}.depth.size_150.high_freq",
                "tick": {
                    "asks": list,
                    "bids": list,
                    "ch": f"market.{self.contract_code}.depth.size_150.high_freq",
                    "event": "snapshot",
                    "id": int,
                    "mrid": int,
                    "ts": int,
                    "version": int
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass