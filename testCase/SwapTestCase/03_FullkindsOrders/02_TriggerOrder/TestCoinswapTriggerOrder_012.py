#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : HuiQing Yu

import time
from decimal import Decimal

import allure
import pytest

from common.CommonUtils import currentPrice
from common.SwapServiceAPI import user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic(epic[1])
@allure.feature(features[2]['feature'])
@allure.story(features[2]['story'][2])
@allure.tag('Script owner : 余辉青', 'Case owner : 邱大伟')
@pytest.mark.stable
class TestCoinswapTriggerOrder_012:
    ids = [
        "TestCoinswapTriggerOrder_012",
        "TestCoinswapTriggerOrder_013",
    ]
    params = [
        {
            "case_name": "计划委托 撤销开仓订单",
            "direction": "buy",
            "offset": "open",
        },
        {
            "case_name": "计划委托 撤销平仓订单",
            "direction": "sell",
            "offset": "close",
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
            user01.swap_trigger_cancelall(contract_code=cls.contract_code)  # 避免用例失败未能撤销订单
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params, DB_contract_trade):
        allure.dynamic.title(params['case_name'])
        with allure.step("操作：挂单"):
            trigger_order = user01.swap_trigger_order(contract_code=self.contract_code,
                                                      trigger_type='ge',
                                                      trigger_price=round(self.latest_price * 1.01, 2),
                                                      volume=1,
                                                      order_price=round(self.latest_price * 1.01, 2),
                                                      direction=params['direction'],
                                                      offset=params['offset'], order_price_type='limit')
            pass
        with allure.step('操作：撤单'):
            orderId = trigger_order['data']['order_id']
            order_reps = user01.swap_trigger_cancel(contract_code=self.contract_code, order_id=orderId)
            pass
        with allure.step('验证：撤单成功'):
            time.sleep(1)
            sqlStr = f'select t.state ' \
                     f'from t_trigger_order t ' \
                     f'where user_order_id = {orderId} and order_type = 2 '
            db_result = DB_contract_trade.dictCursor(sqlStr)[0]
            assert 'ok' in order_reps['status'], '撤单执行失败'
            assert 6 == db_result['state'],'订单状态校验失败'
            pass


if __name__ == '__main__':
    pytest.main()
