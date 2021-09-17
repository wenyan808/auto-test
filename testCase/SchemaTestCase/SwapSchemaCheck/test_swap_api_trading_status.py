#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/8/19
# @Author  : zhangranghan



from common.SwapServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError

from pprint import pprint
import pytest,allure,random,time

@allure.epic('反向永续')
@allure.feature('获取用户的API指标禁用信息')
class TestSwapApiTradingStatus:


    def test_swap_api_trading_status(self):

        r = t.swap_api_trading_status()
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()