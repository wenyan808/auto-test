#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211018
# @Author :  HuiQing Yu

from common.SwapServiceAPI import user01
from tool.atp import ATP
import pytest, allure, random, time
from common.mysqlComm import mysqlComm
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('撮合')  # 这里填功能
@allure.story('闪电平仓-平多')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapEx_134:

    ids = ['TestSwapEx_132', 'TestSwapEx_133', 'TestSwapEx_134']
    params = [
                {'case_name': '平空 闪电平仓', 'order_price_type': 'lightning', 'direction': 'buy'},
                {'case_name': '平空 闪电平仓-IOC', 'order_price_type': 'lightning_ioc', 'direction': 'buy'},
                {'case_name': '平空 闪电平仓-FOK', 'order_price_type': 'lightning_fok', 'direction': 'buy'}
             ]
    contract_code = DEFAULT_CONTRACT_CODE
    @classmethod
    def setup_class(cls):
        with allure.step('*->持仓'):
            cls.currentPrice = ATP.get_current_price()  # 最新价
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2), direction='sell',
                              volume=10)
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2), direction='buy',
                              volume=10)
            user01.swap_order(contract_code=cls.contract_code, volume=10,offset='close',price=round(cls.currentPrice, 2),
                                                 direction='sell')
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('*->恢复环境:取消挂单'):
            time.sleep(1)
            user01.swap_cancelall(contract_code=cls.contract_code)
            pass

    # @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title('撮合 闪电平仓 '+params['case_name'])
        DB_orderSeq = mysqlComm('order_seq')
        with allure.step('执行平仓'):
            orderInfo = user01.swap_lightning_close_position(contract_code=self.contract_code, volume=1, direction=params['direction'],
                                                               order_price_type=params['order_price_type'])
            strStr = "select count(1) from t_exchange_match_result WHERE f_id = " \
                     "(select f_id from t_order_sequence where f_order_id= '%s')" % (orderInfo['data']['order_id'])

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
