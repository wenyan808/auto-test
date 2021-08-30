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
@allure.feature('批量设置子账户交易权限（全逐通用）')
class TestLinearSubAuth:

    def test_linear_sub_auth(self,sub_uid):
        r = t.linear_sub_auth(sub_uid=sub_uid,sub_auth='1')
        pprint(r)
        schema = {'data': {'errors': list,
                           'successes': str},
                         'status': 'ok',
                         'ts': int}

        Schema(schema).validate(r)



if __name__ == '__main__':
    pytest.main()
