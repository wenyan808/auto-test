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
@allure.feature('获取母账户下的所有母子账户的划转记录')
class TestSwapMasterSubTransferRecord:


    def test_swap_master_sub_transfer_record(self,contract_code):

        r = t.swap_master_sub_transfer_record(contract_code=contract_code,transfer_type='34',create_date='7',page_index='',page_size='')
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()