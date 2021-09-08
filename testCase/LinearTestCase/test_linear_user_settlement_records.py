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
@allure.feature('查询用户结算记录（逐仓）')
class TestLinearUserSettlementRecords:


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_user_settlement_records(self,title,contract_code,start_time,end_time,page_size,page_index,status):
        r = t.linear_user_settlement_records(contract_code=contract_code,
                                                 start_time=start_time,
                                                 end_time=end_time,
                                                 page_size=page_size,
                                                 page_index=page_index)
        pprint(r)
        assert r['status'] == status


if __name__ == '__main__':
    pytest.main()



