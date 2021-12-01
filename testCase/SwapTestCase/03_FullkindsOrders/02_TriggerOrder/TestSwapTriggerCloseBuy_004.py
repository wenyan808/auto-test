#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211008
# @Author : DongLin Han


import time
from decimal import Decimal

import allure
import pytest

from config.case_content import epic, features
from common.CommonUtils import currentPrice
from common.SwapServiceAPI import user01 as api_user01
from config.conf import DEFAULT_CONTRACT_CODE

@allure.epic(epic[1])
@allure.feature(features[2]['feature'])
@allure.story(features[2]['story'][2])
@allure.tag('Script owner : 韩东林', 'Case owner : 邱大伟')
@pytest.mark.stable
class TestSwapTriggerCloseBuy_004:
    ids = [
        "TestSwapTriggerCloseBuy_004",
        "TestSwapTriggerCloseBuy_005",
        "TestSwapTriggerCloseBuy_006",
        "TestSwapTriggerCloseSell_004",
        "TestSwapTriggerCloseSell_005",
        "TestSwapTriggerCloseSell_006",
        "TestSwapTriggerOpenBuy_004",
        "TestSwapTriggerOpenBuy_005",
        "TestSwapTriggerOpenBuy_006",
        "TestSwapTriggerOpenSell_004",
        "TestSwapTriggerOpenSell_005",
        "TestSwapTriggerOpenSell_006",
    ]
    params = [
        {
            "caseName": "正常限价平仓-平空-触发价大于最新价",
            "order_price_type": "limit",
            "ratio": 1.01,
            "trigger_type": "ge",
            "offset": "close",
            "direction": "buy",
        },{
            "caseName": "正常限价平仓-平空-触发价等于最新价",
            "order_price_type": "limit",
            "ratio": 1.00,
            "trigger_type": "ge",
            "offset": "close",
            "direction": "buy",
        },{
            "caseName": "正常限价平仓-平空-触发价小于最新价",
            "order_price_type": "limit",
            "ratio": 0.99,
            "trigger_type": "le",
            "offset": "close",
            "direction": "buy",
        },{
            "caseName": "正常限价平仓-平多-触发价大于最新价",
            "order_price_type": "limit",
            "ratio": 1.01,
            "trigger_type": "ge",
            "offset": "close",
            "direction": "sell",
        },{
            "caseName": "正常限价平仓-平多-触发价等于最新价",
            "order_price_type": "limit",
            "ratio": 1.00,
            "trigger_type": "ge",
            "offset": "close",
            "direction": "sell",
        },{
            "caseName": "正常限价平仓-平多-触发价小于最新价",
            "order_price_type": "limit",
            "ratio": 0.99,
            "trigger_type": "le",
            "offset": "close",
            "direction": "sell",
        },{
            "caseName": "正常限价开仓-开多-触发价大于最新价",
            "order_price_type": "limit",
            "ratio": 1.01,
            "trigger_type": "ge",
            "offset": "open",
            "direction": "buy",
        },{
            "caseName": "正常限价开仓-开多-触发价等于最新价",
            "order_price_type": "limit",
            "ratio": 1.00,
            "trigger_type": "ge",
            "offset": "open",
            "direction": "buy",
        },{
            "caseName": "正常限价开仓-开多-触发价小于最新价",
            "order_price_type": "limit",
            "ratio": 0.99,
            "trigger_type": "le",
            "offset": "open",
            "direction": "buy",
        },{
            "caseName": "正常限价开仓-开空-触发价大于最新价",
            "order_price_type": "limit",
            "ratio": 1.01,
            "trigger_type": "ge",
            "offset": "open",
            "direction": "sell",
        },{
            "caseName": "正常限价开仓-开空-触发价等于最新价",
            "order_price_type": "limit",
            "ratio": 1.00,
            "trigger_type": "ge",
            "offset": "open",
            "direction": "sell",
        },{
            "caseName": "正常限价开仓-开空-触发价小于最新价",
            "order_price_type": "limit",
            "ratio": 0.99,
            "trigger_type": "le",
            "offset": "open",
            "direction": "sell",
        }
    ]

    @classmethod
    def setup_class(cls):
        with allure.step('变量初始化'):
            cls.latest_price = currentPrice()  # 最新价
            cls.contract_code = DEFAULT_CONTRACT_CODE
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('恢复环境:取消委托'):
            api_user01.swap_trigger_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self,params, contract_code,DB_contract_trade):
        with allure.step('操作：执行下单'):
            trigger_order = api_user01.swap_trigger_order(contract_code=self.contract_code,trigger_type=params['trigger_type'],
                                          volume=1,offset=params['offset'],direction=params['direction'],
                                          order_price_type=params['order_price_type'],trigger_price=round(currentPrice()*params['ratio'],2),
                                          order_price=round(currentPrice()*params['ratio'],2))
            pass
        with allure.step('验证：下单成功'):
            orderId = trigger_order['data']['order_id']
            assert 'ok' in trigger_order['status'] and orderId
            pass
        with allure.step('验证：订单数据与下单数据一致'):
            sqlStr = f'select case t.direction when 1 then "buy" when 2 then "sell" end as direction ,' \
                     f'case t.trigger_type when 1 then "ge" when 2 then "le" end trigger_type,' \
                     f't.trigger_price,t.order_price, t.lever_rate,' \
                     f'case t.offset when 1 then "open" when 2 then "close" end as offset ' \
                     f'from t_trigger_order t ' \
                     f'where user_order_id = {orderId}'
            for i in range(3):
                db_info = DB_contract_trade.execute(sqlStr)[0]
                if len(db_info)==0:
                    print(f'查询为空，第{i}一次重试……')
                    time.sleep(1)
                else:
                    break

            assert params['direction'] in db_info['direction'],'订单方向 买|卖 校验失败'
            assert params['trigger_type'] in db_info['trigger_type'],'触发类型校验失败'
            assert round(Decimal(currentPrice()*params['ratio']),2) == round(db_info['trigger_price'],2),'触发价校验失败'
            assert round(Decimal(currentPrice()*params['ratio']),2) == round(db_info['order_price'],2),'订单价校验失败'
            assert 5 == db_info['lever_rate'],'杠杆位数校验失败'
            assert params['offset'] in db_info['offset'],'订单仓位 开|平 校验失败'
            pass

if __name__ == '__main__':
    pytest.main()
