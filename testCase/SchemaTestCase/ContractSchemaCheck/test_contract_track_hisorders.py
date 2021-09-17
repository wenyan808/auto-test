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
@allure.feature('查询跟踪委托订单历史委托')
class TestContractTrackHisorders:


    def test_contract_track_hisorders(self,symbol):

        r = t.contract_track_hisorders(symbol=symbol,status='0',trade_type='0',create_date='7')
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()
