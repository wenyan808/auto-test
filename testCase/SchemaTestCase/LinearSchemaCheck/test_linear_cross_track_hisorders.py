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
@allure.feature('获取跟踪委托历史委托(全仓)')
class TestLinearCrossTrackHisorders:


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_cross_track_hisorders(self,title,contract_code,status,trade_type,create_date,page_size,page_index,sort_by,STATUS):
        r = t.linear_cross_track_hisorders(contract_code=contract_code,
                                             status=status,
                                             trade_type=trade_type,
                                             create_date=create_date,
                                             page_size=page_size,
                                             page_index=page_index,
                                             sort_by=sort_by)
        pprint(r)
        assert r['status'] == STATUS



if __name__ == '__main__':
    pytest.main()
