# !-- encode=utf-8 --!
# author wangx
# email: wangx_0102@126.com
# date: 2020/05/10
from App import app
import os
from flask import request

error = {
    "code": 5000,
    "msg": ""
}


def clean_files(dist):
    os.system(f"rm -rf {dist}")


'''
judge problem
'''


@app.route('/judge')
def judge():
    # The source file position
    src = request.args.get("src")
    # The task max running time
    time_limit = request.args.get("time")
    # The task max using memory
    mem_limit = request.args.get("mem")
    # The result file is stored position
    dist = request.args.get("dist")
    # Is using special judge 1 stand for using and 0 stand for not using
    spj_state = request.args.get("spj")
    # Language for spj 1 is c language and 2 is c++ language
    spj_lang = request.args.get("spjLang")
    # The  sudo password, if you are root ignoring it.
    sudo_password = '818923'
    command = './Core'
    # Add running args
    if src != "":
        command.join(f" -c {src}")
    elif time_limit != "":
        command.join(f" -t {time_limit}")
    elif mem_limit != "":
        command.join(f" -m {mem_limit}")
    elif dist != "":
        command.join(f" -d {dist}")
    elif spj_state == "1":
        command.join(f" -s")
        if spj_lang != "":
            command.join(f" -S {spj_lang}")

    app.logger.info("running the command: %s", command)
    # Running the command
    os.system('echo %s|sudo -S %s' % (sudo_password, command))
    # Read the result
    with open(f"{dist}/result.txt", "r") as f:
        line = f.readline().strip()
        time_cost = f.readline().strip()
        mem_cost = f.readline().strip()
        f.close()
    # The result dic
    data = {
        "result": line,
        "time": time_cost,
        "memory": mem_cost
    }
    # Complete and clean temp files
    clean_files(dist)
    return data


@app.route('/src', methods='POST')
def get_src():
    dist = request.form['dist']
    src = request.form['src']
    lang = request.form['lang']
    if lang == "1":
        file_name = "main.c"
    elif lang == "2":
        file_name = "main.cpp"
    elif lang == "3":
        file_name = "Main.java"
    else:
        error['msg'] = "error language option"
        return error
    with open(dist + file_name, "w", encoding="utf-8") as f:
        f.write(src)
        f.close()


@app.route("spj", methods=['POST'])
def get_spj():
    dist = request.form['dist']
    spj_src = request.form['spj']
    spj_lang = request.form['lang']
    if spj_lang == "1":
        file_name = "main.c"
    elif spj_lang == "2":
        file_name = "main.cpp"
    else:
        error['msg'] = "error language option"
        return error
    with open(dist + file_name, "w", encoding="utf-8") as f:
        f.write(spj_src)
        f.close()
    os.system(f"g++ {dist + file_name} -o SpecialJudge -O2")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
