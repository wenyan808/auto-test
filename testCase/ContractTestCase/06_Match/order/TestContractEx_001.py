#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211027
# @Author : zhangguangnan

import time

import allure
import pytest
from common.ContractServiceAPI import user01
from common.redisComm import redisConf
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL
from tool.atp import ATP


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('撮合')  # 这里填功能
@allure.story('委托单')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 张广南', 'Case owner : 吉龙')
class TestContractEx_001:
    ids = ['TestContractEx_001',
           'TestContractEx_005',
           'TestContractEx_009',
           'TestContractEx_013',
           'TestContractEx_017',
           'TestContractEx_021',
           'TestContractEx_025',
           'TestContractEx_029',
           'TestContractEx_033',
           'TestContractEx_037',
           'TestContractEx_041',
           'TestContractEx_045',
           'TestContractEx_049',
           'TestContractEx_053',
           'TestContractEx_057',
           'TestContractEx_061',
           'TestContractEx_135',
           'TestContractEx_139',
           'TestContractEx_143',
           'TestContractEx_147',
           'TestContractEx_151',
           'TestContractEx_155',
           'TestContractEx_159',
           'TestContractEx_163',
           'TestContractEx_167',
           'TestContractEx_171',
           'TestContractEx_175',
           'TestContractEx_179',
           'TestContractEx_183',
           'TestContractEx_187',
           'TestContractEx_191',
           'TestContractEx_195']

    datas = [{'titleName': '当周 限价单', 'contest_type': 'this_week', 'order_price_type': 'limit'},
             {'titleName': '当周 对手价', 'contest_type': 'this_week',
                 'order_price_type': 'opponent'},
             {'titleName': '当周 最优5档', 'contest_type': 'this_week',
                 'order_price_type': 'optimal_5'},
             {'titleName': '当周 最优10档', 'contest_type': 'this_week',
                 'order_price_type': 'optimal_10'},
             {'titleName': '当周 最优20档', 'contest_type': 'this_week',
                 'order_price_type': 'optimal_20'},
             {'titleName': '当周 only maker单', 'contest_type': 'this_week',
                 'order_price_type': 'post_only'},
             {'titleName': '当周 only ioc单', 'contest_type': 'this_week',
                 'order_price_type': 'ioc'},
             {'titleName': '当周 only fok单', 'contest_type': 'this_week',
                 'order_price_type': 'fok'},
             {'titleName': '当周 对手价IOC', 'contest_type': 'this_week',
                 'order_price_type': 'opponent_ioc'},
             {'titleName': '当周 最优5档IOC', 'contest_type': 'this_week',
                 'order_price_type': 'optimal_5_ioc'},
             {'titleName': '当周 最优10档IOC', 'contest_type': 'this_week',
                 'order_price_type': 'optimal_10_ioc'},
             {'titleName': '当周 最优20档IOC', 'contest_type': 'this_week',
                 'order_price_type': 'optimal_20_ioc'},
             {'titleName': '当周 对手价FOK', 'contest_type': 'this_week',
                 'order_price_type': 'opponent_fok'},
             {'titleName': '当周 最优5档FOK', 'contest_type': 'this_week',
                 'order_price_type': 'optimal_5_fok'},
             {'titleName': '当周 最优10档FOK', 'contest_type': 'this_week',
                 'order_price_type': 'optimal_10_fok'},
             {'titleName': '当周 最优20档FOK', 'contest_type': 'this_week',
                 'order_price_type': 'optimal_20_fok'},
             {'titleName': '次周 限价单', 'contest_type': 'next_week',
                 'order_price_type': 'limit'},
             {'titleName': '次周 对手价', 'contest_type': 'next_week',
                 'order_price_type': 'opponent'},
             {'titleName': '次周 最优5档', 'contest_type': 'next_week',
                 'order_price_type': 'optimal_5'},
             {'titleName': '次周 最优10档', 'contest_type': 'next_week',
                 'order_price_type': 'optimal_10'},
             {'titleName': '次周 最优20档', 'contest_type': 'next_week',
                 'order_price_type': 'optimal_20'},
             {'titleName': '次周 only maker单', 'contest_type': 'next_week',
                 'order_price_type': 'post_only'},
             {'titleName': '次周 only fok单', 'contest_type': 'next_week',
                 'order_price_type': 'fok'},
             {'titleName': '次周 only ioc单', 'contest_type': 'next_week',
                 'order_price_type': 'ioc'},
             {'titleName': '次周 对手价IOC', 'contest_type': 'next_week',
                 'order_price_type': 'opponent_ioc'},
             {'titleName': '次周 最优5档IOC', 'contest_type': 'next_week',
                 'order_price_type': 'optimal_5_ioc'},
             {'titleName': '次周 最优10档IOC', 'contest_type': 'next_week',
                 'order_price_type': 'optimal_10_ioc'},
             {'titleName': '次周 最优20档IOC', 'contest_type': 'next_week',
                 'order_price_type': 'optimal_20_ioc'},
             {'titleName': '次周 对手价FOK', 'contest_type': 'next_week',
                 'order_price_type': 'opponent_fok'},
             {'titleName': '次周 最优5档FOK', 'contest_type': 'next_week',
                 'order_price_type': 'optimal_5_fok'},
             {'titleName': '次周 最优10档FOK', 'contest_type': 'next_week',
                 'order_price_type': 'optimal_10_fok'},
             {'titleName': '次周 最优20档FOK', 'contest_type': 'next_week', 'order_price_type': 'optimal_20_fok'}]
    symbol = DEFAULT_SYMBOL
    contract_code = DEFAULT_CONTRACT_CODE
    redisComm = redisConf('redis6379').instance()
    flag = False

    @classmethod
    @allure.step('前置条件')
    def setup(cls):
        print(''' 构造成交数据 ''')
        ATP.make_market_depth(depth_count=5)

    @classmethod
    def setup_class(cls):
        with allure.step('*->挂盘'):
            # 获取交割合约信息
            currContractInfo = user01.contract_contract_info(
                symbol=cls.symbol, contract_type='this_week')
            nextContractInfo = user01.contract_contract_info(
                symbol=cls.symbol, contract_type='next_week')
            cls.curr_contract_code = currContractInfo['data'][0]['contract_code']
            cls.next_contract_code = nextContractInfo['data'][0]['contract_code']
            cls.currentPrice = ATP.get_redis_current_price(
                contract_code=cls.curr_contract_code)  # 最新价

            user01.contract_order(symbol=cls.symbol, contract_code=cls.curr_contract_code, price=cls.currentPrice,
                                  direction='sell', volume=10)
            user01.contract_order(symbol=cls.symbol, contract_code=cls.next_contract_code, price=cls.currentPrice,
                                  direction='sell', volume=10)
            depth = cls.redisComm.hgetall('RsT:MarketBusinessPrice:')
            n = 0
            while not cls.flag:
                if cls.currentPrice not in depth:
                    n = n + 1
                    time.sleep(1)
                    if n > 10:
                        cls.flag = True
                else:
                    break
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('*->恢复环境:取消挂单'):
            user01.contract_cancelall(symbol=cls.symbol)
            pass

    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.skipif(condition=flag, reason='盘口环境问题，跳过以下依赖用例')
    @pytest.mark.parametrize('params', datas, ids=ids)
    def test_execute(self, symbol, params, DB_orderSeq):
        with allure.step('详见官方文档'):
            allure.dynamic.title(params['titleName'])
            self.contract_type = params['contest_type']
            if self.contract_type == 'this_week':
                self.contract_code = self.curr_contract_code
            elif self.contract_type == 'next_week':
                self.contract_code = self.next_contract_code
            orderInfo = user01.contract_order(symbol=symbol, contract_code=self.contract_code,
                                              price=round(
                                                  self.currentPrice, 2),
                                              contract_type=self.contract_type, direction='buy',
                                              order_price_type=params['order_price_type'])
            if "data" in orderInfo:
                orderId = orderInfo['data']['order_id']
                strStr = "select count(1) as c from t_exchange_match_result WHERE f_id = " \
                    "(select f_id from t_order_sequence where f_order_id= '%s')" % (
                        orderId)
                # 给撮合时间，5秒内还未撮合完成则为失败
                n = 0
                while n < 5:
                    isMatch = DB_orderSeq.selectdb_execute(
                        'order_seq', strStr)[0]['c']
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
