#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211018
# @Author : HuiQing

import allure
import pytest
import time

from common.CommonUtils import currentPrice
from common.SwapServiceAPI import user01, user02
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic(epic[1])
@allure.feature(features[5]['feature'])
@allure.story(features[5]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapEx_095:
    ids = ["TestSwapEx_095",
           "TestSwapEx_099",
           "TestSwapEx_111",
           "TestSwapEx_115"]
    params = [
        {
            "case_name": "撮合-买入平仓-部分成交单人多笔价格相同的订单",
            "volume": 2,
            "priceRatio": 0
        }, {
            "case_name": "撮合-买入平仓-全部成交单人多笔价格相同的订单",
            "volume": 1,
            "priceRatio": 0
        }, {
            "case_name": "撮合-买入平仓-部分成交单人多笔价格不同的订单",
            "volume": 2,
            "priceRatio": 0.01
        }, {
            "case_name": "撮合-买入平仓-全部成交单人多笔价格不同的订单",
            "volume": 1,
            "priceRatio": 0.01
        }
    ]
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step('*->挂盘'):
            cls.currentPrice = currentPrice()  # 最新价
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('*->恢复环境'):
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params,DB_orderSeq):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：平空下单'):
            orderIdList = []
            for i in range(1, 3):
                user02.swap_order(contract_code=self.contract_code,
                                  price=round(self.currentPrice * (1 + (i * params['priceRatio'])), 2),
                                  direction='sell')
                orderInfo = user01.swap_order(contract_code=self.contract_code,
                                              price=round(self.currentPrice * (1 + (i * params['priceRatio'])), 2),
                                              volume=params['volume'], direction='buy', offset='close')
                time.sleep(1)  # 等待成交再撤单
                user01.swap_cancelall(contract_code=self.contract_code)
                orderIdList.append(orderInfo['data']['order_id'])
            pass
        with allure.step('验证：订单存在撮合结果表中'):
            for order in orderIdList:
                sqlStr = "select count(1) as count from t_exchange_match_result WHERE f_id in " \
                         "(select f_id from t_order_sequence where f_order_id= '%s')  and role != 'cancel' " % order
                flag = False
                # 给撮合时间，5秒内还未撮合完成则为失败
                for i in range(5):
                    isMatch = DB_orderSeq.execute(sqlStr)[0]['count']
                    if 1 == isMatch:
                        flag = True
                        break
                    time.sleep(1)
                    print('未返回预期结果，第{}次重试………………………………'.format(i))
                assert flag
            pass


if __name__ == '__main__':
    pytest.main()
