#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211018
# @Author : HuiQing
import time

import allure
import pytest

from common.SwapServiceAPI import user01
from common.mysqlComm import mysqlComm
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL
from tool.SwapTools import SwapTool


@allure.epic(epic[1])
@allure.feature(features[5]['feature'])
@allure.story(features[5]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapEx_004:

    ids = ["TestSwapEx_004",
               "TestSwapEx_008",
               "TestSwapEx_012",
               "TestSwapEx_016",
               "TestSwapEx_020",
               "TestSwapEx_024",
               "TestSwapEx_028",
               "TestSwapEx_032",
               "TestSwapEx_036",
               "TestSwapEx_040",
               "TestSwapEx_044",
               "TestSwapEx_048",
               "TestSwapEx_052",
               "TestSwapEx_056",
               "TestSwapEx_060",
               "TestSwapEx_064"]
    params = [
        {
            "case_name": "限价单",
            "order_price_type": "limit"
        },
        {
            "case_name": "对手价",
            "order_price_type": "opponent"
        },
        {
            "case_name": "做maker单",
            "order_price_type": "post_only"
        },
        {
            "case_name": "最优5档",
            "order_price_type": "optimal_5"
        },
        {
            "case_name": "最优10档",
            "order_price_type": "optimal_10"
        },
        {
            "case_name": "最优20档",
            "order_price_type": "optimal_20"
        },
        {
            "case_name": "IOC单",
            "order_price_type": "ioc"
        },
        {
            "case_name": "fok单",
            "order_price_type": "fok"
        },
        {
            "case_name": "对手价IOC",
            "order_price_type": "opponent_ioc"
        },
        {
            "case_name": "对手价FOK",
            "order_price_type": "opponent_fok"
        },
        {
            "case_name": "最优5档IOC",
            "order_price_type": "optimal_5_ioc"
        },
        {
            "case_name": "最优10档IOC",
            "order_price_type": "optimal_10_ioc"
        },
        {
            "case_name": "最优20档IOC",
            "order_price_type": "optimal_20_ioc"
        },
        {
            "case_name": "最优5档FOK",
            "order_price_type": "optimal_5_fok"
        },
        {
            "case_name": "最优10档FOK",
            "order_price_type": "optimal_10_fok"
        },
        {
            "case_name": "最优20档FOK",
            "order_price_type": "optimal_20_fok"
        }
    ]
    isExecute = False

    @classmethod
    def setup_class(cls):
        with allure.step('变量初始化'):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.latest_price = SwapTool.currentPrice()
            cls.symbol = DEFAULT_SYMBOL
            cls.mysqlClient = mysqlComm()
            pass
        with allure.step('挂盘'):
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.latest_price, 2), direction='buy',
                              volume=40)
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.latest_price, 2), direction='sell',
                              volume=20)
            pass


    @classmethod
    def teardown_class(cls):
        with allure.step('*->恢复环境:取消挂单'):
            user01.swap_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self,params):
        with allure.step('操作：卖出平仓'):
            orderInfo = user01.swap_order(contract_code=self.contract_code, price=round(self.latest_price, 2),
                                          direction='sell',
                                          offset='close', order_price_type=params['order_price_type'])
            pass
        with allure.step('验证：订单在撮合结果表中'):
            orderId = orderInfo['data']['order_id_str']
            sqlStr = f'select count(1) as count from t_exchange_match_result ' \
                     f'WHERE f_id = (select f_id from t_order_sequence where f_order_id= {orderId})'
            flag = False
            # 给撮合时间，5秒内还未撮合完成则为失败
            for i in range(3):
                isMatch = self.mysqlClient.selectdb_execute(dbSchema='order_seq',sqlStr=sqlStr)[0]['count']
                if 1 == isMatch:
                    flag = True
                    break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i))
            assert flag
            pass


if __name__ == '__main__':
    pytest.main()
