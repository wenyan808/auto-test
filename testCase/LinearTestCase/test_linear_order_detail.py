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
@allure.feature('获取用户的合约订单明细信息')
class TestLinearOrderDetail:


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_order_detail(self,title,contract_code,sell_price,lever_rate,order_type,page_index,page_size,status):
        a = t.linear_order(contract_code=contract_code,
                       client_order_id='',
                       price=sell_price,
                       volume='1',
                       direction='buy',
                       offset='open',
                       lever_rate=lever_rate,
                       order_price_type='limit')
        time.sleep(1)
        order_id = a['data']['order_id']
        created_at = a['ts']
        r = t.linear_order_detail(contract_code=contract_code,
                                  order_id=order_id,
                                  created_at=created_at,
                                  order_type=order_type,
                                  page_index=page_index,
                                  page_size=page_size)
        pprint(r)
        assert r['status'] == status


if __name__ == '__main__':
    pytest.main()
