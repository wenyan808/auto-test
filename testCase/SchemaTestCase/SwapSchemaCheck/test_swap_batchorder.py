#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/10/13
# @Author  : zhangranghan

import allure
import pytest

from common.SwapServiceAPI import t


@allure.epic('反向永续')
@allure.feature('合约批量下单')
class TestSwapBatchorder:

    def test_swap_batchorder(self, contract_code):
            r = t.swap_batchorder({"orders_data": [{
                "contract_code": contract_code,
                "client_order_id": '',
                "price": '1',
                "volume": '1',
                "direction": 'buy',
                "offset": 'open',
                "lever_rate": '5',
                "order_price_type": 'limit'},
                {
                    "contract_code": contract_code,
                    "client_order_id": '',
                    "price": '2',
                    "volume": '1',
                    "direction": 'buy',
                    "offset": 'open',
                    "lever_rate": '5',
                    "order_price_type": 'limit'}]})




if __name__ == '__main__':
    pytest.main()
