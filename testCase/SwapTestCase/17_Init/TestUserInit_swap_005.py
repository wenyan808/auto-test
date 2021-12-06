#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/6 9:57 上午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from common.SwapServiceAPI import user01, user02
from common.CommonUtils import currentPrice
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL
from config.case_content import epic, features
from common.SwapMqComm import mqComm


@allure.epic(epic[1])
@allure.feature(features[16]['feature'])
@allure.story(features[16]['story'][0])
@allure.tag('Script owner : 余辉青', 'Case owner : 曾超群')
@pytest.mark.stable
class TestUserInit_swap_005:
    ids = ['TestUserInit_swap_005']
    params = [{'case_name': '检查用户已开户，有资金持空仓，个人初始化'}]

    @classmethod
    def setup_class(cls):
        with allure.step('变量初始化'):
            cls.symbol = DEFAULT_SYMBOL
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.latest_price = currentPrice()
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params, redis6380):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：查看用户是否有仓位'):
            name = f'RsT:APO:11538483#{self.symbol}'
            key = f'Position:#{self.symbol}#{self.contract_code}#'
            position_info_1 = int(float(str(redis6380.hmget(name=name, keys=key + '1')).split(',')[5]))
            position_info_2 = int(float(str(redis6380.hmget(name=name, keys=key + '2')).split(',')[5]))
            pass
        with allure.step('操作：仓位调整(有空仓则跳过,无则持多仓；有多仓则清仓，无则跳过)'):
            if position_info_1 > 0:
                print(f'当前用户持有多仓数量{position_info_1},开始进行清仓……')
                user01.swap_order(contract_code=self.contract_code, price=self.latest_price,
                                  volume=position_info_1,
                                  offset='close', direction='sell')
                user02.swap_order(contract_code=self.contract_code, price=self.latest_price,
                                  volume=position_info_1,
                                  offset='open', direction='buy')
            elif position_info_2 == 0:
                print(f'当前用户持有空数量{position_info_1},开始进行持仓……')
                user01.swap_order(contract_code=self.contract_code, price=self.latest_price,
                                  volume=1,
                                  offset='open', direction='sell')
                user02.swap_order(contract_code=self.contract_code, price=self.latest_price,
                                  volume=1,
                                  offset='open', direction='buy')
            pass
        with allure.step(f'操作：删除Redis Key={name}'):
            time.sleep(1)  # 等待清仓完成
            redis6380.delete(name)
            pass
        with allure.step('操作：发送MQ信息'):
            mq_result = mqComm.UserProductTriggerInitChannel(userId='11538483',symbol=self.symbol)
            if mq_result and mq_result['routed']:
                print('MQ信息发送成功……')
            else:
                assert False,'MQ发送失败……'
            pass
        with allure.step(f'验证：Redis Key={name}初始化成功'):
            time.sleep(1)  # 等待初始化完成
            keys = [f'Position:#{self.symbol}#{self.contract_code}#1',  # 多仓key
                    f'Position:#{self.symbol}#{self.contract_code}#2',  # 空仓key
                    f'orderPositionFrozen:{self.contract_code}#1',
                    f'orderPositionFrozen:{self.contract_code}#2',
                    f'clearUnPositionFrozen:{self.contract_code}#1',
                    f'clearUnPositionFrozen:{self.contract_code}#2',
                    f'Account:#{self.symbol}',
                    'orderFrozenMargin',
                    'clearUnFrozenMargin',
            ]
            for key in keys:
                result = redis6380.hmget(name=name, keys=key)
                assert result[0] is not None,key+'校验失败'
            pass


