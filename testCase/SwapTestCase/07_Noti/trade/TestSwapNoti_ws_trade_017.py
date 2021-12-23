#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/10 4:03 下午
# @Author  : HuiQing Yu

from common.mysqlComm import mysqlComm as mysqlClient

import allure
import pytest
import time

from common.SwapServiceWS import user01 as ws_user01
from common.SwapServiceAPI import user01 as api_user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE
from tool.SwapTools import SwapTool


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][5])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapNoti_ws_trade_017:
    contract_code = DEFAULT_CONTRACT_CODE
    ids = [
            'TestSwapNoti_ws_trade_017',
            'TestSwapNoti_ws_trade_018',
            'TestSwapNoti_ws_trade_019',
            'TestSwapNoti_ws_trade_020',
            'TestSwapNoti_ws_trade_021']
    params =[
              {
                "case_name": "限价单成交",
                "order_price_type": "limit",
                "contract_code": contract_code
              },{
                "case_name": "对手价成交",
                "order_price_type": "opponent",
                "contract_code": contract_code
              },{
                "case_name": "最优5档成交",
                "order_price_type": "optimal_5",
                "contract_code": contract_code
              },{
                "case_name": "最优10档成交",
                "order_price_type": "optimal_10",
                "contract_code": contract_code
              },{
                "case_name": "最优20档成交",
                "order_price_type": "optimal_20",
                "contract_code": contract_code
              }
            ]

    @classmethod
    def setup_class(cls):
        with allure.step('挂盘口'):
            cls.currentPrice = SwapTool.currentPrice()
            api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2),direction='sell',volume=10)
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('撤盘口'):
            api_user01.swap_cancelall(cls.contract_code)
            pass

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
                "sub": "market.{}.trade.detail".format(self.contract_code),
                "id": "id1",
            }
            trade_info = ws_user01.swap_sub(subs=subs,keyword='tick')
            pass
        with allure.step('验证:返回结果各字段不为空'):
            for d in trade_info['tick']['data']:
                assert d['id']
                assert d['amount']
                assert d['quantity']
                assert d['price']
                assert d['direction']
            pass


