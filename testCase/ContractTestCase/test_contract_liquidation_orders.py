#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : zhangranghan

from common.ContractServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError
from pprint import pprint
import pytest,allure,random,time



@allure.epic('反向交割')
@allure.feature('获取强平订单')
class TestContractLiquidationOrders:


    def test_contract_liquidation_orders(self,symbol):

        r = t.contract_liquidation_orders(symbol=symbol,
                                          trade_type='0',
                                          create_date='7',
                                          page_index='',
                                          page_size='')
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()