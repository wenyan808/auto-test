#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211018
# @Author :  HuiQing Yu

import allure
import pytest
import time

from common.SwapServiceAPI import user01
from config.conf import DEFAULT_CONTRACT_CODE
from common.CommonUtils import currentPrice
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[5]['feature'])
@allure.story(features[5]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapEx_127:

    ids = ['TestSwapEx_129', 'TestSwapEx_128', 'TestSwapEx_127']
    params = [
                {'case_name':'平多 闪电平仓','order_price_type':'lightning','direction':'sell'},
                {'case_name':'平多 闪电平仓-IOC','order_price_type':'lightning_ioc','direction':'sell'},
                {'case_name':'平多 闪电平仓-FOK','order_price_type':'lightning_fok','direction':'sell'}
             ]

    @classmethod
    def setup_class(cls):
        with allure.step('变量初始化'):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.latest_price = currentPrice()
            pass
        with allure.step('*->持仓'):
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.latest_price, 2), direction='sell',
                              volume=10)
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.latest_price, 2), direction='buy',
                              volume=10)
            user01.swap_order(contract_code=cls.contract_code, volume=10, offset='close',
                              price=round(cls.latest_price, 2),
                              direction='buy')
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('*->恢复环境:取消挂单'):
            time.sleep(1)
            user01.swap_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params,DB_orderSeq):
        allure.dynamic.title('撮合 闪电平仓 '+params['case_name'])
        with allure.step('操作：执行平仓'):
            orderInfo = user01.swap_lightning_close_position(contract_code=self.contract_code, volume=1, direction=params['direction'],
                                                               order_price_type=params['order_price_type'])
            pass
        with allure.step('验证：订单存在撮合结果表'):
            strStr = "select count(1) as count from t_exchange_match_result WHERE f_id = " \
                     "(select f_id from t_order_sequence where f_order_id= '%s')" % (orderInfo['data']['order_id'])

            flag = False
            # 给撮合时间，3秒内还未撮合完成则为失败
            for i in range(3):
                isMatch = DB_orderSeq.dictCursor(strStr)[0]['count']
                if 1 == isMatch:
                    flag = True
                    break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i))
            assert flag,'多次重试失败……'

            pass



if __name__ == '__main__':
    pytest.main()
