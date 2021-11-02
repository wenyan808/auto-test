#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211027
# @Author : yuhuiqing

from tool.atp import ATP
import pytest, allure, random, time
from common.mysqlComm import orderSeq as DB_orderSeq
from common.ContractServiceAPI import user01

@allure.epic('反向交割')  # 这里填业务线
@allure.feature('撮合')  # 这里填功能
@allure.story('平多')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestContractEx_272:
    ids = ['TestContractEx_272',
           'TestContractEx_276',
           'TestContractEx_280',
           'TestContractEx_284',
           'TestContractEx_288',
           'TestContractEx_292',
           'TestContractEx_296',
           'TestContractEx_300',
           'TestContractEx_304',
           'TestContractEx_308',
           'TestContractEx_312',
           'TestContractEx_315',
           'TestContractEx_320',
           'TestContractEx_324',
           'TestContractEx_328',
           'TestContractEx_332',
           'TestContractEx_406',
           'TestContractEx_410',
           'TestContractEx_414',
           'TestContractEx_418',
           'TestContractEx_422',
           'TestContractEx_426',
           'TestContractEx_430',
           'TestContractEx_434',
           'TestContractEx_438',
           'TestContractEx_442',
           'TestContractEx_446',
           'TestContractEx_450',
           'TestContractEx_454',
           'TestContractEx_458',
           'TestContractEx_462',
           'TestContractEx_466']
    datas = [{'titleName': '当季 限价单', 'contest_type': 'quarter', 'order_price_type': 'limit'},
             {'titleName': '当季 对手价', 'contest_type': 'quarter', 'order_price_type': 'opponent'},
             {'titleName': '当季 最优5档', 'contest_type': 'quarter', 'order_price_type': 'optimal_5'},
             {'titleName': '当季 最优10档', 'contest_type': 'quarter', 'order_price_type': 'optimal_10'},
             {'titleName': '当季 最优20档', 'contest_type': 'quarter', 'order_price_type': 'optimal_20'},
             {'titleName': '当季 only maker单', 'contest_type': 'quarter', 'order_price_type': 'post_only'},
             {'titleName': '当季 only ioc单', 'contest_type': 'quarter', 'order_price_type': 'ioc'},
             {'titleName': '当季 only fok单', 'contest_type': 'quarter', 'order_price_type': 'fok'},
             {'titleName': '当季 对手价IOC', 'contest_type': 'quarter', 'order_price_type': 'opponent_ioc'},
             {'titleName': '当季 最优5档IOC', 'contest_type': 'quarter', 'order_price_type': 'optimal_5_ioc'},
             {'titleName': '当季 最优10档IOC', 'contest_type': 'quarter', 'order_price_type': 'optimal_10_ioc'},
             {'titleName': '当季 最优20档IOC', 'contest_type': 'quarter', 'order_price_type': 'optimal_20_ioc'},
             {'titleName': '当季 对手价FOK', 'contest_type': 'quarter', 'order_price_type': 'opponent_fok'},
             {'titleName': '当季 最优5档FOK', 'contest_type': 'quarter', 'order_price_type': 'optimal_5_fok'},
             {'titleName': '当季 最优10档FOK', 'contest_type': 'quarter', 'order_price_type': 'optimal_10_fok'},
             {'titleName': '当季 最优20档FOK', 'contest_type': 'quarter', 'order_price_type': 'optimal_20_fok'},
             {'titleName': '次季 限价单', 'contest_type': 'next_quarter', 'order_price_type': 'limit'},
             {'titleName': '次季 对手价', 'contest_type': 'next_quarter', 'order_price_type': 'opponent'},
             {'titleName': '次季 最优5档', 'contest_type': 'next_quarter', 'order_price_type': 'optimal_5'},
             {'titleName': '次季 最优10档', 'contest_type': 'next_quarter', 'order_price_type': 'optimal_10'},
             {'titleName': '次季 最优20档', 'contest_type': 'next_quarter', 'order_price_type': 'optimal_20'},
             {'titleName': '次季 only maker单', 'contest_type': 'next_quarter', 'order_price_type': 'post_only'},
             {'titleName': '次季 only fok单', 'contest_type': 'next_quarter', 'order_price_type': 'fok'},
             {'titleName': '次季 only ioc单', 'contest_type': 'next_quarter', 'order_price_type': 'ioc'},
             {'titleName': '次季 对手价IOC', 'contest_type': 'next_quarter', 'order_price_type': 'opponent_ioc'},
             {'titleName': '次季 最优5档IOC', 'contest_type': 'next_quarter', 'order_price_type': 'optimal_5_ioc'},
             {'titleName': '次季 最优10档IOC', 'contest_type': 'next_quarter', 'order_price_type': 'optimal_10_ioc'},
             {'titleName': '次季 最优20档IOC', 'contest_type': 'next_quarter', 'order_price_type': 'optimal_20_ioc'},
             {'titleName': '次季 对手价FOK', 'contest_type': 'next_quarter', 'order_price_type': 'opponent_fok'},
             {'titleName': '次季 最优5档FOK', 'contest_type': 'next_quarter', 'order_price_type': 'optimal_5_fok'},
             {'titleName': '次季 最优10档FOK', 'contest_type': 'next_quarter', 'order_price_type': 'optimal_10_fok'},
             {'titleName': '次季 最优20档FOK', 'contest_type': 'next_quarter', 'order_price_type': 'optimal_20_fok'}]


    @allure.step('测试执行')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.parametrize('params',datas,ids=ids)
    def test_execute(self,symbol,params):
        with allure.step('详见官方文档'):
            allure.dynamic.title(params['titleName'])
            self.contract_type = params['contest_type']
            # 获取交割合约信息
            contractInfo = user01.contract_contract_info(symbol=symbol, contract_type=self.contract_type)
            self.contract_code = contractInfo['data'][0]['contract_code']
            self.currentPrice = ATP.get_current_price(contract_code=self.contract_code)
            # 持仓
            user01.contract_order(symbol=symbol, contract_code=self.contract_code,
                                  price=round(self.currentPrice, 2),
                                  contract_type=self.contract_type, direction='buy')
            user01.contract_order(symbol=symbol, contract_code=self.contract_code,
                                  price=round(self.currentPrice, 2),
                                  contract_type=self.contract_type, direction='sell')
            # 平仓
            user01.contract_order(symbol=symbol, contract_code=self.contract_code,
                                  price=round(self.currentPrice, 2),
                                  contract_type=self.contract_type, direction='buy',offset='close')
            orderInfo = user01.contract_order(symbol=symbol,contract_code=self.contract_code,
                                              price=round(self.currentPrice, 2),
                                              contract_type=self.contract_type,direction='sell',offset='close',
                                              order_price_type=params['order_price_type'])
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
            user01.contract_cancelall(symbol=symbol)
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
