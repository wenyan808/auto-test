#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211012
# @Author : 张广南
    用例标题
        WS订阅深度 合约代码为空
    前置条件
        
    步骤/文本
        参考官方文档
    预期结果
        订阅失败
    优先级
        3
    用例别名
        TestContractNoti_depth_039
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceWS import t as contract_service_ws

from pprint import pprint
import pytest, allure, random, time

from tool import atp

@allure.epic('反向交割')  # 这里填业务线
@allure.feature('行情')  # 这里填功能
@allure.story('深度')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 张广南', 'Case owner : 吉龙')
class TestContractNoti_depth_039:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol_period):
        print("\n清盘》》》》", atp.ATP.clean_market())
        contract_types = {'CW': "this_week", 'NW': "next_week", 'CQ': "quarter", 'NQ': "next_quarter"}
        symbol = symbol_period.split('_')[0]
        contract_type = contract_types[symbol_period.split('_')[1]]
        lever_rate = 5

        # 获取交割合约当前价格

        contractInfo = contract_api.contract_contract_info(symbol=symbol, contract_type=contract_type)
        print('BTC当周合约信息 = ', contractInfo)

        # 等待深度信息更新
        time.sleep(3)

    @allure.title('WS订阅深度 合约代码为空')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('参考官方文档'):
            depth_type = 'step6'
            subs = {
                "sub": "market.{}.depth.{}".format(' ', depth_type),
                "id": "id5"
            }
            result = contract_service_ws.contract_sub(subs)
            result_str = '\nDepth返回结果 = ' + str(result)
            print('\033[1;32;49m%s\033[0m' % result_str)
            assert result['err-code'] == 'bad-request'

    @allure.step('恢复环境')
    def teardown(self):
        atp.ATP.cancel_all_types_order()
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
