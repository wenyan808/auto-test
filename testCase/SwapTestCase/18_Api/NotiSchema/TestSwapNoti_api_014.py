#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/16 2:09 下午
# @Author  : HuiQing Yu

from common.mysqlComm import mysqlComm as mysqlClient

import pytest, allure, time
from schema import Or, Schema

from common.SwapServiceWS import user01
from config.conf import DEFAULT_CONTRACT_CODE,DEFAULT_SYMBOL
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][2])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapNoti_api_014:
    ids = ['TestSwapNoti_api_014']
    params = [{'title': 'TestSwapNoti_api_014', 'case_name': 'WS K线(req)'}]

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
            self.toTime = int(time.time())
            self.fromTime = self.toTime - 60*10
            subs = {
                "req": "market.{}.kline.1min".format(self.contract_code),
                "id": "id4",
                "from": self.fromTime,
                "to": self.toTime
            }
            r = user01.swap_sub(subs=subs)
            pass
        with allure.step('验证:schema响应字段校验'):
            schema = {
                "id": str,
                "rep": f"market.{self.contract_code}.kline.1min",
                "ts": int,
                "wsid": int,
                "status": "ok",
                "data": [
                    {
                        "id": int,
                        "open": Or(int,float),
                        "close":  Or(int,float),
                        "low":  Or(int,float),
                        "high":  Or(int,float),
                        "amount":  Or(int,float),
                        "vol":  Or(int,float),
                        "count": int
                    }
                ]
            }
            Schema(schema).validate(r)
            pass