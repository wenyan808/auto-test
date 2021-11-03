#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211027
# @Author : 
    用例标题
        撮合次周 最优10档 卖出 开仓               
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        正确撮合
    优先级
        2
    用例别名
        TestContractEx_148
"""

from common.ContractServiceAPI import t as contract_api
from pprint import pprint
import pytest, allure, random, time
from tool.atp import ATP
from common.mysqlComm import orderSeq as DB_orderSeq
import pymysql


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('撮合')  # 这里填功能
@allure.story('委托单')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 张广南', 'Case owner : 吉龙')
class TestContractEx_148:

    @allure.step('前置条件')
    def setup(self):
        ATP.cancel_all_types_order()
        self.from_time = int(time.time())
        print(''' 制造成交数据 ''')
        ATP.make_market_depth()

    @allure.title('撮合次周 最优10档 卖出 开仓               ')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('详见官方文档'):
            contracttype = 'next_week'
            leverrate = 5
            # 获取当周合约
            sell_price = ATP.get_adjust_price(1.02)
            buy_price = ATP.get_adjust_price(0.98)
            print('\n步骤一:获取最近价\n')

            sell_order = contract_api.contract_order(symbol=symbol, contract_type=contracttype, price=sell_price,
                                                     volume='1',
                                                     direction='sell', offset='close', lever_rate=leverrate,
                                                     order_price_type='optimal_10')
            pprint(sell_order)
            buy_order = contract_api.contract_order(symbol=symbol, contract_type=contracttype, price=buy_price,
                                                    volume='1',
                                                    direction='buy', offset='open', lever_rate=leverrate,
                                                    order_price_type='limit')
            pprint(buy_order)

            time.sleep(1)
            self.current_price = ATP.get_current_price()
            orderId = sell_order['data']['order_id']
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

    def getdbconnection(self, dbConf):
        pprint("before not")
        if not self._is_init:
            pprint("after not")
            dbConfProperties = str(dbConf).split(';')
            self.__host = dbConfProperties[0]
            self.__port = int(dbConfProperties[1])
            self.__userName = dbConfProperties[2]
            self.__password = dbConfProperties[3]
            self.__dbName = dbConfProperties[4]
            try:
                pprint("before db")
                self.__db = pymysql.connect(host=self.__host, port=self.__port, user=self.__userName,
                                            password=self.__password, database=self.__dbName)
                pprint("after db")
                self._is_init = True
            except Exception as e:
                pprint('pymysql.connect Fail')
                pprint(e)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.clean_market()


if __name__ == '__main__':
    pytest.main()