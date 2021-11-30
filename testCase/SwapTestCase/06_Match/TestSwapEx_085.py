#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211018
# @Author : HuiQing Yu
from common.SwapServiceAPI import user01
import pytest, allure, random, time
from common.CommonUtils import currentPrice
from common.mysqlComm import mysqlComm
from config.conf import DEFAULT_CONTRACT_CODE

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('撮合')  # 这里填功能
@allure.story('开多')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapEx_085:
    contract_code = DEFAULT_CONTRACT_CODE
    @classmethod
    def setup_class(cls):
        with allure.step('*->挂盘'):
            cls.currentPrice = currentPrice()  # 最新价
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2),direction='sell')
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('*->恢复环境:取消挂单'):
            user01.swap_cancelall(contract_code=cls.contract_code)
            pass

    @allure.title('撮合-买入开仓-部分成交')
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, contract_code,DB_orderSeq):
        with allure.step('操作：开多下单'):
            orderInfo = user01.swap_order(contract_code=contract_code, price=round(self.currentPrice, 2), direction='buy',volume=2)
            pass
        with allure.step('验证：订单存在撮合结果表中'):
            sqlStr = "select count(1) from t_exchange_match_result WHERE f_id = " \
                     "(select f_id from t_order_sequence where f_order_id= '%s')" % (orderInfo['data']['order_id'])
            flag = False
            # 给撮合时间，5秒内还未撮合完成则为失败
            for i in range(5):
                isMatch = DB_orderSeq.execute(sqlStr)[0][0]
                if 1 == isMatch:
                    flag = True
                    break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i + 1))
            assert flag
            pass



if __name__ == '__main__':
    pytest.main()
