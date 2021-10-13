#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/31
# @Author  : zhangranghan

import pytest
from common.SwapServiceAPI import t as st
from config import conf


@pytest.fixture()
def sub_uid():
    sub_uid_list = st.swap_sub_account_list()
    sub_uid = sub_uid_list['data'][0]['sub_uid']
    return sub_uid


@pytest.fixture()
def contract_code():
    contract_code = conf.DEFAULT_CONTRACT_CODE
    return contract_code
