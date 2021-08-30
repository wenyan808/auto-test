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
@allure.feature('获取标记价格的K线数据')
class TestContractMarkPriceKline:


    def test_contract_mark_price_kline(self,symbol_period):

        r = t.contract_mark_price_kline(symbol=symbol_period,period='1min',size='20')
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()