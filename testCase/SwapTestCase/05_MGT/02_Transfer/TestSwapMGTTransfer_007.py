#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/8 10:29 上午
# @Author  : HuiQing Yu
from decimal import Decimal

import pytest, allure, random, time
from common.SwapServiceMGT import SwapServiceMGT
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[4]['feature'])
@allure.story(features[4]['story'][2])
@allure.tag('Script owner : 余辉青', 'Case owner : 程卓')
@pytest.mark.stable
class TestSwapMGTTransfer_007:
    ids = [
           'TestSwapMGTTransfer_007',
           'TestSwapMGTTransfer_006',
           'TestSwapMGTTransfer_005',
           'TestSwapMGTTransfer_004',
           ]
    params = [
        {
            "case_name": "运营账户-转账到-用户保证金账户：返利",
            "request_params": {
                "userAmountList": [{"uid": "115384842", "amount": "77"}],
                "transType": 29,
                "transferInAccount": 1,
                "transferOutAccount": 9,
                "quantity": None
            }
        },
        {
            "case_name": "运营账户-转账到-用户保证金账户：活动奖励",
            "request_params": {
                "userAmountList": [{"uid": "115384842", "amount": "77"}],
                "transType": 28,
                "transferInAccount": 1,
                "transferOutAccount": 9,
                "quantity": None
            }
        },
        {
            "case_name": "用户保证金账户-转账到-运营账户：扣减用户资产-惩戒",
            "request_params": {
                "userAmountList": [{"uid": "115384842", "amount": "77"}],
                "transType": 27,
                "transferInAccount": 9,
                "transferOutAccount": 1,
                "quantity": None
            }
        },
        {
            "case_name": "运营账户-转账到-用户保证金账户：给用户赠币-赔偿",
            "request_params": {
                "userAmountList": [{"uid": "115384842", "amount": "77"}],
                "transType": 26,
                "transferInAccount": 1,
                "transferOutAccount": 9,
                "quantity": None
            }
        },
    ]

    @classmethod
    def setup_class(cls):
        with allure.step('变量初始化'):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.symbol = DEFAULT_SYMBOL
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params, DB_contract_trade):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：执行转账'):
            transfer = SwapServiceMGT.saveTransfer(symbol=self.symbol,userAmountList=params['request_params']['userAmountList'],
                                                   transType=params['request_params']['transType'],
                                                   transferInAccount=params['request_params']['transferInAccount'],
                                                   transferOutAccount=params['request_params']['transferOutAccount'],
                                                   quantity=params['request_params']['quantity'])
            pass
        with allure.step('验证：转账申请提交成功'):
            assert transfer['errorCode'] == 0 and transfer['data'].index('数据接收成功') != -1, '转账申请失败'
            pass
        with allure.step('验证：转账申请入库成功'):
            quantity = 77
            sqlStr = f'select transfer_id from t_transfer_data where product_id="{self.symbol}" ' \
                     f'AND amount= {quantity} AND transfer_status=6 order by id desc limit 1'
            db_info = DB_contract_trade.dictCursor(sqlStr=sqlStr)
            assert 'transfer_id' in db_info[0]
        with allure.step('操作: 执行转账审核'):
            transfer_id = db_info[0]['transfer_id']
            SwapServiceMGT.checkTransferRecord(transferId=transfer_id)
            pass
        with allure.step('验证: 存在转账记录且状态为转账成功'):
            sqlStr = 'select  product_id,' \
                             'transfer_status,' \
                             'transfer_in_account,' \
                             'transfer_out_account,' \
                             'actual_transfer_amount,' \
                             'pending_transfer_amount,' \
                             'remark ' \
                     'from t_transfer_record ' \
                     f'where id = {transfer_id}'
            db_info = DB_contract_trade.dictCursor(sqlStr=sqlStr)
            assert db_info, '未获取到数据校验失败'

            assert db_info[0]['product_id'] == self.symbol, '币种数据库校验失败'
            assert db_info[0]['transfer_status'] == '3' or '1', '转账状态数据库校验失败'
            assert db_info[0]['transfer_in_account'] == params['request_params']['transferInAccount'], '转入账号类型，数据库校验失败'
            assert db_info[0]['transfer_out_account'] == params['request_params'][
                'transferOutAccount'], '转出账号类型，数据库校验失败'
            # assert db_info[0]['actual_transfer_amount'] == quantity or 0, '实际转账金额，数据库校验失败'
            assert db_info[0]['pending_transfer_amount'] == quantity, '计划转账金额，数据库校验失败'
            assert db_info[0]['remark'] == 'Automation Test', '转账备注，数据库校验失败'
            pass
