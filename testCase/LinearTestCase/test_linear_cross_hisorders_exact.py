#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/8/7
# @Author  : zhangranghan



from common.LinearServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError

from pprint import pprint
import pytest,allure,random,time

@allure.epic('正向永续')
@allure.feature('组合查询合约历史委托（全仓）')
class TestLinearCrossHisordersExact:



    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_cross_hisorders_exact(self,title,contract_code,trade_type,type,status,order_price_type,start_time,end_time,from_id,size,direct,STATUS):
        r = t.linear_cross_hisorders_exact(contract_code=contract_code,
                                           trade_type=trade_type,
                                           type=type,
                                           status=status,
                                           order_price_type=order_price_type,
                                           start_time=start_time,
                                           end_time=end_time,
                                           from_id=from_id,
                                           size=size,
                                           direct=direct)
        pprint(r)
        assert r['status'] == STATUS



if __name__ == '__main__':
    pytest.main()
