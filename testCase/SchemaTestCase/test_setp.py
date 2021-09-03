#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/9/2
# @Author  : zhangranghan



from common.LinearServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError
from pprint import pprint
import pytest,allure



@allure.feature('setp')
class TestSetp:

    @allure.title('获取合约用户账户信息')
    @allure.description('这是注释1')
    @allure.step('步骤1')
    def test_setp(self):
        """
        这是注释2
        """
        print('111')

    @allure.title('获取合约用户账户信息')
    @allure.description('这是注释1')
    @allure.step('步骤2')
    def test_setp1(self):
        """
        这是注释2
        """
        print('222')

if __name__ == '__main__':
    pytest.main()