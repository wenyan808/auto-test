#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/11 2:01 下午
# @Author  : HuiQing Yu

import allure
import pytest
import time
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE
from common.SwapServiceWS import user01 as ws_user01



@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.P0
class TestSwapExIndex_estimatedrate_001:

    contract_code = DEFAULT_CONTRACT_CODE
    def test_execute(self):
        with allure.step('操作：执行req请求'):


            pass
