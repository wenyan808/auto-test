#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/9
# @Author  : Alex Li
"""
    用例标题
        母用户当前无挂单切换杠杆倍数测试
    前置条件
        1、用户在该业务线下已开户
        2、用户在合约下没有任何挂单
        
    步骤/文本
        1、在币本位交割合约交易页，选择币本位交割当周合约，检查杠杆倍数
        2、在杠杆滑动条上，切换杠杆倍数至20倍，点击"确定"按钮
        3、在杠杆滑动条上，切换杠杆倍数至1倍，点击"确定"按钮
    预期结果
        1、杠杆倍数显示正常（如5X），且用户RsT:APO:user_id#品种(如RsT:APO:11448828#BTC)->leverRate值及t_account_capital表中`leverage`用户币本位交割当周的杠杆倍数值数据相等
        2、切换杠杆倍数至20倍成功，且用户RsT:APO:user_id#品种(如RsT:APO:11448828#BTC)->leverRate值及t_account_capital表中`leverage`用户币本位交割当周的杠杆倍数值数据相等
        3、切换杠杆倍数至1倍成功，且用户RsT:APO:user_id#品种(如RsT:APO:11448828#BTC)->leverRate值及t_account_capital表中`leverage`用户币本位交割当周的杠杆倍数值数据相等
    优先级
        0
    用例别名
        TestContractLever_017
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractMGTServiceAPI import t as contract_mgt_api
import json
import pytest
import allure
import random
from common.redisComm import *
from common.mysqlComm import *
from tool.atp import ATP
from schema import Schema


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('切换杠杆')  # 这里填功能
@allure.story('在币本位交割合约交易页，选择币本位交割当周合约，检查杠杆倍数')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : 叶永刚')
@pytest.mark.stable
class TestContractLever_s001:

    params = [
        {"contract_type": "this_week", "case_title": "母用户- 币本位交割当周-无持仓切换杠杆倍数",
            "id": "TestContractLever_017"},
        {"contract_type": "next_week", "case_title": "母用户- 币本位交割次周-无持仓切换杠杆倍数",
            "id": "TestContractLever_018"},
        {"contract_type": "quarter", "case_title": "母用户- 币本位交割当季-无持仓切换杠杆倍数",
            "id": "TestContractLever_19"},
        {"contract_type": "next_quarter",
            "case_title": "母用户- 币本位交割次季-无持仓切换杠杆倍数", "id": "TestContractLever_020"},
        {"contract_type": "this_week", "case_title": "母用户- 币本位交割当周-切换杠杆倍数-高倍杠杆-有持仓且允许有持仓切换杠杆",
         "id": "TestContractLever_025"},
        {"contract_type": "next_week", "case_title": "母用户- 币本位交割当周-切换杠杆倍数-高倍杠杆-有持仓且允许有持仓切换杠杆",
            "id": "TestContractLever_026"},
        {"contract_type": "quarter", "case_title": "母用户- 币本位交割当周-切换杠杆倍数-高倍杠杆-有持仓且允许有持仓切换杠杆",
            "id": "TestContractLever_27"},
        {"contract_type": "next_quarter",
            "case_title": "母用户- 币本位交割当周-切换杠杆倍数-高倍杠杆-有持仓且允许有持仓切换杠杆", "id": "TestContractLever_028"},
    ]

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol_period):
        # 清仓和取消挂单才能切杠杆
        ATP.cancel_all_types_order(contract_code=symbol_period)
        ATP.make_market_depth(contract_code=symbol_period, depth_count=5)
        print("前置条件：{}", symbol_period)
        # 确保“允许在有持仓时切换杠杆”打开
        params = [{"id": 989, "dictClass": "cutLever",
                   "dictValue": 1, "dictNameCn": "1", "dictNameEn": "1"}]
        form_params = "params={}".format(str(params))
        result = contract_mgt_api.cutLeverWhiteListService_updateCutLeverByPrimaryKey(
            form_params)
        print(result)
        assert result["errorCode"] == 0

    @allure.title('母用户- 币本位交割当周-切换杠杆倍数')
    @allure.step('测试执行')
    @pytest.mark.parametrize('param', params, ids=[x['id'] for x in params])
    def test_execute(self, symbol_period, symbol, param):
        allure.dynamic.title(param['case_title'])
        currentPrice = ATP.get_current_price(contract_code=symbol_period)
        with allure.step('1、在币本位交割合约交易页，选择币本位交割当周合约，检查杠杆倍数'):
            res = contract_api.contract_available_level_rate(symbol=symbol)
            availableleverlist = res['data'][0]['available_level_rate'].split(
                ',')
            print(availableleverlist)
            # 获取合约号
            res_contract_info = contract_api.contract_contract_info(
                contract_type=param["contract_type"])
            self._contract_code = res_contract_info['data'][0]['contract_code']
        with allure.step('2、将杠杆倍数切换为任意值'):
            self._lever_rate = random.choice(availableleverlist)
            res = contract_api.contract_switch_lever_rate(
                symbol=symbol, lever_rate=self._lever_rate)
            print(res)
            if res['status'] == 'ok':
                contract_api.contract_order(
                    symbol=symbol, contract_type=param["contract_type"], price=currentPrice, volume=1, lever_rate=self._lever_rate, direction="buy", offset="open", order_price_type="limit")

                redis_client = redisConf('redis6380').instance()
                redis_result = redis_client.hget(
                    "RsT:APO:11538447#{}".format(symbol), "orderPositionFrozen:{}#1".format(self._contract_code))[0]
                redis_dic = json.loads(redis_result)
                self._redis_lever_rate = redis_dic["leverage"]
                with allure.step('3、Redis 值对比'):
                    assert self._redis_lever_rate == self._lever_rate

                with allure.step('4、数据库 值对比'):
                    btc_conn = mysqlComm()
                    sqlStr = 'SELECT leverage FROM t_account_capital WHERE user_id="{}" AND product_id="{}" AND user_order_id="{}"'.format(
                        11538447, symbol)
                    print(sqlStr)
                    rec_db_dic = btc_conn.selectdb_execute("btc", sqlStr)
                    if(len(rec_db_dic) > 0):
                        rec_db_dic[0]["leverage"] == self._redis_lever_rate
            else:  # {'status': 'error', 'err_code': 1045, 'err_msg': '当前有挂单,无法切换倍数', 'ts': 1640760719058}
                schema = {'status': str, 'err_code': int,
                          'err_msg': str, 'ts': int}
                Schema(schema).validate(res)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_types_order()


if __name__ == '__main__':
    pytest.main()
