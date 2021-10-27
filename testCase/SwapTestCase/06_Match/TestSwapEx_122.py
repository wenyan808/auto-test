#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211018
# @Author : 
    用例标题
        撮合 卖出开仓 全部成交多人多笔价格不同的订单
    前置条件

    步骤/文本
        详见官方文档
    预期结果
        正确撮合
    优先级
        2
    用例别名
        TestSwapEx_122
"""

from common.SwapServiceAPI import user01, user02, user03
import pytest, allure, random, time
from tool.atp import ATP
from common.mysqlComm import orderSeq as DB_orderSeq


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('撮合')  # 这里填功能
@allure.story('开空')  # 这里填子功能，没有的话就把本行注释掉
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
    @allure.step('测试执行')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_execute(self, contract_code):
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