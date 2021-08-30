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
@allure.feature('批量设置子账户交易权限')
class TestSwapSubAuth:


    def test_swap_sub_auth(self,sub_uid):

        r = t.swap_sub_auth(sub_uid=sub_uid,sub_auth='1')
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()