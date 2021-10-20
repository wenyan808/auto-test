#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211015
# @Author : 
    用例标题
        restful请求K线15min 传参size
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        
    优先级
        0
    用例别名
        TestSwapNoti_restful_kline_020
"""

from common.SwapServiceAPI import t as swap_api
import pytest, allure, random, time


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('restful请求K线')  # 这里填功能
@allure.story('restful请求K线15min 选填参数验证：只传参size')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_restful_kline_020:

    @allure.step('前置条件')
    def setup(self):
        print("\n自动化步骤："
              "\n*、发送restful请求kline的请求,类型=15min；"
              "\n*、选填参数是否传参：from【N】 ,to【N】 , size【Y】"
              "\n*、验证Kline返回结果："
              "\n\t返回topic正确，data内所有字段校验，不存在空的情况"
              "\n\tdata内所有数据时间连续")

    @allure.title('restful请求K线15min 传参size')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('详见官方文档'):
            period = '15min'
            size = 60 * 24
            kLineInfo = swap_api.swap_kline(contract_code=contract_code, period=period, size=size)
            assert 'market.' + contract_code + '.kline.15min' in kLineInfo['ch']
            if 'data' in kLineInfo:
                assert len(kLineInfo['data']) <= size
                n = 0
                while n< len(kLineInfo['data']):
                    assert kLineInfo['data'][n]['open'] > 0
                    assert kLineInfo['data'][n]['close'] > 0
                    assert kLineInfo['data'][n]['low'] > 0
                    assert kLineInfo['data'][n]['high'] > 0
                    assert kLineInfo['data'][n]['amount'] >= 0
                    assert kLineInfo['data'][n]['vol'] >= 0
                    assert kLineInfo['data'][n]['count'] >= 0
                    # 断言24小时k线的连续
                    if n != len(kLineInfo['data']) - 1:
                        assert kLineInfo['data'][n]['id'] + 60*15 == kLineInfo['data'][n+1]['id']
                    n = n + 1
            else:
                assert False #无data返回直接失败
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
