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
@allure.feature('母子账户划转')
class TestLinearMasterSubTransfer:

    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_master_sub_transfer(self,title,sub_uid,asset,from_margin_account,to_margin_account,amount,type,status):
        r = t.linear_master_sub_transfer(sub_uid=sub_uid,
                                         asset=asset,
                                         from_margin_account=from_margin_account,
                                         to_margin_account=to_margin_account,
                                         amount=amount,
                                         type=type)
        pprint(r)
        assert r['status'] == status


if __name__ == '__main__':
    pytest.main()
