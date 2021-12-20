#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : HuiQing Yu

from common.mysqlComm import mysqlComm as mysqlClient
from decimal import Decimal

import allure
import pytest
import time
import random

from config.case_content import epic, features
from common.SwapServiceAPI import user01
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL
from tool.SwapTools import SwapTool


@allure.epic(epic[1])
@allure.feature(features[2]['feature'])
@allure.story(features[2]['story'][2])
@allure.tag('Script owner : 余辉青', 'Case owner : 邱大伟')
@pytest.mark.stable
class TestCoinswapTriggerOrder_010:
    ids = [
        "TestCoinswapTriggerOrder_010",
        "TestCoinswapTriggerOrder_011",
    ]
    params = [
        {
            "case_name": "计划委托 触发开仓订单-测试",
            "direction":"buy",
            "offset":"open",
            "ratio": 1.01,
            "trigger_type":"ge"
        },
        {
            "case_name": "计划委托 触发平仓订单-测试",
            "direction": "sell",
            "offset": "close",
            "ratio": 1.01,
            "trigger_type":"ge"
        }
    ]

    @classmethod
    def setup_class(cls):
        with allure.step("变量初始化"):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.latest_price = SwapTool.currentPrice()
            pass
        with allure.step("持仓"):
            user01.swap_order(contract_code=cls.contract_code,price=cls.latest_price,direction='buy',volume=3)
            user01.swap_order(contract_code=cls.contract_code,price=cls.latest_price,direction='sell',volume=3)
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('撤销挂单'):
            user01.swap_trigger_cancelall(contract_code=cls.contract_code)  # 避免用例失败未能撤销订单
            user01.swap_cancelall(contract_code=cls.contract_code)  # 避免用例失败未能撤销订单
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：下单'):
            order_reps = user01.swap_trigger_order(contract_code=self.contract_code, trigger_type=params['trigger_type'],
                                                trigger_price=round(self.latest_price * params['ratio'], 2),volume=1,
                                                order_price=round(self.latest_price * params['ratio'],2),direction=params['direction'],
                                                offset=params['offset'],order_price_type='limit' )
            pass
        with allure.step('验证：下单成功'):
            orderId = order_reps['data']['order_id']
            assert 'ok' in order_reps['status'] and orderId
            pass
        with allure.step('验证：订单信息与下单数据一致'):
            sqlStr = f'select case t.direction when 1 then "buy" when 2 then "sell" end as direction ,' \
                     f'case t.trigger_type when 1 then "ge" when 2 then "le" end trigger_type,' \
                     f't.trigger_price,t.order_price, t.lever_rate,' \
                     f'case t.offset when 1 then "open" when 2 then "close" end as offset ' \
                     f'from t_trigger_order t ' \
                     f'where user_order_id = {orderId}'
            for i in range(3):
                db_info_list = mysqlClient.selectdb_execute(dbSchema='contract_trade',sqlStr=sqlStr)
                if len(db_info_list) == 0:
                    print(f'查询为空，第{i}一次重试……')
                    time.sleep(1)
                else:
                    break
            for db_info in db_info_list:
                assert params['direction'] in db_info['direction'], '订单方向 买|卖 校验失败'
                assert params['trigger_type'] in db_info['trigger_type'], '触发类型校验失败'
                assert round(Decimal(currentPrice() * params['ratio']), 2) == round(db_info['trigger_price'],
                                                                                    2), '触发价校验失败'
                assert round(Decimal(currentPrice() * params['ratio']), 2) == round(db_info['order_price'],
                                                                                    2), '订单价校验失败'
                assert 5 == db_info['lever_rate'], '杠杆位数校验失败'
                assert params['offset'] in db_info['offset'], '订单仓位 开|平 校验失败'
            pass

        with allure.step('操作：成交使最新价更新到触发价'):
            user01.swap_order(contract_code=self.contract_code, price=round(self.latest_price * params['ratio'], 2), direction='buy', volume=3)
            user01.swap_order(contract_code=self.contract_code, price=round(self.latest_price * params['ratio'], 2), direction='sell', volume=3)
            pass
        with allure.step('验证：委托单被触发'):
            for i in range(3):
                sqlStr = f'select t.state,t.order_id,t.triggered_at ' \
                         f'from t_trigger_order t ' \
                         f'where user_order_id = {orderId}'
                is_trigger = mysqlClient.selectdb_execute(dbSchema='contract_trade',sqlStr=sqlStr)[0]
                if is_trigger['state'] == 2:
                    print(f'校验失败，第{i+1}次重试……')
                    time.sleep(1)
                else:
                    break

            assert is_trigger['state'] == 4,'订单状态未更新'
            assert is_trigger['order_id'] != -1,'触发后限价单号未更新'
            assert is_trigger['triggered_at'],'触发时间示未更新'
            pass
        with allure.step('验证：生成了限价单'):
            print('waiting to finish……')
            pass

if __name__ == '__main__':
    pytest.main()
