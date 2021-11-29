#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211009
# @Author : HuiQing Yu

from common.SwapServiceWS import user01 as ws_user01
from common.SwapServiceAPI import user01 as api_user01
import pytest, allure, random, time
from config.conf import DEFAULT_CONTRACT_CODE
from common.CommonUtils import currentPrice

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('合约交易接口')  # 这里填功能
@allure.story('市场行情接口')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.link(url='https://docs.huobigroup.com/docs/coin_margined_swap/v1/cn/#a690ab6851',name='文档地址')
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_009:
    ids = ['TestSwapNoti_009']
    params = [{'case_name': '订阅深度图'}]
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step('更新深度'):
            cls.current_price = currentPrice()
            for i in range(10):
                api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.current_price*(1-i*0.01) , 2),
                                      direction='buy')
                api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.current_price*(1+i*0.01) , 2),
                                      direction='sell')
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('撤单'):
            api_user01.swap_cancelall(cls.contract_code)
            pass

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：执行sub订阅'):
            subs = {
                      "sub": "market.{}.depth.percent10".format(self.contract_code),
                      "id": "test_depth_id"
                    }
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(1, 4):
                result = ws_user01.swap_sub(subs)
                if result['tick']['bids'] and result['tick']['asks']:
                    flag = True
                    break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i))
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
