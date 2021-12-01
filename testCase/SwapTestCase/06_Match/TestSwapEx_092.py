#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211018
# @Author : HuiQing Yu

from common.SwapServiceAPI import user01
import pytest, allure, random, time
from common.CommonUtils import currentPrice
from common.mysqlComm import mysqlComm
from config.conf import DEFAULT_CONTRACT_CODE
from config.case_content import epic,features

@allure.epic(epic[1])
@allure.feature(features[5]['feature'])
@allure.story(features[5]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapEx_088:
    DB_orderSeq = mysqlComm('order_seq')
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step('*->挂盘'):
            cls.currentPrice = currentPrice()  # 最新价
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2), direction='sell')
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2), direction='buy',
                              volume=2)
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('*->恢复环境:取消挂单'):
            user01.swap_cancelall(contract_code=cls.contract_code)
            pass

    @allure.title('撮合-卖出平仓-全部成交单笔订单')
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, contract_code):
        with allure.step('操作：平多下单'):
            orderInfo = user01.swap_order(contract_code=contract_code, price=round(self.currentPrice, 2),offset='close',
                                          direction='sell')
            pass
        with allure.step('验证：订单存在撮合结果表中'):
            sqlStr = "select count(1) from t_exchange_match_result WHERE f_id = " \
                     "(select f_id from t_order_sequence where f_order_id= '%s')" % (orderInfo['data']['order_id'])
            flag = False
            # 给撮合时间，5秒内还未撮合完成则为失败
            for i in range(5):
                isMatch = self.DB_orderSeq.execute(sqlStr)[0][0]
                if 1 == isMatch:
                    flag = True
                    break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i + 1))
            assert flag
            pass


if __name__ == '__main__':
    pytest.main()
