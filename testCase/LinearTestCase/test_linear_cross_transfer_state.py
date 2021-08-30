#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/11/6
# @Author  : zhangranghan




from common.LinearServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError

from pprint import pprint
import pytest,allure,random,time



@allure.epic('正向永续')
@allure.feature('查询系统划转权限--全仓')
class TestLinearAdjustfactor:


    def test_linear_cross_transfer_state(self):
        r = t.linear_cross_transfer_state()
        pprint(r)
        schema = {
                    "status": str,
                    "data": [
                        {
                            "margin_mode": str,
                            "margin_account": str,
                            "transfer_in": Or(None,int),
                            "transfer_out": Or(None,int),
                            "master_transfer_sub": Or(None,int),
                            "sub_transfer_master": Or(None,int),
                            "master_transfer_sub_inner_in": Or(None,int),
                            "master_transfer_sub_inner_out": Or(None,int),
                            "sub_transfer_master_inner_in": Or(None,int),
                            "sub_transfer_master_inner_out": Or(None,int),
                            "transfer_inner_in": Or(None,int),
                            "transfer_inner_out": Or(None,int),

                        }
                    ],
                    "ts": int
                }

        Schema(schema).validate(r)





if __name__ == '__main__':
    pytest.main()
