#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211009
# @Author : HuiQing Yu

import allure
import pytest
import time

from common.SwapServiceAPI import user01 as api_user01
from common.SwapServiceWS import user01 as ws_user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL
from tool.SwapTools import SwapTool


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][0])
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_002:
    ids = ['TestSwapNoti_002','TestSwapNoti_003']
    params = [{'case_name': '订阅深度-150档不合并', 'depth_type': 'step0'},
              {'case_name': '订阅深度-20档不合并', 'depth_type': 'step6'},]
    flag = False
    @classmethod
    def setup_class(cls):
        with allure.step('挂盘'):
            cls.current_price = SwapTool.currentPrice()
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.symbol = DEFAULT_SYMBOL
            api_user01.swap_order(contract_code=cls.contract_code,price=round(cls.current_price*0.5,2),direction='buy')
            api_user01.swap_order(contract_code=cls.contract_code,price=round(cls.current_price*1.5,2),direction='sell')
            pass


    @classmethod
    def teardown_class(cls):
        with allure.step('撤单恢复环境'):
            time.sleep(1)
            api_user01.swap_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self,params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：执行sub请求'):
            subs = {
                "sub": "market.{}.depth.{}".format(self.contract_code, params['depth_type']),
                "id": "id1"
            }
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(3):
                result = ws_user01.swap_sub(subs)
                if 'tick' in result:
                    flag = True
                    break
                time.sleep(1)
                print(f'未返回预期结果，第{i + 1}次重试………………………………')
            assert flag
            pass
        with allure.step('验证：返回结果tick字段不为空'):
            assert result['tick'], '返回结果无tick,校验不通过'
            pass
        with allure.step('验证：返回结果bids买盘字段不为空'):
            assert result['tick']['bids'], '返回结果无买盘,校验不通过'
            pass
        with allure.step('验证：返回结果asks卖盘字段不为空'):
            assert result['tick']['asks'], '返回结果无卖盘,校验不通过'
            pass



if __name__ == '__main__':
    pytest.main()
