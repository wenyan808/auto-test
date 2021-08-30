#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/10/13
# @Author  : zhangranghan




from common.SwapServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError

from pprint import pprint
import pytest,allure,random,time


@allure.epic('反向永续')
@allure.feature('组合查询用户历史成交记录')
class TestSwapMatchresultsExact:


    def test_swap_matchresults_exact(self,contract_code):

        r = t.swap_matchresults_exact(contract_code=contract_code,
                                      trade_type='0',
                                      start_time='',
                                      end_time='',
                                      from_id='',
                                      size='',
                                      direct='')
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()