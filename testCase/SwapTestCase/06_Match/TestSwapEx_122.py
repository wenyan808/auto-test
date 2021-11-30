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
from tool.atp import ATP


@allure.epic(epic[1])
@allure.feature(features[5]['feature'])
@allure.story(features[5]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapEx_122:

    @allure.step('前置条件')
    def setup(self):
        print('测试步骤：'
              '\n*、下限价单；买入开仓（开多）'
              '\n*、用户1，用户2各下2笔开空单（价不同，数量为2）'
              '\n*、用户3下单分别与用户1，用户2不同价位的单成交，成交数量2'
              '\n*、验证开空订单撮合成功（查询撮合表有数据）')

    @allure.title('撮合 卖出开仓 全部成交多人多笔价格不同的订单')
    def test_execute(self, contract_code):
        DB_orderSeq = mysqlComm('order_seq')
        with allure.step('详见官方文档'):
            self.currentPrice = ATP.get_current_price()  # 最新价
            orderIdList = []
            # 2个用户分别下2个不同价位的单，并成交；
            for user in [user01, user02]:
                for i in range(2):
                    orderInfo = user.swap_order(contract_code=contract_code,
                                                price=round(self.currentPrice * (1 + (i + 1) * 0.01), 2),
                                                direction='sell', volume=2)
                    orderIdList.append(orderInfo['data']['order_id'])
                    # 用于成交
                    user03.swap_order(contract_code=contract_code,
                                      price=round(self.currentPrice * (1 + (i + 1) * 0.01), 2),
                                      direction='buy',volume=2)
            for i in range(4):
                strStr = "select count(1) from t_exchange_match_result WHERE f_id = " \
                         "(select f_id from t_order_sequence where f_order_id= '%s')" % (orderIdList[i])
                # 给撮合时间，5秒内还未撮合完成则为失败
                n = 0
                while n < 5:
                    isMatch = DB_orderSeq.execute(strStr)[0][0]
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
