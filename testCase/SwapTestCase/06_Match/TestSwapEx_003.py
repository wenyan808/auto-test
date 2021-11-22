#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211018
# @Author : HuiQing Yu
from tool.atp import ATP
import pytest, allure, random, time
from common.mysqlComm import mysqlComm
from common.SwapServiceAPI import user01
from config.conf import DEFAULT_CONTRACT_CODE
from common.CommonUtils import currentPrice,opponentExist

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('撮合')  # 这里填功能
@allure.story('平空')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapEx_003:
    DB_orderSeq = mysqlComm('order_seq')
    ids = [ "TestSwapEx_003",
            "TestSwapEx_007",
            "TestSwapEx_011",
            "TestSwapEx_015",
            "TestSwapEx_019",
            "TestSwapEx_023",
            "TestSwapEx_027",
            "TestSwapEx_031",
            "TestSwapEx_035",
            "TestSwapEx_039",
            "TestSwapEx_043",
            "TestSwapEx_047",
            "TestSwapEx_051",
            "TestSwapEx_055",
            "TestSwapEx_059",
            "TestSwapEx_063"]
    params = [
              {
                "case_name": "限价单",
                "order_price_type": "limit"
              },
              {
                "case_name": "对手价",
                "order_price_type": "opponent"
              },
              {
                "case_name": "做maker单",
                "order_price_type": "post_only"
              },
              {
                "case_name": "最优5档",
                "order_price_type": "optimal_5"
              },
              {
                "case_name": "最优10档",
                "order_price_type": "optimal_10"
              },
              {
                "case_name": "最优20档",
                "order_price_type": "optimal_20"
              },
              {
                "case_name": "IOC单",
                "order_price_type": "ioc"
              },
              {
                "case_name": "fok单",
                "order_price_type": "fok"
              },
              {
                "case_name": "对手价IOC",
                "order_price_type": "opponent_ioc"
              },
              {
                "case_name": "对手价FOK",
                "order_price_type": "opponent_fok"
              },
              {
                "case_name": "最优5档IOC",
                "order_price_type": "optimal_5_ioc"
              },
              {
                "case_name": "最优10档IOC",
                "order_price_type": "optimal_10_ioc"
              },
              {
                "case_name": "最优20档IOC",
                "order_price_type": "optimal_20_ioc"
              },
              {
                "case_name": "最优5档FOK",
                "order_price_type": "optimal_5_fok"
              },
              {
                "case_name": "最优10档FOK",
                "order_price_type": "optimal_10_fok"
              },
              {
                "case_name": "最优20档FOK",
                "order_price_type": "optimal_20_fok"
              }
            ]
    contract_code = DEFAULT_CONTRACT_CODE
    isExecute = False
    @classmethod
    def setup_class(cls):
        with allure.step('*->挂盘'):
            cls.currentPrice = currentPrice()  # 最新价
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2), direction='buy',
                              volume=20)
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2), direction='sell',
                              volume=40)
            # 判断对手价是否更新，如果更新（True）则给反值，表示不跳过该用例
            cls.isExecute = ~opponentExist('BTC', asks='asks')
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('*->恢复环境:取消挂单'):
            user01.swap_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    @pytest.mark.skipif(condition=isExecute, reason='对手价未刷新跳过用例')
    def test_execute(self, params):
        allure.dynamic.title('撮合 买入 平仓 ' + params['case_name'])
        with allure.step('操作：下单（平空）'):
            orderInfo = user01.swap_order(contract_code=self.contract_code, price=round(self.currentPrice, 2),
                                          direction='buy',offset='close', order_price_type=params['order_price_type'])
            pass
        with allure.step('验证：订单存在撮合结果表中'):
            strStr = "select count(1) from t_exchange_match_result WHERE f_id = " \
                     "(select f_id from t_order_sequence where f_order_id= '%s')" % (orderInfo['data']['order_id'])
            flag = False
            # 给撮合时间，5秒内还未撮合完成则为失败
            for i in range(5):
                isMatch = self.DB_orderSeq.execute(strStr)[0][0]
                if 1 == isMatch:
                    flag = True
                    break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i))
            assert flag
            pass

if __name__ == '__main__':
    pytest.main()
