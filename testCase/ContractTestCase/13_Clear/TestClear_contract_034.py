#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/20
# @Author  : Alex Li
"""

所属分组
    定序,清算,落库,复核
用例标题
    用户APO中清算version数据跳号时，检查当周合约下成交情况
前置条件

步骤/文本
    # order_version_0#t_version_2999为版本号，修改小一点，例：1）
    1、连接redis， 根据key修改用户APO中的清算版本号数据 key:apo_clear_version,value：999
    2、当周合约下成交，记住user_order_id

预期结果
    1、当周合约下单后，下单成功，但是清算处理不成功
    2、检查数据库表中订单状态 （state=2，2则订单数据未被清算处理）select state from t_tmp_order_check where user_id='11226437' and product_id='ETH' and user_order_id='898607006221377536'

优先级
    0
"""

import time
import allure
import pytest
from common.ContractServiceAPI import t as contract_api, common_user_contract_service_api as common_contract_api
from common.redisComm import *
from common.mysqlComm import *
from tool.atp import ATP


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('定序,清算,落库,复核')  # 这里填功能
@allure.story('用户APO中清算version数据跳号时，检查当周合约下成交情况')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestClear_contract_026:
    params = [
        {"contract_type": "this_week",  "id": "TestClear_contract_034",
            "case_title": "用户APO中清算version数据跳号时，检查当周合约下成交情况"},
        {"contract_type": "next_week", "id": "TestClear_contract_035",
            "case_title": "用户APO中清算version数据跳号时，检查次周合约下成交情况"},
        {"contract_type": "quarter", "id": "TestClear_contract_036",
            "case_title": "用户APO中清算version数据跳号时，检查当季合约下成交情况"},
        {"contract_type": "next_quarter", "id": "TestClear_contract_037",
            "case_title": "用户APO中清算version数据跳号时，检查次季合约下成交情况"}
    ]

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol_period):
        print("前置条件 {}".format(symbol_period))

    @allure.step('测试执行')
    @pytest.mark.parametrize('param', params, ids=[x['id'] for x in params])
    def test_execute(self, symbol_period, symbol, param):
        allure.dynamic.title(param['case_title'])
        contract_type = param["contract_type"]
        with allure.step('1、连接redis， 根据key修改用户APO中的清算版本号数据 key:apo_clear_version,value：999#order_version_0#t_version_2999为版本号，修改小一点，例：1'):
            # redis 取值
            redis_client = redisConf('redis6380').instance()
            self.version_value = redis_client.hmget(
                "RsT:APO:11538447#{}".format(symbol), "apo_clear_version")[0]
            print(self.version_value)
            version_list = str.split(self.version_value, '#')
            self._sn = version_list[0]
            redis_client.hset("RsT:APO:11538447#{}".format(
                symbol), "apo_clear_version", "{}#{}#{}".format("1", version_list[1], version_list[2]))
            time.sleep(1)
        with allure.step('2、当周合约下成交，记住user_order_id'):
            current_price = ATP.get_current_price(
                contract_code=symbol_period)
            common_contract_api.contract_order(
                symbol=symbol, contract_type=contract_type, price=current_price, volume=1, direction='sell', offset='open')
            res = contract_api.contract_order(
                symbol=symbol, contract_type=contract_type, price=current_price, volume=1, direction='buy', offset='open')
            print(res)
            if "data" in res.keys():
                self._user_order_id = res["data"]["order_id_str"]
        with allure.step('2、检查数据库表中订单状态 （state=2，2则订单数据未被清算处理）'):
            btc_conn = mysqlComm()
            sqlStr = 'SELECT state FROM t_tmp_order_check WHERE user_id="{}" AND product_id="{}" AND user_order_id="{}"'.format(
                11538447, symbol, self._user_order_id)
            rec_dict = btc_conn.selectdb_execute(
                "btc", sqlStr)
            if len(rec_dict) > 0:
                assert rec_dict[0]["state"] == 2
                time.sleep(1)

        with allure.step('恢复apo_clear_version'):
            redis_client = redisConf('redis6380').instance()
            version_list = str.split(self.version_value, '#')
            print(version_list)
            redis_client.hset("RsT:APO:11538447#{}".format(
                symbol), "apo_clear_version", "{}#{}#{}".format(self._sn, version_list[1], version_list[2]))

    @ allure.step('恢复环境')
    @pytest.fixture(scope='function', autouse=True)
    def teardown(self, symbol):
        time.sleep(1)
        print('\n恢复环境操作')

        ATP.cancel_all_order()
        ATP.clean_market()


if __name__ == '__main__':
    pytest.main()
