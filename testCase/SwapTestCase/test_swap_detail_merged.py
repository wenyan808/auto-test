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
@allure.feature('获取聚合行情')
class TestSwapDetailMerged:


    def test_swap_detail_merged(self,contract_code):

        r = t.swap_detail_merged(contract_code=contract_code)
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()
