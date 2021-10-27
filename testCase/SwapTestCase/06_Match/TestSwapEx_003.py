#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211018
# @Author : 
    用例标题
        撮合 限价委托 买入 平仓
    前置条件

    步骤/文本
        详见官方文档
    预期结果
        正确撮合
    优先级
        0
    用例别名
        TestSwapEx_003
"""
from tool.atp import ATP
import pytest, allure, random, time
from common.mysqlComm import orderSeq as DB_orderSeq
from common.SwapServiceAPI import user01

caseNames = ['限价单','对手价','做maker单','最优5档','最优10档','最优20档','IOC单','fok单','对手价IOC','对手价FOK',
             '最优5档IOC','最优10档IOC','最优20档IOC','最优5档FOK','最优10档FOK','最优20档FOK']
params = ['limit','opponent','post_only','optimal_5','optimal_10','optimal_20','ioc','fok','opponent_ioc','opponent_fok',
          'optimal_5_ioc','optimal_10_ioc','optimal_20_ioc','optimal_5_fok','optimal_10_fok','optimal_20_fok']


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('撮合')  # 这里填功能
@allure.story('平空')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapEx_003:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self,contract_code):
        print('测试步骤：'
              '\n*、先下单开仓持仓'
              '\n*、下限价单；买入平仓（平空）'
              '\n*、验证撮合成功（查询撮合表有数据）')
        self.currentPrice = ATP.get_current_price()  # 最新价
        user01.swap_order(contract_code=contract_code, price=round(self.currentPrice, 2), direction='sell')
        user01.swap_order(contract_code=contract_code, price=round(self.currentPrice, 2), direction='buy')

    @allure.title('撮合 限价委托 买入 平仓')
    @allure.step('测试执行')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_execute(self, params,contract_code):
        with allure.step('详见官方文档'):
            user01.swap_order(contract_code=contract_code, price=round(self.currentPrice, 2), direction='sell',offset='close')
            time.sleep(0.5)
            orderInfo = user01.swap_order(contract_code=contract_code, price=round(self.currentPrice, 2),
                                          direction='buy',offset='close', order_price_type=params)
            orderId = orderInfo['data']['order_id']
            strStr = "select count(1) from t_exchange_match_result WHERE f_id = " \
                     "(select f_id from t_order_sequence where f_order_id= '%s')" % (orderId)

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

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
