#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211027
# @Author : HuiQing Yu

from tool.atp import ATP
import pytest
import allure
import random
import time
from common.mysqlComm import mysqlComm
from common.ContractServiceAPI import user01


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('撮合')  # 这里填功能
@allure.story('平多')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestContractEx_393:
    ids = ['TestContractEx_393',
           'TestContractEx_394',
           'TestContractEx_395',
           'TestContractEx_527',
           'TestContractEx_528',
           'TestContractEx_529']

    datas = [('当季 lightning 卖出平仓', 'quarter', 'lightning'),
             ('当季 lightning_ioc 卖出平仓', 'quarter', 'lightning_ioc'),
             ('当季 lightning_fok 卖出平仓', 'quarter', 'lightning_fok'),
             ('次季 lightning 卖出平仓', 'next_quarter', 'lightning'),
             ('次季 lightning_ioc 卖出平仓', 'next_quarter', 'lightning_ioc'),
             ('次季 lightning_fok 卖出平仓', 'next_quarter', 'lightning_fok')]

    @allure.step('测试执行')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.parametrize('caseName,contest_type,order_price_type', datas, ids=ids)
    def test_execute(self, symbol, caseName, contest_type, order_price_type, DB_orderSeq):
        with allure.step('详见官方文档'):
            allure.dynamic.title(caseName)
            self.contract_type = contest_type
            # 获取交割合约信息
            contractInfo = user01.contract_contract_info(
                symbol=symbol, contract_type=self.contract_type)
            self.contract_code = contractInfo['data'][0]['contract_code']
            self.currentPrice = ATP.get_redis_current_price(
                contract_code=self.contract_code)  # 最新价
            # 持仓
            user01.contract_order(symbol=symbol, contract_code=self.contract_code,
                                  price=round(self.currentPrice, 2),
                                  contract_type=self.contract_type, direction='sell')
            user01.contract_order(symbol=symbol, contract_code=self.contract_code,
                                  price=round(self.currentPrice, 2),
                                  contract_type=self.contract_type, direction='buy')
            time.sleep(1)
            # 平仓
            user01.contract_order(symbol=symbol, contract_code=self.contract_code,
                                  price=round(self.currentPrice, 2),
                                  contract_type=self.contract_type, direction='buy', offset='close')
            orderInfo = user01.lightning_close_position(symbol=symbol, contract_code=self.contract_code,
                                                        order_price_type=order_price_type,
                                                        contract_type=self.contract_type, direction='sell')
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
            user01.contract_cancelall(symbol=symbol)
            pass


if __name__ == '__main__':
    pytest.main()
