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
@allure.feature('切换杠杆倍数 （逐仓）')
class TestLinearSwitchLeverRate:

    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_switch_lever_rate(self,title,contract_code,lever_rate,status):
        r = t.linear_switch_lever_rate(contract_code=contract_code,lever_rate=lever_rate)
        pprint(r)
        assert r['status'] == status


if __name__ == '__main__':
    pytest.main()



