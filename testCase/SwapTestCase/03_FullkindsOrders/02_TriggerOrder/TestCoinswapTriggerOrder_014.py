#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : HuiQing Yu

from common.mysqlComm import mysqlComm as mysqlClient

import time
from decimal import Decimal

import allure
import pytest

from tool.SwapTools import SwapTool
from common.SwapServiceAPI import user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic(epic[1])
@allure.feature(features[2]['feature'])
@allure.story(features[2]['story'][2])
@allure.tag('Script owner : 余辉青', 'Case owner : 邱大伟')
@pytest.mark.stable
class TestCoinswapTriggerOrder_014:
    ids = [
        "TestCoinswapTriggerOrder_014",
    ]
    params = [
        {
            "case_name": "计划委托 全部撤销订单",
            "direction": "buy",
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
            user01.swap_trigger_cancelall(contract_code=cls.contract_code)  # 避免用例失败未能撤销订单
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params, mysqlClient):
        allure.dynamic.title(params['case_name'])
        with allure.step("操作：挂单"):
            trigger_order_list = []
            for offset in ['open','close']:
                trigger_order = user01.swap_trigger_order(contract_code=self.contract_code,
                                                          trigger_type='ge',
                                                          trigger_price=round(self.latest_price * 1.01, 2),
                                                          volume=1,
                                                          order_price=round(self.latest_price * 1.01, 2),
                                                          direction=params['direction'],
                                                          offset=offset, order_price_type='limit')
                trigger_order_list.append(trigger_order['data']['order_id'])
            pass
        with allure.step('操作：撤单'):
            for i in range(1,4):
                order_reps = user01.swap_trigger_cancelall(contract_code=self.contract_code)
                if 'ok' in order_reps['status']:
                    break
                else:
                    print(f'撤单失败,第{i}次重试……')
                    time.sleep(1)
            pass
        with allure.step('验证：撤单成功'):
            time.sleep(1)
            for orderId in trigger_order_list:
                sqlStr = f'select t.state ' \
                         f'from t_trigger_order t ' \
                         f'where user_order_id = {orderId} and order_type = 2 '
                db_result = mysqlClient.selectdb_execute(dbSchema='contract_trade',sqlStr=sqlStr)[0]
                assert 'ok' in order_reps['status'], '撤单执行失败'
                assert 6 == db_result['state'],'订单状态校验失败'
            pass


if __name__ == '__main__':
    pytest.main()
