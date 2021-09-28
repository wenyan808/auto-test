import json
import os
import pathlib
import shutil
from string import Template


class DingDingMsg:
    ding_ding_msg = '''{
        "msgtype": "text",
        "text": {
        "content": "env: '${env}' system_type: '${system_type}' test_type: '${test_type}' \\ntotal: ${total} passed: ${passed}  \\nfailed: ${failed}  error: ${error} skipped: ${skipped}  \\nrun_time: ${run_time} \\nreport url: \\nhttp://172.18.6.183:8080/jenkins/view/autotest(%E8%87%AA%E5%8A%A8%E5%8C%96%E6%B5%8B%E8%AF%95)/job/auto-test/${build_num}/allure/"
        }}'''

    @classmethod
    def init(cls,):
        path = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
        path = path.parent / 'report/allure/'
        if not path.exists():
            path.mkdir()
        else:
            shutil.rmtree(path)
            path.mkdir()

    @classmethod
    def update_json_file(cls, **kwargs):
        cls.ding_ding_msg = Template(cls.ding_ding_msg).safe_substitute(**kwargs, **cls.get_run_result())
        with open('report/dingding.json', 'w') as dingding_json_f:
            dingding_json_f.write(cls.ding_ding_msg)

    @classmethod
    def get_run_result(cls, ):
        path = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
        path = path.parent / 'report/allure/'
        if not path.exists():
            path.mkdir()
        total = 0
        failed = 0
        error = 0
        passed = 0
        skipped = 0
        for file in os.listdir(path):
            if file.endswith('-result.json'):
                total += 1
                with open(path / file) as result_json_file:
                    result_info = result_json_file.read()
                    if '"status": "failed"' in result_info:
                        failed += 1
                    elif '"status": "broken"' in result_info:
                        error += 1
                    elif '"status": "passed"' in result_info:
                        passed += 1
                    elif '"status": "skipped"' in result_info:
                        skipped += 1

        return {'passed': passed, 'failed': failed, 'error': error, 'skipped': skipped, 'total': total}


if __name__ == '__main__':
    print(DingDingMsg.get_run_result())
