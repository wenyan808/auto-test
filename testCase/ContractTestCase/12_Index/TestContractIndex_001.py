#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211008
# @Author : Donglin Han

所属分组
    合约测试基线用例//01 交割合约//12 指数
用例标题
    校验交割业务线指数是否正常计算
前置条件
    打开了合约交割的交易界面
步骤/文本
    1、通过接口获取某个品种的指数（例如BTC-USD）
    2、对比指数接口两次的数据
    3、校验指数是否有变化
预期结果
    1）品种的指数价格有正常变化
优先级
    0
用例编号
    TestContractIndex_001
自动化作者
    韩东林
"""

import time

import allure
import pytest

from common.ContractServiceAPI import t as contract_api
from config import conf
from tool.atp import ATP


def check_index_res(res, symbol):
    assert_err_msg = "获取指数价出错: {res}".format(res=res)
    res_data = res.get('data', [])
    assert len(res_data) == 1, assert_err_msg
    assert isinstance(res_data[0], dict), assert_err_msg

    index_price = res_data[0].get('index_price', -1)
    index_symbol = res_data[0].get('symbol', '')
    assert index_price > 0, "指数价格不正确：{res} ".format(res=res)
    assert index_symbol == symbol.upper(), "symbol 不正确：{res} ".format(res=res)
    return index_price


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('合约测试基线用例//01 交割合约//12 指数')  # 这里填功能
@allure.story('校验交割业务线指数是否正常计算')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Donglin Han', 'Case owner : Donglin Han')
@pytest.mark.stable
class TestContractIndex_001:

    @allure.step('前置条件')
    def setup(self):
        print(''' 打开了合约交割的交易界面 ''')

    @allure.title('校验交割业务线指数是否正常计算')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('1、通过接口获取某个品种的指数（例如BTC-USD）'):
            first_index_res = contract_api.contract_index(symbol)
            first_index_price = check_index_res(first_index_res, symbol)

        with allure.step('2、对比指数接口两次的数据'):
            time.sleep(1.05)
            second_index_res = contract_api.contract_index(symbol)
            second_index_price = check_index_res(second_index_res, symbol)

        with allure.step('3、校验指数是否有变化'):
            print()
            print(f'first_index_price : {first_index_price}')
            print(f'second_index_price : {second_index_price}')
            if conf.ENV.startswith('Test'):
                assert first_index_price == second_index_price
            else:
                assert first_index_price != second_index_price

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_order()


if __name__ == '__main__':
    pytest.main()
