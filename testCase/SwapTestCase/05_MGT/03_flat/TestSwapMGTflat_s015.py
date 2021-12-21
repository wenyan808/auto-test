#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/17 3:07 下午
# @Author  : HuiQing Yu

from common.mysqlComm import mysqlComm as mysqlClient
from decimal import Decimal

import pytest, allure, time,random
from common.SwapServiceMGT import SwapServiceMGT
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL
from config.case_content import epic, features
from tool.SwapTools import SwapTool

@allure.epic(epic[1])
@allure.feature(features[4]['feature'])
@allure.story(features[4]['story'][3])
@allure.tag('Script owner : 余辉青', 'Case owner : ')
@pytest.mark.stable
class TestSwapMGTflat_s015:
    ids = ['TestSwapMGTflat_015',
           'TestSwapMGTflat_016',
           'TestSwapMGTflat_017',
           'TestSwapMGTflat_018',
           'TestSwapMGTflat_019',
           'TestSwapMGTflat_020',
           'TestSwapMGTflat_021',
           'TestSwapMGTflat_022',
           'TestSwapMGTflat_023',
           'TestSwapMGTflat_024',
           'TestSwapMGTflat_025',
           'TestSwapMGTflat_026',
           'TestSwapMGTflat_027',
           'TestSwapMGTflat_028',
           ]
    params = [
        {'title': 'TestSwapMGTflat_015', 'case_name': '用户保证金账户平账-加钱失败', 'flatAccount': 1, 'uuid': '115384838','money':random.randint(10,100)},
        {'title': 'TestSwapMGTflat_016', 'case_name': '系统的爆仓账户-加钱失败', 'flatAccount': 2, 'uuid': '111862677','money':random.randint(10,100)},
        {'title': 'TestSwapMGTflat_017', 'case_name': '系统的运营账户-加钱失败', 'flatAccount': 9, 'uuid': '13896090','money':random.randint(10,100)},
        {'title': 'TestSwapMGTflat_018', 'case_name': '系统的借贷账户-加钱失败', 'flatAccount': 3, 'uuid': '111862660','money':random.randint(10,100)},
        {'title': 'TestSwapMGTflat_019', 'case_name': '系统的交易手续费账户-加钱失败', 'flatAccount': 4, 'uuid': '13896070','money':random.randint(10,100)},
        {'title': 'TestSwapMGTflat_020', 'case_name': '系统的互换账户-加钱失败', 'flatAccount': 5, 'uuid': '13896080','money':random.randint(10,100)},
        {'title': 'TestSwapMGTflat_020', 'case_name': '平台虚拟资产-加钱失败', 'flatAccount': 11, 'money': random.randint(10, 100)},
        {'title': 'TestSwapMGTflat_022', 'case_name': '用户保证金账户平账-减钱失败', 'flatAccount': 1, 'uuid': '115384838',
         'money': -random.randint(10, 100)},
        {'title': 'TestSwapMGTflat_023', 'case_name': '系统的爆仓账户-减钱失败', 'flatAccount': 2, 'uuid': '111862677',
         'money': -random.randint(10, 100)},
        {'title': 'TestSwapMGTflat_024', 'case_name': '系统的运营账户-减钱失败', 'flatAccount': 9, 'uuid': '13896090',
         'money': -random.randint(10, 100)},
        {'title': 'TestSwapMGTflat_025', 'case_name': '系统的借贷账户-减钱失败', 'flatAccount': 3, 'uuid': '111862660',
         'money': -random.randint(10, 100)},
        {'title': 'TestSwapMGTflat_026', 'case_name': '系统的交易手续费账户-减钱失败', 'flatAccount': 4, 'uuid': '13896070',
         'money': -random.randint(10, 100)},
        {'title': 'TestSwapMGTflat_027', 'case_name': '系统的互换账户-减钱失败', 'flatAccount': 5, 'uuid': '13896080',
         'money': -random.randint(10, 100)},
        {'title': 'TestSwapMGTflat_028', 'case_name': '平台虚拟资产-减钱失败', 'flatAccount': 11,
         'money': random.randint(10, 100)},
    ]
    symbol = SwapTool.getContractStatus(init_status=0)['product_id']

    @classmethod
    def setup_class(cls):
        with allure.step('获取结算中的合约'):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['title'])
        with allure.step('操作:执行-给用户保证金平账'):
            if params['flatAccount'] == 1:
                api_result = SwapServiceMGT.flat(flatAccount=params['flatAccount'], uid=params['uuid'], money=params['money'])
            else:
                api_result = SwapServiceMGT.flat(flatAccount=params['flatAccount'], uid=None, money=params['money'])
            pass
        with allure.step('验证:平账执行失败'):
            assert '此合约在非交易状态中' or '该品种的状态不是交易中或者停牌' in api_result['data'],'接口执行失败'
            pass
