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
@allure.feature('获取用户API指标禁用信息')
class TestLinearApiTradingStatus:

    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_api_trading_status(self,title,status):
        r = t.linear_api_trading_status()
        pprint(r)
        assert r['status'] == status



if __name__ == '__main__':
    pytest.main()
