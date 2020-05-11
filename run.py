# !-- encode=utf-8 --!
# author wangx
# email: wangx_0102@126.com
# date: 2020/05/10
from App import app
import os
from flask import request

'''
判题 
'''


@app.route('/judge')
def judge():
    src = request.args.get("src")
    time_limit = request.args.get("time")
    mem_limit = request.args.get("mem")
    dist = request.args.get("dist")
    sudo_password = '818923'
    command = f'./Core -c {src} -t {time_limit} -m {mem_limit}  -d {dist}'
    app.logger.info("running the command: %s", command)
    os.system('echo %s|sudo -S %s' % (sudo_password, command))
    with open(f"{dist}/result.txt", "r") as f:
        line = f.readline().strip()
        time_cost = f.readline().strip()
        mem_cost = f.readline().strip()
    data = {
        "result": line,
        "time": time_cost,
        "memory": mem_cost
    }
    return data


if __name__ == "__main__":
    app.run(host="0.0.0.0")
