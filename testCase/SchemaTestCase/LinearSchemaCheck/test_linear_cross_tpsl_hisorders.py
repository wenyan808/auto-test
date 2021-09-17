#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/8/7
# @Author  : zhangranghan


from common.LinearServiceAPI import t
import pytest, allure


@allure.epic('正向永续')
@allure.feature('查询止盈止损订单历史委托（全仓）')
class TestLinearCrossTpslHisorders:

    def test_linear_cross_tpsl_hisorders(self, api_test_data):
        r = t.linear_cross_tpsl_hisorders(**api_test_data)
        assert r['status'] == api_test_data['STATUS']


if __name__ == '__main__':
    pytest.main()
