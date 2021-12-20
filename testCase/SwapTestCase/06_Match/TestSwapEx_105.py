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
from tool.SwapTools import SwapTool


@allure.epic(epic[1])
@allure.feature(features[5]['feature'])
@allure.story(features[5]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapEx_105:

    @allure.title('撮合 买入开仓 全部成交多人多笔价格相同的订单')
    def test_execute(self, contract_code, mysqlClient):
        allure.dynamic.description('测试步骤：'
                                   '\n*、下限价单；买入开仓（开多）'
                                   '\n*、3用户下单，用户1，用户2各下2笔开多单，用户3下4笔开空单'
                                   '\n*、用户1与用户2的开多单与用户3的开空单成交'
                                   '\n*、验证开多订单撮合成功（查询撮合表有数据）')
        with allure.step('操作：多用户下单'):
            self.currentPrice = SwapTool.currentPrice()  # 最新价
            orderIdList = []
            for user in [user01, user02]:
                orderInfo = user.swap_order(contract_code=contract_code, price=round(self.currentPrice, 2),
                                            direction='buy')
                orderIdList.append(orderInfo['data']['order_id'])
                orderInfo = user.swap_order(contract_code=contract_code, price=round(self.currentPrice, 2),
                                            direction='buy')
                orderIdList.append(orderInfo['data']['order_id'])
            # 用于成交
            user03.swap_order(contract_code=contract_code, price=round(self.currentPrice, 2),
                              direction='sell', volume=4)
            pass
        with allure.step('验证：所有订单都在撮合表中'):
            for i in range(4):
                sqlStr = "select count(1) as count from t_exchange_match_result WHERE f_id = " \
                         "(select f_id from t_order_sequence where f_order_id= '%s')" % (orderIdList[i])
                # 给撮合时间，5秒内还未撮合完成则为失败
                n = 0
                while n < 5:
                    isMatch = mysqlClient.selectdb_execute(dbSchema='order_seq',sqlStr=sqlStr)[0]['count']
                    if 1 == isMatch:
                        break
                    else:
                        n = n + 1
                        time.sleep(1)
                        print('等待处理，第' + str(n) + '次重试………………………………')
                        if n == 5:
                            assert False
            pass


if __name__ == '__main__':
    pytest.main()
