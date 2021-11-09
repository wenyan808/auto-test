#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211018
# @Author : 
    用例标题
        撮合 限价委托 买入 开仓               
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        正确撮合
    优先级
        0
    用例别名
        TestSwapEx_001
"""
from tool.atp import ATP
from config.conf import DEFAULT_CONTRACT_CODE
import pytest, allure, random, time
from common.mysqlComm import orderSeq as DB_orderSeq
from common.SwapServiceAPI import user01

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('撮合')  # 这里填功能
@allure.story('开多')  # 这里填子功能，没有的话就把本行注释掉
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
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step('*->挂盘'):
            cls.currentPrice = ATP.get_current_price()  # 最新价
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2), direction='sell',volume=20)
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('*->恢复环境:取消挂单'):
            time.sleep(1)
            user01.swap_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title('撮合 买入 开仓 ' + params['case_name'])
        with allure.step("测试方案->买入开仓，通过查询撮合结果表验证撮合结果"):
            pass
        with allure.step('买入开仓'):
            orderInfo = user01.swap_order(contract_code=self.contract_code,price=round(self.currentPrice,2), direction='buy',
                                          order_price_type=params['order_price_type'])
            pass
        with allure.step('验证撮合结果'):
            strStr = "select count(1) from t_exchange_match_result WHERE f_id = " \
                     "(select f_id from t_order_sequence where f_order_id= '%s')" % (orderInfo['data']['order_id'])
            # 给撮合时间，5秒内还未撮合完成则为失败
            n = 0
            while n<5:
                isMatch = DB_orderSeq.execute(strStr)[0][0]
                if 1 == isMatch:
                    break
                else:
                    n = n+1
                    time.sleep(1)
                    print('等待处理，第'+str(n)+'次重试………………………………')
                    if n == 5:
                        assert False

            pass


if __name__ == '__main__':
    pytest.main()
