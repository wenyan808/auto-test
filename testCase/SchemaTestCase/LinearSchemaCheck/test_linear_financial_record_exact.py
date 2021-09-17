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
@allure.feature('组合查询用户财务记录（全逐通用）')
class TestLinearFinancialRecordExact:


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_financial_record_exact(self,title,margin_account,contract_code,type,start_time,end_time,from_id,size,direct,status):
        r = t.linear_financial_record_exact(margin_account=margin_account,
                                            contract_code=contract_code,
                                            type=type,
                                            start_time=start_time,
                                            end_time=end_time,
                                            from_id=from_id,
                                            size=size,
                                            direct=direct)
        pprint(r)
        assert r['status'] == status


if __name__ == '__main__':
    pytest.main()
