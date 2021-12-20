#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211018
# @Author : HuiQing Yu

import allure
import pytest
import time

from common.SwapServiceAPI import user01, user02, user03
from common.mysqlComm import mysqlComm
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE
from tool.SwapTools import SwapTool


@allure.epic(epic[1])
@allure.feature(features[5]['feature'])
@allure.story(features[5]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapEx_120:
    @classmethod
    def setup_class(cls):
        with allure.step('实始化变量'):
            cls.mysqlClient = mysqlComm()
            cls.currentPrice = SwapTool.currentPrice()  # 最新价
            cls.contract_code = DEFAULT_CONTRACT_CODE
        with allure.step('持仓'):
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2),
                              direction='buy', volume=4)
            user02.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2),
                              direction='buy', volume=4)
            user03.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2),
                              direction='sell', volume=8)

    @classmethod
    def teardown_class(cls):
        with allure.step('*->恢复环境'):
            # 测试完后所有用户都撤单
            user01.swap_cancelall(contract_code=cls.contract_code)
            user02.swap_cancelall(contract_code=cls.contract_code)
            user03.swap_cancelall(contract_code=cls.contract_code)
            pass

    @allure.title('撮合 买入平仓 部分成交多人多笔价格不同的订单')
    def test_execute(self):
        allure.dynamic.description('测试步骤：'
                                   '\n*、下限价单；买入平仓（平多）'
                                   '\n*、用户1，用户2各下2笔开平多单（价不同，数量为2）'
                                   '\n*、用户3下单分别与用户1，用户2不同价位的单成交，成交数量1'
                                   '\n*、验证平多订单撮合成功（查询撮合表有数据）')
        with allure.step('操作：多用户下单'):
            orderIdList = []
            # 2个用户分别下2个不同价位的单，并成交一半；
            for user in [user01, user02]:
                for i in range(2):
                    orderInfo = user.swap_order(contract_code=self.contract_code,
                                                price=round(self.currentPrice * (1 - (i + 1) * 0.01), 2),
                                                direction='sell', offset='close', volume=2)
                    orderIdList.append(orderInfo['data']['order_id'])
                    # 用于成交
                    user03.swap_order(contract_code=self.contract_code,
                                      price=round(self.currentPrice * (1 - (i + 1) * 0.01), 2),
                                      direction='buy', offset='close')
        with allure.step('验证：订单都存在撮合表中'):
            for i in range(4):
                sqlStr = "select count(1) as count from t_exchange_match_result WHERE f_id = " \
                         "(select f_id from t_order_sequence where f_order_id= '%s')" % (orderIdList[i])
                # 给撮合时间，5秒内还未撮合完成则为失败
                flag = False
                for j in range(3):
                    isMatch = self.mysqlClient.selectdb_execute(dbSchema='order_seq', sqlStr=sqlStr)[0]['count']
                    if 1 == isMatch:
                        flag = True
                        break
                    else:
                        time.sleep(1)
                        print(f'等待处理，第{j + 1}次重试………………………………')

            assert flag, '多次重试失败'


if __name__ == '__main__':
    pytest.main()
