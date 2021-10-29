import json

import requests


class GlobalData:
    ATPHost = 'http://172.18.6.52:8000'
    # ATPHost = 'http://172.18.169.20:8000'
    # ATPHost = 'http://0.0.0.0:8000'
    header = {'accept': 'application/json', 'Content-Type': 'application/json'}

    @classmethod
    def get_global_data(cls, env=None, system_type=None):
        atp_url = cls.ATPHost + "/global_data/get_all_global_data_by_env_and_system_type"
        params = {"env": env,
                  "system_type": system_type}
        response = requests.get(atp_url, headers=cls.header, params=params)
        return response.json()


if __name__ == '__main__':
    print(GlobalData.get_global_data())
    print(GlobalData.get_global_data(env='Test6'))
    print(GlobalData.get_global_data(env='Test20', system_type='LinearSwap'))
