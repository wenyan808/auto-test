#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211018
# @Author : HuiQing Yu

import time

import allure
import pytest

from common.SwapServiceAPI import user01
from common.mysqlComm import mysqlComm
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE
from tool.SwapTools import SwapTool


@allure.epic(epic[1])
@allure.feature(features[5]['feature'])
@allure.story(features[5]['story'][3])
@pytest.mark.stable
class TestSwapEx_069:
    ids = ["TestSwapEx_069",
           "TestSwapEx_073",
           "TestSwapEx_077"]
    params = [
        {
            "case_name": "买入开仓 挂单 撤销",
            "ratio": 0.9,
            "volume":2
        },{
            "case_name": "买入开仓 全部成交 撤销",
            "ratio": 1.0,
            "volume":2
        },{
            "case_name": "买入开仓 部分成交 撤销",
            "ratio": 1.0,
            "volume":4
        }

    ]

    @classmethod
    def setup_class(cls):
        with allure.step('变量初始化'):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.latest_price = SwapTool.currentPrice()
            cls.mysqlClient = mysqlComm()
            pass
        with allure.step('挂盘'):
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.latest_price, 2), direction='sell',
                              volume=4)
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('恢复环境:取消挂单'):
            user01.swap_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        allure.dynamic.description("先挂卖单4张："
                                   "\n下单价格为当前价的一半，无法成交；"
                                   "\n以当前价下单，数量为2，则全部成交;"
                                   "\n以当前价下单，数量为4；当前买盘只有2张，所以会部分成交；"
                                   "\n最后撤单所有限价单")

        with allure.step('操作：开多下单'):
            orderInfo = user01.swap_order(contract_code=self.contract_code, price=round(self.latest_price * params['ratio'], 2),
                                          volume=params['volume'], direction='buy')
            pass
        with allure.step('验证：订单存在撮合结果表'):
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



if __name__ == '__main__':
    pytest.main()
