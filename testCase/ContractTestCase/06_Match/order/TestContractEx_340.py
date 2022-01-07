#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : HuiQing Yu

from tool.atp import ATP
import pytest
import allure
import time
from common.mysqlComm import mysqlComm
from common.ContractServiceAPI import user01


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('撮合')  # 这里填功能
@allure.story('平多')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestContractEx_340:
    ids = ['TestContractEx_340', 'TestContractEx_474']
    datas = [('当季 卖出平仓挂单 撤单', 'quarter'), ('次季 卖出平仓挂单 撤单', 'next_quarter')]

    @allure.step('测试执行')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.parametrize('case_name,contest_type', datas, ids=ids)
    def test_execute(self, symbol, case_name, contest_type, DB_orderSeq):
        with allure.step('详见官方文档'):
            allure.dynamic.title(case_name)
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
                                  contract_type=self.contract_type, direction='buy')
            user01.contract_order(symbol=symbol, contract_code=self.contract_code,
                                  price=round(self.currentPrice, 2),
                                  contract_type=self.contract_type, direction='sell')
            # 平仓挂单
            orderInfo = user01.contract_order(symbol=symbol, contract_code=self.contract_code,
                                              price=round(
                                                  self.currentPrice * 1.05, 2),
                                              contract_type=self.contract_type, direction='sell', offset='close')
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
            # 撤单
            user01.contract_cancelall(symbol=symbol)
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
