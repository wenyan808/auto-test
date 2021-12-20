#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : HuiQing Yu

from common.mysqlComm import mysqlComm as mysqlClient

import time
from decimal import Decimal
import random
import allure
import pytest

from tool.SwapTools import SwapTool
from common.SwapServiceAPI import user01,user02
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic(epic[1])
@allure.feature(features[2]['feature'])
@allure.story(features[2]['story'][2])
@allure.tag('Script owner : 余辉青', 'Case owner : 邱大伟')
@pytest.mark.stable
class TestCoinswapTriggerOrder_019:
    ids = [
        "TestCoinswapTriggerOrder_019",
        "TestCoinswapTriggerOrder_020",
    ]
    params = [
        {
            "case_name": "持仓区域下止盈止损正常限价",
            "tp_order_price_type": "limit",
        },
        {
            "case_name": "持仓区域下止盈止损最优5/10/20档",
            "tp_order_price_type": "optimal_{}".format(random.choice([5, 10, 20])),
        }
    ]

    @classmethod
    def setup_class(cls):
        with allure.step("变量初始化"):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.latest_price = SwapTool.currentPrice()
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('撤销挂单'):
            user01.swap_tpsl_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params, mysqlClient):
        allure.dynamic.title(params['case_name'])
        with allure.step("操作：持仓区域下止盈止损单"):
            tpsl_order = user01.swap_tpsl_order(contract_code=self.contract_code,volume=1,direction='sell',tp_order_price=round(self.latest_price*1.5,2),
                                   tp_trigger_price=round(self.latest_price*1.5,2),tp_order_price_type=params['tp_order_price_type'])
            pass
        with allure.step("验证：返回止盈止损单号"):
            tp_order_id = tpsl_order['data']['tp_order']['order_id']
            assert 'ok' in tpsl_order['status'],'下单失败'
            assert tp_order_id,'单号为空校验失败'
            pass
        with allure.step("验证：状态为待委托"):
            time.sleep(1)#等待数据更新
            sqlStr = f'select state from t_tpsl_trigger_order where user_order_id={tp_order_id}'
            db_info = mysqlClient.selectdb_execute(dbSchema='contract_trade',sqlStr=sqlStr)[0]
            assert 2 == db_info['state'],'状态为待委托校验失败'

if __name__ == '__main__':
    pytest.main()
