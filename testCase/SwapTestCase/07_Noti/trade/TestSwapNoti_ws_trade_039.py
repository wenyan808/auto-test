#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/10 4:03 下午
# @Author  : yuhuiqing
from tool.atp import ATP
import pytest, allure, random, time
from common.SwapServiceWS import user01
from common.SwapServiceAPI import user01 as api_user01
from config.conf import DEFAULT_CONTRACT_CODE
from common.CommonUtils import currentPrice

@allure.epic('反向永续')
@allure.feature('行情')
@allure.story('成交')
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapNoti_ws_trade_039:
    contract_code = DEFAULT_CONTRACT_CODE
    ids = [
            'TestSwapNoti_ws_trade_039',
            'TestSwapNoti_ws_trade_040',
            'TestSwapNoti_ws_trade_041',
            'TestSwapNoti_ws_trade_042',
            'TestSwapNoti_ws_trade_043']
    params =[
              {
                "case_name": "限价单成交",
                "order_price_type": "limit"
              },{
                "case_name": "对手价成交",
                "order_price_type": "opponent"
              },{
                "case_name": "最优5档成交",
                "order_price_type": "optimal_5"
              },{
                "case_name": "最优10档成交",
                "order_price_type": "optimal_10"
              },{
                "case_name": "最优20档成交",
                "order_price_type": "optimal_20"
              }
            ]

    @classmethod
    def setup_class(cls):
        with allure.step('挂盘口'):
            cls.currentPrice = currentPrice()
            api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2),direction='sell',volume=10)
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('撤盘口'):
            api_user01.swap_cancelall(cls.contract_code)
            pass

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('执行'+params['case_name']):
            api_user01.swap_order(contract_code=self.contract_code, price=round(self.currentPrice, 2),
                                  order_price_type=params['order_price_type'],direction='buy')

            pass
        with allure.step('执行sub请求'):
            time.sleep(1)
            subs = {
                "req": "market.{}.trade.detail".format(self.contract_code),
                "size":10,
                "id": "id1",
            }
            trade_info = user01.swap_sub(subs=subs)
            pass
        with allure.step('验证:返回结果各字段不为空'):
            for d in trade_info['data']:
                assert d['id']
                assert d['amount']
                assert d['quantity']
                assert d['price']
                assert d['direction']
            pass


