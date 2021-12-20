#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211018
# @Author :  HuiQing Yu

import time

import allure
import pytest

from common.mysqlComm import mysqlComm
from tool.SwapTools import SwapTool
from common.SwapServiceAPI import user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic(epic[1])
@allure.feature(features[5]['feature'])
@allure.story(features[5]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapEx_134:
    ids = ['TestSwapEx_132', 'TestSwapEx_133', 'TestSwapEx_134']
    params = [
        {'case_name': '平空 闪电平仓', 'order_price_type': 'lightning', 'direction': 'buy'},
        {'case_name': '平空 闪电平仓-IOC', 'order_price_type': 'lightning_ioc', 'direction': 'buy'},
        {'case_name': '平空 闪电平仓-FOK', 'order_price_type': 'lightning_fok', 'direction': 'buy'}
    ]

    @classmethod
    def setup_class(cls):
        with allure.step('变量初始化'):
            cls.mysqlClient = mysqlComm()
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.latest_price = SwapTool.currentPrice()
            pass
        with allure.step('*->持仓'):
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.latest_price, 2), direction='sell',
                              volume=10)
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.latest_price, 2), direction='buy',
                              volume=10)
            user01.swap_order(contract_code=cls.contract_code, volume=10, offset='close',
                              price=round(cls.latest_price, 2),
                              direction='sell')
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('恢复环境:取消挂单'):
            user01.swap_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title('撮合 闪电平仓 ' + params['case_name'])
        with allure.step('操作：执行平仓'):
            for i in range(3):
                orderInfo = user01.swap_lightning_close_position(contract_code=self.contract_code, volume=1,
                                                                 direction=params['direction'],
                                                                 order_price_type=params['order_price_type'])
                if 'ok' in orderInfo['status']:
                    break
                else:
                    print(f'盘口未更新，第{i+1}次重试……')
                    time.sleep(1)

            pass
        with allure.step('验证：订单存在撮合结果表'):
            sqlStr = "select count(1) as count from t_exchange_match_result WHERE f_id = " \
                     "(select f_id from t_order_sequence where f_order_id= '%s')" % (orderInfo['data']['order_id'])
            flag = False
            # 给撮合时间，5秒内还未撮合完成则为失败
            for i in range(5):
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
