#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/10 4:03 下午
# @Author  : yuhuiqing
from tool.atp import ATP
import pytest, allure, random, time
from common.SwapServiceWS import user01
from common.SwapServiceAPI import user01 as api_user01
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic('反向永续')
@allure.feature('行情')
@allure.story('成交')
@allure.tag('Script owner : 余辉青', 'Case owner : ')
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
            cls.currentPrice = ATP.get_current_price()
            api_user01.swap_order(contract_code=cls.contract_code,price=round(cls.currentPrice*0.5,2),direction='buy')
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('撤单挂单'):
            time.sleep(1)
            api_user01.swap_cancelall(cls.contract_code)
            pass

    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title('' + params['case_name'])
        with allure.step('执行sub请求'):
            subs = {
                "sub": "market.{}.trade.detail".format(self.contract_code),
                "id": "id1",
            }
            trade_info = user01.swap_sub(subs=subs)
            pass
        with allure.step('验证返回'):
            for d in trade_info['tick']['data']:
                assert d['id'] is not None
                assert d['amount'] is not None
                assert d['quantity'] is not None
                assert d['price'] is not None
                assert d['direction'] is not None
            pass


