#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/9
# @Author  : Alex Li
"""
    用例标题
        母用户- 币本位交割当周-切换杠杆倍数-有持仓且禁止有持仓切换杠杆
    前置条件
        母账户切换杠杆不设置功能白名单
        
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
        TestContractLever_s033
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
class TestContractLever_s049:

    params = [
        {"contract_type": "this_week", "case_title": "母用户- 币本位交割当周-切换杠杆倍数-有持仓且禁止有持仓切换杠杆",
            "id": "TestContractLever_049", "lever_rate": 5},
        {"contract_type": "next_week", "case_title": "母用户- 币本位交割次周-切换杠杆倍数-有持仓且禁止有持仓切换杠杆",
            "id": "TestContractLever_050", "lever_rate": 5},
        {"contract_type": "quarter", "case_title": "母用户- 币本位交割当季-切换杠杆倍数-有持仓且禁止有持仓切换杠杆",
            "id": "TestContractLever_051", "lever_rate": 5},
        {"contract_type": "next_quarter",
            "case_title": "母用户- 币本位交割次季-切换杠杆倍数-有持仓且禁止有持仓切换杠杆", "id": "TestContractLever_052", "lever_rate": 5},
        {"contract_type": "this_week", "case_title": "母用户- 币本位交割当周-切换杠杆倍数-高倍杠杆-有持仓且禁止有持仓切换杠杆",
         "id": "TestContractLever_057", "lever_rate": 50},
        {"contract_type": "next_week", "case_title": "母用户- 币本位交割当周-切换杠杆倍数-高倍杠杆-有持仓且禁止有持仓切换杠杆",
            "id": "TestContractLever_058", "lever_rate": 50},
        {"contract_type": "quarter", "case_title": "母用户- 币本位交割当周-切换杠杆倍数-高倍杠杆-有持仓且禁止有持仓切换杠杆",
            "id": "TestContractLever_059", "lever_rate": 50},
        {"contract_type": "next_quarter",
            "case_title": "母用户- 币本位交割当周-切换杠杆倍数-高倍杠杆-有持仓且禁止有持仓切换杠杆", "id": "TestContractLever_060", "lever_rate": 50},
    ]

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol, symbol_period):
        # 清仓和取消挂单才能切杠杆
        ATP.cancel_all_types_order(contract_code=symbol_period)
        ATP.make_market_depth(contract_code=symbol_period, depth_count=5)
        print("前置条件：{}", symbol_period)
        # 构造持仓
        currentPrice = ATP.get_current_price()  # 最新价
        contract_api.contract_order(
            symbol=symbol, price=currentPrice, direction='buy', volume=1)

        # 确保“允许在有持仓时切换杠杆”禁止
        params = [{"id": 989, "dictClass": "cutLever",
                   "dictValue": 1, "dictNameCn": "0", "dictNameEn": "0"}]
        form_params = "params={}".format(str(params))
        result = contract_mgt_api.cutLeverWhiteListService_updateCutLeverByPrimaryKey(
            form_params)
        print(result)
        assert result["errorCode"] == 0
        # 白名单中删除当前用户
        params = [{"uid": "115384476", "remark": "11538447"}]
        form_params = "params={}".format(str(params))
        result = contract_mgt_api.cutLeverWhiteListService_insertCutLeverWhiteList(
            form_params)
        print(result)

    @allure.title('母用户- 币本位交割当周-切换杠杆倍数')
    @allure.step('测试执行')
    @pytest.mark.parametrize('param', params, ids=[x['id'] for x in params])
    def test_execute(self, symbol_period, symbol, param):
        allure.dynamic.title(param['case_title'])
        currentPrice = ATP.get_current_price(contract_code=symbol_period)
        with allure.step('1、在币本位交割合约交易页，选择币本位交割当周合约，检查杠杆倍数'):
            res = contract_api.contract_switch_lever_rate(
                symbol=symbol, lever_rate=param["lever_rate"])
            if param["lever_rate"] == 5:
                # 允许切换
                print(res)
            else:
                # 不允许切换
                print(res)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
