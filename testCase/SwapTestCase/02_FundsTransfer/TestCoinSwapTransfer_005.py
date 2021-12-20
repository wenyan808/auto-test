#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : HuiQing Yu


import random
import time

import allure
import pytest

from common.SwapServiceAPI import user01
from common.redisComm import redisConf
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL


@allure.epic(epic[1])
@allure.feature(features[1]['feature'])
@allure.story(features[1]['story'][2])
@allure.tag('Script owner : 张广南', 'Case owner : 叶永刚')
@pytest.mark.stable
class TestCoinSwapTransfer_005:

    @classmethod
    def setup_class(cls):
        with allure.step("变量初始化"):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.symbol = DEFAULT_SYMBOL
            cls.redisClient = redisConf('redis6380').instance()
            pass
        with allure.step('获取当前母账号与子账号资金信息'):
            cls.f_account = str(cls.redisClient.hmget('RsT:APO:11538483#'+cls.symbol,'Account:#'+cls.symbol)).split(',')[26]
            cls.c_account = str(cls.redisClient.hmget('RsT:APO:11539580#'+cls.symbol,'Account:#'+cls.symbol)).split(',')[26]
            print('母账户初始金额={}，子账户初始金额={}'.format(cls.f_account,cls.c_account))
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass
    @allure.title('母账户划转到子账号')
    def test_execute(self, contract_code):
        with allure.step("操作：执行划转，母 划 子"):
            amount = random.randint(10,800)
            result = user01.swap_master_sub_transfer(sub_uid='115395803',contract_code=self.contract_code,amount=amount,type='master_to_sub')
            pass
        with allure.step("验证：划转成功还回单号"):
            assert 'ok' in result['status'] and result['data']['order_id']
            pass
        with allure.step("操作：获取当前母子账号资金信息"):
            time.sleep(1)  # 等待划转数据更新
            f_current_account = str(self.redisClient.hmget('RsT:APO:11538483#'+self.symbol,'Account:#'+self.symbol)).split(',')[26]
            c_current_account = str(self.redisClient.hmget('RsT:APO:11539580#'+self.symbol,'Account:#'+self.symbol)).split(',')[26]
            print('母账户当前资金={}，子账户当前资金={}'.format(f_current_account, c_current_account))
            pass
        with allure.step("验证：母账号金额更新正确"):
            assert amount == float(self.f_account) - float(f_current_account)
            pass
        with allure.step("验证：子账号金额更新正确"):
            assert amount == float(c_current_account) - float(self.c_account)
            pass
        with allure.step("验证：存在划转记录"):
            flag = False
            for i in range(3):
                record = user01.swap_master_sub_transfer_record(contract_code=self.contract_code, transfer_type='34',
                                                                page_size=1, page_index=1, create_date=1)
                if -amount == record['data']['transfer_record'][0]['amount']:
                    flag = True
                    break
                else:
                    print("验证失败,第{}次重试……".format(i+1))
                    time.sleep(1)
            assert flag, '多次重试，记录金额与实操金额不一致'
            pass



if __name__ == '__main__':
    pytest.main()
