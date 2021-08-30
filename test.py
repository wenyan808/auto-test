from common.ContractServiceOrder import t
from common.LinearServiceOrder import t as lsot
from common.SwapServiceOrder import t

# pprint(t.contract_account_info(symbol='btc'))

# print(t.contract_contract_info(symbol='btc',contract_code='',contract_type='this_week'))


# print(lsot.linear_contract_info(contract_code='btc-usdt'))
# print(lsot.linear_account_info(contract_code='btc-usdt'))


# pprint(ct.contract_account_info(symbol='btc'))
# pprint(ct.contract_contract_info(symbol='btc'))


print(t.swap_contract_info(contract_code='btc-usd'))
print(t.swap_account_info(contract_code='btc-usd'))