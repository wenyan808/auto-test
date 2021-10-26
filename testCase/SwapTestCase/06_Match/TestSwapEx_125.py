#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211018
# @Author : 
    用例标题
        撮合 闪电平仓 卖出
    前置条件

    步骤/文本
        详见官方文档
    预期结果
        正确撮合
    优先级
        3
    用例别名
        TestSwapEx_125 ~ TestSwapEx_129
"""
from common.SwapServiceAPI import t as swap_api
from tool.atp import ATP
import pytest, allure, random, time
from common.mysqlComm import orderSeq as DB_orderSeq

caseNames = ['闪电平仓', '闪电平仓-IOC', '闪电平仓-FOK']
params = ['lightning', 'lightning_ioc', 'lightning_fok']


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('撮合')  # 这里填功能
@allure.story('闪电平仓-平多')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapEx_134:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('撮合 闪电平仓 卖出')
    @allure.step('测试执行')
    def test_execute(self, params, contract_code):
        with allure.step('详见官方文档'):
            ATP.clean_market(contract_code=contract_code)
            self.currentPrice = ATP.get_current_price()  # 最新价
            swap_api.swap_order(contract_code=contract_code, price=round(self.currentPrice * 0.99, 2), direction='sell')
            swap_api.swap_order(contract_code=contract_code, price=round(self.currentPrice * 0.99, 2), direction='buy')
            time.sleep(1)
            swap_api.swap_order(contract_code=contract_code, price=round(self.currentPrice * 0.99, 2), direction='buy',offset='close')
            orderInfo = swap_api.swap_lightning_close_position(contract_code=contract_code, volume=1, direction='sell',
                                                               order_price_type=params)
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
