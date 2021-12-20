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
from common.ContractServiceAPI import user01, user02, user03


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('撮合')  # 这里填功能
@allure.story('开多')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestContractEx_369:

    ids = ['TestContractEx_369',
           'TestContractEx_373',
           'TestContractEx_385',
           'TestContractEx_389',
           'TestContractEx_503',
           'TestContractEx_507',
           'TestContractEx_519',
           'TestContractEx_523']

    datas = [('quarter', '买入开仓 部分成交多人多笔价格相同的订单', 0, 1),
             ('quarter', '买入开仓 全部成交多人多笔价格相同的订单', 0, 2),
             ('quarter', '买入开仓 部分成交多人多笔价格不同的订单', 0.01, 1),
             ('quarter', '买入开仓 全部成交多人多笔价格不同的订单', 0.01, 2),
             ('next_quarter', '买入开仓 部分成交多人多笔价格相同的订单', 0, 1),
             ('next_quarter', '买入开仓 全部成交多人多笔价格相同的订单', 0, 2),
             ('next_quarter', '买入开仓 部分成交多人多笔价格不同的订单', 0.01, 1),
             ('next_quarter', '买入开仓 全部成交多人多笔价格不同的订单', 0.01, 2)]

    @allure.step('测试执行')
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('contest_type,caseName,ratio,volume', datas, ids=ids)
    def test_execute(self, symbol, contest_type, caseName, ratio, volume, DB_orderSeq):
        DB_orderSeq = mysqlComm('order_seq')
        with allure.step('详见官方文档'):
            allure.dynamic.title(caseName)
            self.contract_type = contest_type
            # 获取交割合约信息
            contractInfo = user01.contract_contract_info(
                symbol=symbol, contract_type=self.contract_type)
            self.contract_code = contractInfo['data'][0]['contract_code']
            self.currentPrice = ATP.get_current_price(
                contract_code=self.contract_code)
            orderIdList = []
            for user in [user01, user02]:
                for i in range(2):
                    orderInfo = user.contract_order(symbol=symbol, contract_code=self.contract_code,
                                                    price=round(
                                                        self.currentPrice*(1+(i+1)*ratio), 2),
                                                    contract_type=self.contract_type, direction='buy', volume=2)
                    orderId = orderInfo['data']['order_id']
                    orderIdList.append(orderId)
                    user03.contract_order(symbol=symbol, contract_code=self.contract_code,
                                          price=round(
                                              self.currentPrice*(1+(i+1)*ratio), 2),
                                          contract_type=self.contract_type, direction='sell', volume=volume)
                    user.contract_cancelall(symbol=symbol)

            strStr = "select count(1) as c from t_exchange_match_result WHERE f_id in " \
                     "(select f_id from t_order_sequence where f_order_id= '%s')" % (
                         orderId)
            # 给撮合时间，5秒内还未撮合完成则为失败
            n = 0
            while n < 5:
                isMatch = DB_orderSeq.selectdb_execute(
                    'order_seq', strStr)[0]['c']
                if 1 <= isMatch:
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
