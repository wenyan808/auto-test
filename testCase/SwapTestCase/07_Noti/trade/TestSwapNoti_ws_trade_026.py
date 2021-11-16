#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/10 4:03 下午
# @Author  : yuhuiqing
from tool.atp import ATP
import pytest, allure, random, time
from common.mysqlComm import orderSeq as DB_orderSeq
from common.SwapServiceWS import user01
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic('反向永续')
@allure.feature('行情')
@allure.story('成交')
@allure.tag('Script owner : 余辉青', 'Case owner : ')
@pytest.mark.stable
class TestSwapNoti_ws_trade_026:
    contract_code = DEFAULT_CONTRACT_CODE
    ids = ['TestSwapNoti_ws_trade_026',
           'TestSwapNoti_ws_trade_027',
           'TestSwapNoti_ws_trade_028']
    params =[
              {
                "case_name": "大写",
                "contract_code": contract_code
              },
              {
                "case_name": "小写",
                "contract_code": str(contract_code).lower()
              },
              {
                "case_name": "大小写",
                "contract_code": contract_code.split('-')[0]+'-usdt'
              }
            ]

    @classmethod
    def setup_class(cls):
        with allure.step(''):
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title('' + params['case_name'])
        with allure.step('执行req请求'):
            subs = {
                "req": "market.{}.trade.detail".format(self.contract_code),
                "size":10,
                "id": "id1",
            }
            trade_info = user01.swap_sub(subs=subs)
            pass
        with allure.step('验证返回'):
            for d in trade_info['data']:
                assert d['id'] is not None
                assert d['amount'] is not None
                assert d['quantity'] is not None
                assert d['price'] is not None
                assert d['direction'] is not None
            pass


