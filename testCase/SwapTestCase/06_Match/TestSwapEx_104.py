#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211018
# @Author : HuiQing Yu

import time

import allure
import pytest

from common.CommonUtils import currentPrice
from common.SwapServiceAPI import user01, user02, user03
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[5]['feature'])
@allure.story(features[5]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapEx_104:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, contract_code):
        self.currentPrice = currentPrice()  # 最新价
        # 先持仓
        user01.swap_order(contract_code=contract_code, price=round(self.currentPrice, 2),
                          direction='buy', volume=2)
        user01.swap_order(contract_code=contract_code, price=round(self.currentPrice, 2),
                          direction='sell', volume=2)
        user02.swap_order(contract_code=contract_code, price=round(self.currentPrice, 2),
                          direction='buy', volume=2)
        user02.swap_order(contract_code=contract_code, price=round(self.currentPrice, 2),
                          direction='sell', volume=2)

    @allure.title('撮合 买入平仓 部分成交多人多笔价格相同的订单')
    def test_execute(self, contract_code, DB_orderSeq):
        allure.dynamic.description('测试步骤：'
                                   '\n*、下限价单；卖出平仓（平多）'
                                   '\n*、3用户下单，用户1，用户2各下2笔平多单，用户3下2笔开多单'
                                   '\n*、用户1与用户2的平多单与用户3的开多单成交'
                                   '\n*、验证平多订单撮合成功（查询撮合表有数据）')
        with allure.step('操作：多用户下单'):
            orderIdList = []
            for user in [user01, user02]:
                orderInfo = user.swap_order(contract_code=contract_code, price=round(self.currentPrice * 0.99, 2),
                                            direction='sell', offset='close')
                orderIdList.append(orderInfo['data']['order_id'])
                orderInfo = user.swap_order(contract_code=contract_code, price=round(self.currentPrice, 2),
                                            direction='sell', offset='close')
                orderIdList.append(orderInfo['data']['order_id'])
            # 用于成交
            user03.swap_order(contract_code=contract_code, price=round(self.currentPrice * 0.99, 2),
                              direction='buy', volume=2)
            pass
        with allure.step('验证：所有订单都存在撮合表中'):
            for i in range(4):
                strStr = "select count(1) as count from t_exchange_match_result WHERE f_id = " \
                         "(select f_id from t_order_sequence where f_order_id= '%s')" % (orderIdList[i])
                # 给撮合时间，5秒内还未撮合完成则为失败
                n = 0
                while n < 5:
                    isMatch = DB_orderSeq.execute(strStr)[0]['count']
                    if 1 == isMatch:
                        break
                    else:
                        n = n + 1
                        time.sleep(1)
                        print('等待处理，第' + str(n) + '次重试………………………………')
                        if n == 5:
                            assert False
            # 测试完后所有用户都撤单
            user01.swap_cancelall(contract_code=contract_code)
            user02.swap_cancelall(contract_code=contract_code)
            user03.swap_cancelall(contract_code=contract_code)
            pass


if __name__ == '__main__':
    pytest.main()
