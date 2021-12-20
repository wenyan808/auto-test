#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211018
# @Author : HuiQing Yu

import time

import allure
import pytest

from common.mysqlComm import mysqlComm
from config.conf import DEFAULT_CONTRACT_CODE
from tool.SwapTools import SwapTool
from common.SwapServiceAPI import user01, user02, user03
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[5]['feature'])
@allure.story(features[5]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapEx_117:
    @classmethod
    def setup_class(cls):
        with allure.step('实始化变量'):
            cls.mysqlClient = mysqlComm()
            cls.currentPrice = SwapTool.currentPrice()  # 最新价
            cls.contract_code = DEFAULT_CONTRACT_CODE
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('*->恢复环境'):
            # 测试完后所有用户都撤单
            user01.swap_cancelall(contract_code=cls.contract_code)
            user02.swap_cancelall(contract_code=cls.contract_code)
            user03.swap_cancelall(contract_code=cls.contract_code)
            pass

    @allure.title('撮合 买入开仓 部分成交多人多笔价格不同的订单')
    def test_execute(self):
        allure.dynamic.description('测试步骤：'
                                   '\n*、下限价单；买入开仓（开多）'
                                   '\n*、用户1，用户2各下2笔开多单（价不同，数量为2）'
                                   '\n*、用户3下单分别与用户1，用户2不同价位的单成交，成交数量1'
                                   '\n*、验证开多订单撮合成功（查询撮合表有数据）')
        with allure.step('操作：多用户下单'):
            self.currentPrice = SwapTool.currentPrice()  # 最新价
            orderIdList = []
            # 2个用户分别下2个不同价位的单，并成交一半；
            for user in [user01, user02]:
                for i in range(2):
                    orderInfo = user.swap_order(contract_code=self.contract_code,
                                                price=round(self.currentPrice * (1 - (i + 1) * 0.01), 2),
                                                direction='buy', volume=2)
                    orderIdList.append(orderInfo['data']['order_id'])
                    user03.swap_order(contract_code=self.contract_code,
                                      price=round(self.currentPrice * (1 - (i + 1) * 0.01), 2),
                                      direction='sell')
            pass
        with allure.step('验证：所有订单都在撮合表中'):
            # 验证2个用户共4个开多单的撮合
            for i in range(4):
                sqlStr = "select count(1) as count from t_exchange_match_result WHERE f_id = " \
                         "(select f_id from t_order_sequence where f_order_id= '%s')" % (orderIdList[i])
                # 给撮合时间，5秒内还未撮合完成则为失败
                n = 0
                while n < 5:
                    isMatch = self.mysqlClient.selectdb_execute(dbSchema='order_seq', sqlStr=sqlStr)[0]['count']
                    if 1 == isMatch:
                        break
                    else:
                        n = n + 1
                        time.sleep(1)
                        print('等待处理，第' + str(n) + '次重试………………………………')
                        if n == 5:
                            assert False


if __name__ == '__main__':
    pytest.main()
