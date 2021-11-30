#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211018
# @Author : HuiQing Yu
from common.SwapServiceAPI import user01, user02, user03
import pytest, allure, random, time
from tool.atp import ATP
from common.mysqlComm import mysqlComm


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('撮合')  # 这里填功能
@allure.story('开空')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapEx_106:
    DB_orderSeq = mysqlComm('order_seq')
    @allure.step('前置条件')
    def setup(self):
        print('测试步骤：'
              '\n*、下限价单；买入开仓（开空）'
              '\n*、3用户下单，用户1，用户2各下2笔开空单，用户3下4笔开多单'
              '\n*、用户1与用户2的开空单与用户3的开多单成交'
              '\n*、验证开空笔订单撮合成功（查询撮合表有数据）')

    @allure.title('撮合 卖出开仓 全部成交多人多笔价格相同的订单')
    def test_execute(self, contract_code):
        with allure.step('操作：用户1，2开空订单多笔，用户3开多订单用于成交'):
            self.currentPrice = ATP.get_current_price()  # 最新价
            orderIdList = []
            for user in [user01, user02]:
                orderInfo = user.swap_order(contract_code=contract_code, price=round(self.currentPrice, 2),
                                            direction='sell')
                orderIdList.append(orderInfo['data']['order_id'])
                orderInfo = user.swap_order(contract_code=contract_code, price=round(self.currentPrice, 2),
                                direction='sell')
                orderIdList.append(orderInfo['data']['order_id'])
            # 用于成交
            user03.swap_order(contract_code=contract_code, price=round(self.currentPrice, 2),
                              direction='buy',volume=4)
        with allure.step('验证：开空订单多笔是否已存在撮合结果表中'):

            for i in range(4):
                strStr = "select count(1) from t_exchange_match_result WHERE f_id = " \
                         "(select f_id from t_order_sequence where f_order_id= '%s')" % (orderIdList[i])
                # 给撮合时间，5秒内还未撮合完成则为失败
                n = 0
                while n < 5:
                    isMatch = self.DB_orderSeq.execute(strStr)[0][0]
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
