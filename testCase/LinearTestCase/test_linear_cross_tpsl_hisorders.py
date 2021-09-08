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
@allure.feature('查询止盈止损订单历史委托（全仓）')
class TestLinearCrossTpslHisorders:


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_cross_tpsl_hisorders(self,title,contract_code,status,create_date,page_size,page_index,sort_by,STATUS):
        r = t.linear_cross_tpsl_hisorders(contract_code=contract_code,
                                            status=status,
                                            create_date=create_date,
                                            page_size=page_size,
                                            page_index=page_index,
                                            sort_by=sort_by)
        pprint(r)
        assert r['status'] == STATUS


if __name__ == '__main__':
    pytest.main()
