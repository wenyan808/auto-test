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
@allure.feature('合约批量下单')
class TestLinearBatchorder:


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_batchorder(self,title,contract_code,client_order_id,volume,direction,offset,order_price_type,buy_price,lever_rate,status):
        r = t.linear_batchorder({"orders_data": [{
                                        "contract_code": contract_code,
                                        "client_order_id": client_order_id,
                                        "price": buy_price-1,
                                        "volume": volume,
                                        "direction": direction,
                                        "offset": offset,
                                        "lever_rate": lever_rate,
                                        "order_price_type": order_price_type}]})
        pprint(r)
        assert r['status'] == status




if __name__ == '__main__':
    pytest.main()
