#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/17 3:07 下午
# @Author  : HuiQing Yu

from common.mysqlComm import mysqlComm as mysqlClient
from decimal import Decimal

import pytest, allure, time,random
from common.SwapServiceMGT import SwapServiceMGT
from common.mysqlComm import mysqlComm
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[4]['feature'])
@allure.story(features[4]['story'][3])
@allure.tag('Script owner : 余辉青', 'Case owner : ')
@pytest.mark.stable
class TestSwapMGTflat_001:
    ids = [
        # 'TestSwapMGTflat_001',
        # 'TestSwapMGTflat_002',
        # 'TestSwapMGTflat_003',
        # 'TestSwapMGTflat_004',
        # 'TestSwapMGTflat_005',
        # 'TestSwapMGTflat_006',
        'TestSwapMGTflat_007',
        # 'TestSwapMGTflat_008',
        # 'TestSwapMGTflat_009',
        # 'TestSwapMGTflat_010',
        # 'TestSwapMGTflat_011',
        # 'TestSwapMGTflat_012',
        # 'TestSwapMGTflat_013',
        # 'TestSwapMGTflat_014',
           ]
    params = [
        # {'title': 'TestSwapMGTflat_001', 'case_name': '用户保证金账户平账-加钱成功', 'flatAccount': 1, 'uuid': '115384838','money':random.randint(10,100)},
        # {'title': 'TestSwapMGTflat_002', 'case_name': '系统的爆仓账户-加钱成功', 'flatAccount': 2, 'uuid': '111862677','money':random.randint(10,100)},
        # {'title': 'TestSwapMGTflat_003', 'case_name': '系统的运营账户-加钱成功', 'flatAccount': 9, 'uuid': '13896090','money':random.randint(10,100)},
        # {'title': 'TestSwapMGTflat_004', 'case_name': '系统的借贷账户-加钱成功', 'flatAccount': 3, 'uuid': '111862660','money':random.randint(10,100)},
        # {'title': 'TestSwapMGTflat_005', 'case_name': '系统的交易手续费账户-加钱成功', 'flatAccount': 4, 'uuid': '13896070','money':random.randint(10,100)},
        # {'title': 'TestSwapMGTflat_006', 'case_name': '系统的互换账户-加钱成功', 'flatAccount': 5, 'uuid': '13896080','money':random.randint(10,100)},
        {'title': 'TestSwapMGTflat_007', 'case_name': '虚拟平台资产-加钱成功', 'flatAccount': 11, 'money': random.randint(10, 100)},
        # {'title': 'TestSwapMGTflat_008', 'case_name': '用户保证金账户平账-加钱成功', 'flatAccount': 1, 'uuid': '115384838',
        #  'money': -random.randint(10, 100)},
        # {'title': 'TestSwapMGTflat_009', 'case_name': '系统的爆仓账户-加钱成功', 'flatAccount': 2, 'uuid': '111862677',
        #  'money': -random.randint(10, 100)},
        # {'title': 'TestSwapMGTflat_010', 'case_name': '系统的运营账户-加钱成功', 'flatAccount': 9, 'uuid': '13896090',
        #  'money': -random.randint(10, 100)},
        # {'title': 'TestSwapMGTflat_011', 'case_name': '系统的借贷账户-加钱成功', 'flatAccount': 3, 'uuid': '111862660',
        #  'money': -random.randint(10, 100)},
        # {'title': 'TestSwapMGTflat_012', 'case_name': '系统的交易手续费账户-加钱成功', 'flatAccount': 4, 'uuid': '13896070',
        #  'money': -random.randint(10, 100)},
        # {'title': 'TestSwapMGTflat_013', 'case_name': '系统的互换账户-加钱成功', 'flatAccount': 5, 'uuid': '13896080',
        #  'money': -random.randint(10, 100)},
        # {'title': 'TestSwapMGTflat_014', 'case_name': '虚拟平台资产-加钱成功', 'flatAccount': 11, 'money': -random.randint(10, 100)},
    ]

    @classmethod
    def setup_class(cls):
        with allure.step('变量初始化'):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.symbol = DEFAULT_SYMBOL
            cls.mysqlClient = mysqlComm()
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params,SwapTool):
        allure.dynamic.title(params['title'])
        with allure.step('操作:查询用户当前保证金数量'):
            if 11==params['flatAccount']:
                pass
            else:
                static_interest = SwapTool.user_account(uid=params['uuid'][:-1]).split(',')[5]
            pass
        with allure.step('操作:执行-给用户保证金平账'):
            flatTime = int(round(time.time()*1000))
            if params['flatAccount'] == 1:
                api_result = SwapServiceMGT.flat(flatAccount=params['flatAccount'], uid=params['uuid'], money=params['money'])
            else:
                api_result = SwapServiceMGT.flat(flatAccount=params['flatAccount'], uid=None, money=params['money'])
            pass
        with allure.step('验证:平账执行成功'):
            assert '数据发送给交易系统成功' in api_result['data'],'接口执行失败'
            time.sleep(0.5)
            pass
        with allure.step('验证:用户保证金账户加钱数量与平账数量一致'):
            if 11==params['flatAccount']:
                sqlStr = ' select flat_account, flat_status ' \
                         'from t_flat_money_record ' \
                         f'where flat_time > {flatTime} ' \
                         f'and product_id = "{self.symbol}" ' \
                         'and operator = "yuhuiqing" limit 1'
                db_info = self.mysqlClient.selectdb_execute(dbSchema='btc',sqlStr=sqlStr)
                assert False,'环境问题，待完成'
                pass
            else:
                after_flat_static_interest = SwapTool.user_account(uid=params['uuid'][:-1]).split(',')[5]
                assert Decimal(static_interest) + Decimal(params['money']) == Decimal(after_flat_static_interest)
            pass