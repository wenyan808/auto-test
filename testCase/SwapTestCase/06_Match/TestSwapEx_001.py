#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211018
# @Author : HuiQing Yu

import time
import allure
import pytest
from common.CommonUtils import currentPrice, opponentExist
from common.SwapServiceAPI import user01
from config.conf import DEFAULT_CONTRACT_CODE,DEFAULT_SYMBOL
from config.case_content import epic,features

@allure.epic(epic[1])
@allure.feature(features[5]['feature'])
@allure.story(features[5]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapEx_001:
    ids = [ "TestSwapEx_001",
            "TestSwapEx_005",
            "TestSwapEx_009",
            "TestSwapEx_013",
            "TestSwapEx_017",
            "TestSwapEx_021",
            "TestSwapEx_025",
            "TestSwapEx_029",
            "TestSwapEx_033",
            "TestSwapEx_037",
            "TestSwapEx_041",
            "TestSwapEx_045",
            "TestSwapEx_049",
            "TestSwapEx_053",
            "TestSwapEx_057",
            "TestSwapEx_061"]
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
    isExecute = False

    @classmethod
    def setup_class(cls):
        with allure.step("变量初始化"):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.latest_price = currentPrice()
            cls.symbol = DEFAULT_SYMBOL
            pass
        with allure.step('挂盘'):
            cls.currentPrice = currentPrice()  # 最新价
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.latest_price, 2), direction='sell',volume=20)
            pass
        with allure.step('检查盘口更新'):
            # 判断对手价是否更新，如果更新（True）则给反值，表示不跳过该用例
            cls.isExecute = ~opponentExist(symbol=cls.symbol, asks='asks')
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('恢复环境:取消挂单'):
            user01.swap_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    @pytest.mark.skipif(condition=isExecute,reason='对手价未刷新跳过用例')
    def test_execute(self, params,DB_orderSeq):
        allure.dynamic.title('撮合 买入 开仓 ' + params['case_name'])
        with allure.step('操作：开多下单'):
            orderInfo = user01.swap_order(contract_code=self.contract_code,price=round(self.latest_price,2), direction='buy',
                                          order_price_type=params['order_price_type'])
            pass
        with allure.step('验证：订单存在撮合结果表中'):
            orderId = orderInfo['data']['order_id_str']
            sqlStr = f'select count(1) as count from t_exchange_match_result ' \
                     f'WHERE f_id = (select f_id from t_order_sequence where f_order_id= {orderId})'
            flag = False
            # 给撮合时间，5秒内还未撮合完成则为失败
            for i in range(3):
                isMatch = DB_orderSeq.dictCursor(sqlStr)[0]['count']
                if 1 == isMatch:
                    flag = True
                    break
                time.sleep(1)
                print(f'未返回预期结果，第{i+1}次重试………………………………')
            assert flag
            pass



if __name__ == '__main__':
    pytest.main()
