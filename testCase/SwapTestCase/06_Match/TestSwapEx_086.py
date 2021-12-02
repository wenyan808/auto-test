#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211018
# @Author : HuiQing Yu

import allure
import pytest
import time

from common.CommonUtils import currentPrice
from common.SwapServiceAPI import user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic(epic[1])
@allure.feature(features[5]['feature'])
@allure.story(features[5]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapEx_086:
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step('*->挂盘'):
            cls.currentPrice = currentPrice()  # 最新价
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2), direction='buy')
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('*->恢复环境:取消挂单'):
            user01.swap_cancelall(contract_code=cls.contract_code)
            pass

    @allure.title('撮合-卖出开仓-部分成交')
    def test_execute(self, contract_code, DB_orderSeq):
        with allure.step('操作：开空下单'):
            self.currentPrice = currentPrice()  # 最新价

            orderInfo = user01.swap_order(contract_code=contract_code, price=round(self.currentPrice, 2),
                                          direction='sell', volume=2)
            pass
        with allure.step('操作：开多下单'):
            orderId = orderInfo['data']['order_id_str']
            sqlStr = f'select count(1) as count from t_exchange_match_result ' \
                     f'WHERE f_id = (select f_id from t_order_sequence where f_order_id= {orderId})'
            flag = False
            # 给撮合时间，5秒内还未撮合完成则为失败
            for i in range(3):
                isMatch = DB_orderSeq.dictCursor(sqlStr)[0]['count']
                if 1 == isMatch:
                    flag = True
                    break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i + 1))
            assert flag
            pass


if __name__ == '__main__':
    pytest.main()
