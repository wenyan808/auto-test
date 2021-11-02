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
@allure.story('开多')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestContractEx_269:
    ids = ['TestContractEx_269',
           'TestContractEx_273',
           'TestContractEx_277',
           'TestContractEx_281',
           'TestContractEx_285',
           'TestContractEx_289',
           'TestContractEx_293',
           'TestContractEx_297',
           'TestContractEx_301',
           'TestContractEx_305',
           'TestContractEx_309',
           'TestContractEx_313',
           'TestContractEx_317',
           'TestContractEx_321',
           'TestContractEx_325',
           'TestContractEx_329',
           'TestContractEx_403',
           'TestContractEx_407',
           'TestContractEx_411',
           'TestContractEx_415',
           'TestContractEx_419',
           'TestContractEx_423',
           'TestContractEx_427',
           'TestContractEx_431',
           'TestContractEx_435',
           'TestContractEx_439',
           'TestContractEx_443',
           'TestContractEx_447',
           'TestContractEx_451',
           'TestContractEx_455',
           'TestContractEx_459',
           'TestContractEx_463']

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
            user01.contract_order(symbol=symbol, contract_code=self.contract_code,
                                  price=round(self.currentPrice, 2),
                                  contract_type=self.contract_type, direction='sell')
            orderInfo = user01.contract_order(symbol=symbol,contract_code=self.contract_code,
                                              price=round(self.currentPrice, 2),
                                              contract_type=self.contract_type,direction='buy',order_price_type=params['order_price_type'])
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


if __name__ == '__main__':
    pytest.main()
