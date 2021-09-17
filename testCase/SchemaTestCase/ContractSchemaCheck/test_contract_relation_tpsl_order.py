

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : zhangranghan

from common.ContractServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError
from pprint import pprint
import pytest,allure,random,time



@allure.epic('反向交割')
@allure.feature('查询开仓单关联的止盈止损订单详情接口')
class TestContractTpslRelationTpslOrder:


    def test_contract_relation_tpsl_order(self,symbol):

        a = t.contract_order(symbol=symbol,
                             contract_type='this_week',
                             contract_code='',
                             client_order_id='',
                             price=50000,
                             volume=1,
                             direction='buy',
                             offset='open',
                             lever_rate=5,
                             order_price_type='limit',
                             tp_order_price='50000',
                             tp_order_price_type='limit',
                             tp_trigger_price='60000')
        r = t.contract_relation_tpsl_order(symbol='btc',order_id=a['data']['order_id'])
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()