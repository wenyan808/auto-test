#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/10 4:03 下午
# @Author  : HuiQing Yu
import allure
import pytest
import time
from common.SwapServiceAPI import user01 as api_user01
from common.SwapServiceWS import user01 as ws_user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE
from common.CommonUtils import currentPrice

@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][5])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapNoti_ws_trade_007:
    contract_code = DEFAULT_CONTRACT_CODE
    ids = ['TestSwapNoti_ws_trade_007']
    params =[
              {
                "case_name": "有挂单 无成交",
                "contract_code": contract_code
              }
            ]

    @classmethod
    def setup_class(cls):
        with allure.step('挂单'):
            cls.currentPrice = currentPrice()
            api_user01.swap_order(contract_code=cls.contract_code,price=round(cls.currentPrice*0.5,2),direction='buy')
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('撤单挂单'):
            time.sleep(1)
            api_user01.swap_cancelall(cls.contract_code)
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('执行sub请求'):
            subs = {
                "sub": "market.{}.trade.detail".format(self.contract_code),
                "id": "id1",
            }
            trade_info = ws_user01.swap_sub(subs=subs)
            pass
        with allure.step('验证：返回结果各字段不为空'):
            for d in trade_info['tick']['data']:
                assert d['id']
                assert d['amount']
                assert d['quantity']
                assert d['price']
                assert d['direction']
            pass


