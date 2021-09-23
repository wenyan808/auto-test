from string import Template


class DingDingMsg:
    ding_ding_msg = '''{
        "msgtype": "text",
        "text": {
        "content": "env: '${env}' system_type: '${system_type}' test_type: '${test_type}' \\ntotal: ${total} passed: ${passed}  \\nfailed: ${failed}  error: ${error} skipped: ${skipped}  \\nrun_time: ${run_time} \\nreport url: \\nhttp://172.18.6.183:8080/jenkins/view/autotest(%E8%87%AA%E5%8A%A8%E5%8C%96%E6%B5%8B%E8%AF%95)/job/auto-test/${build_num}/allure/"
        }}'''

    @classmethod
    def init_result(cls, **kwargs):
        with open('report/dingding.json', 'w') as dingding_json_f:
            msg = Template(cls.ding_ding_msg).safe_substitute(**kwargs)
            dingding_json_f.write(msg)

    @classmethod
    def update_result(cls, **kwargs):
        with open('report/dingding.json', 'r') as dingding_json_f:
            msg = dingding_json_f.read()
            with open('report/dingding.json', 'w') as dingding_json_f:
                dingding_json_f.write(Template(msg).safe_substitute(**kwargs))

    @classmethod
    def update_json_file(cls, build_num):
        with open('report/dingding.json', 'r') as dingding_json_f:
            msg = dingding_json_f.read()
            with open('report/dingding.json', 'w') as dingding_json_f:
                dingding_json_f.write(Template(msg).safe_substitute(build_num=build_num))
