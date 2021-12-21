#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211013
# @Author : HuiQing Yu

from common.SwapServiceWS import user01 as ws_user01
import pytest, allure, random, time
from config.case_content import epic, features
from tool.SwapTools import SwapTool


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][6])
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_023:

    ids = ['TestSwapNoti_ws_kline_023',
           'TestSwapNoti_ws_kline_029',
           'TestSwapNoti_ws_kline_035',
           'TestSwapNoti_ws_kline_041',
           'TestSwapNoti_ws_kline_047',
           'TestSwapNoti_ws_kline_053',
           'TestSwapNoti_ws_kline_059',
           'TestSwapNoti_ws_kline_065',
           'TestSwapNoti_ws_kline_071']
    params = [
              {
                "case_name": "合约停牌-1min",
                "period": "1min"
              },
              {
                "case_name": "合约停牌-5min",
                "period": "5min"
              },
              {
                "case_name": "合约停牌-15min",
                "period": "15min"
              },
              {
                "case_name": "合约停牌-30min",
                "period": "30min"
              },
              {
                "case_name": "合约停牌-60min",
                "period": "60min"
              },
              {
                "case_name": "合约停牌-4hour",
                "period": "4hour"
              },
              {
                "case_name": "合约停牌-1day",
                "period": "1day"
              },
              {
                "case_name": "合约停牌-1week",
                "period": "1week"
              },
              {
                "case_name": "合约停牌-1mon",
                "period": "1mon"
              }
            ]
    contract_info = SwapTool.getContractStatus(init_status=3)

    @pytest.mark.parametrize('param', params, ids=ids)
    @pytest.mark.skipif(condition=contract_info['isSkip'], reason='无停牌合约暂时跳过用例')
    def test_execute(self, param):
        allure.dynamic.title(param['case_name'])
        with allure.step('操作：执行sub请求'):
            self.contract_code = self.contract_info['instrument_index_code']
            subs = {
                "sub": "market.{}.kline.{}".format(self.contract_code, param['period']),
                "id": "id1"
            }
            result = ws_user01.swap_sub(subs=subs)
            pass
        with allure.step('校验返回结果'):
            # 请求topic校验
            assert result['ch'] == "market." + self.contract_code + ".kline." + param['period']
            # 开仓价校验，不为空
            assert result['tick']['open']
            # 收仓价校验
            assert result['tick']['close']
            # 最低价校验,不为空
            assert result['tick']['low']
            # 最高价校验,不为空
            assert result['tick']['high']
            # 币的成交量
            assert result['tick']['amount'] >= 0
            # 成交量张数。 值是买卖双边之和
            assert result['tick']['vol'] >= 0
            # 成交笔数。 值是买卖双边之和
            assert result['tick']['count'] >= 0
            pass



if __name__ == '__main__':
    pytest.main()
