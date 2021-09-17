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
@allure.feature('获取预测资金费率的K线数据')
class TestLinearEstimatedRateKline:


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_estimated_rate_kline(self,title,contract_code,period,size,status):
        r = t.linear_estimated_rate_kline(contract_code=contract_code,period=period,size=size)
        pprint(r)
        assert r['status'] == status


if __name__ == '__main__':
    pytest.main()
