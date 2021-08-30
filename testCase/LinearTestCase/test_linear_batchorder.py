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

    def setup(self):
        self.client_order_id = random.randint(1,999999)


    def test_linear_batchorder1(self,contract_code):
        r = t.linear_batchorder({"orders_data": [{
                                        "contract_code": contract_code,
                                        "client_order_id": '',
                                        "price": '50000',
                                        "volume": '1',
                                        "direction": 'buy',
                                        "offset": 'open',
                                        "lever_rate": '5',
                                        "order_price_type": 'limit'}]})
        pprint(r)
        schema = {
                    'data': {
                        'errors': [

                        ],
                        'success': [
                            {
                                'index': int,
                                'order_id': int,
                                'order_id_str': str
                            }
                        ]
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)


    @pytest.mark.schema
    @allure.story('字段校验')
    @allure.title('校验返回所有的字段及数据格式(包含client_order_id)')
    def test_linear_batchorder2(self,contract_code):
        r = t.linear_batchorder({"orders_data": [{
                                        "contract_code": contract_code,
                                        "client_order_id": self.client_order_id,
                                        "price": '50000',
                                        "volume": '1',
                                        "direction": 'buy',
                                        "offset": 'open',
                                        "lever_rate": '5',
                                        "order_price_type": 'limit'}]})
        pprint(r)
        schema = {
                    'data': {
                        'errors': [

                        ],
                        'success': [
                            {
                                'index': int,
                                'order_id': int,
                                'order_id_str': str,
                                'client_order_id': int
                            }
                        ]
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
