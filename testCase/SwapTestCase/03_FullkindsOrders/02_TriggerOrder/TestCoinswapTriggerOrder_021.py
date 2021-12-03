#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : HuiQing Yu

import time
from decimal import Decimal
import random
import allure
import pytest

from common.CommonUtils import currentPrice
from common.SwapServiceAPI import user01,user02
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic(epic[1])
@allure.feature(features[2]['feature'])
@allure.story(features[2]['story'][2])
@allure.tag('Script owner : 余辉青', 'Case owner : 邱大伟')
@pytest.mark.stable
class TestCoinswapTriggerOrder_020:
    ids = [
        "TestCoinswapTriggerOrder_020",
        "TestCoinswapTriggerOrder_021",
    ]
    params = [
        {
            "case_name": "撤销止盈止损订单",
            "operate_type": "cancel",
        },
        {
            "case_name": "全部撤销止盈止损订单",
            "operate_type": "cancelAll",

        }
    ]

    @classmethod
    def setup_class(cls):
        with allure.step("变量初始化"):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.latest_price = currentPrice()
            pass


    @classmethod
    def teardown_class(cls):
        with allure.step('撤销挂单'):
            user01.swap_cancelall(contract_code=cls.contract_code)  # 避免用例失败未能撤销订单
            user01.swap_tpsl_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params, DB_contract_trade):
        allure.dynamic.title(params['case_name'])
        with allure.step("操作：挂卖盘"):
            user02.swap_order(contract_code=self.contract_code, price=self.latest_price, direction='sell')
            pass
        with allure.step('操作：下限价单并设置止盈'):
            limit_order = user01.swap_order(contract_code=self.contract_code, price=round(self.latest_price, 2),
                                            direction='buy',
                                            tp_order_price=round(self.latest_price * 1.5, 2),
                                            tp_order_price_type='limit',
                                            tp_trigger_price=round(self.latest_price * 1.5, 2))
            pass
        with allure.step('验证：订单成交后，生成止盈单'):
            time.sleep(1)#等待生效数据更新
            limit_order_id = limit_order['data']['order_id']
            sqlStr = f'select count(1) as tpIsExesit,user_order_id from t_tpsl_trigger_order where client_order_id= {limit_order_id}'
            tpsl_order_info = DB_contract_trade.dictCursor(sqlStr)
            assert len(tpsl_order_info),'查无数据,校验失败'
            assert 1 <= tpsl_order_info[0]['tpIsExesit'], '校验生成止盈单失败'
            pass
        with allure.step('操作：撤销止盈订单'):
            if 'cancel' in params['operate_type']:
                user01.swap_tpsl_cancel(contract_code=self.contract_code,order_id=tpsl_order_info[0]['user_order_id'])
            elif 'cancelAll' in params['operate_type']:
                user01.swap_tpsl_cancelall(contract_code=self.contract_code)
            pass
        with allure.step('验证：撤销后订单存在历史订单中'):
            for i in range(3):
                sqlStr = f'select state from t_tpsl_trigger_order where client_order_id= {limit_order_id} and order_type = 2'
                tpsl_order_info = DB_contract_trade.dictCursor(sqlStr)
                if tpsl_order_info==() or tpsl_order_info[0]['state']==2:
                    print(f'校验失败，第{i+1}次重试……')
                    time.sleep(1)
                else:
                    break
            assert 6 == tpsl_order_info[0]['state'], '校验撤销状态失败'
            pass


if __name__ == '__main__':
    pytest.main()
