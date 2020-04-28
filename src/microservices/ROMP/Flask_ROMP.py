from flask import Flask, request, render_template, redirect, Response, jsonify
from subprocess import PIPE, run
import flask
import subprocess
import os
import json
from werkzeug import secure_filename
import time

UPLOAD_FOLDER = '/tmp/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def api_root():
    return render_template('index.html', val="")


# benchmark API for archer
@app.route('/benchmark', methods=['POST'])
def benchmark():
    print("request received")
    # Running first command
    cmd = "sh /home/rds/dataracebench/check-data-races.sh"
    tstart = time.time()
    result = run(cmd.split(),
                 stdout=PIPE,
                 stderr=subprocess.STDOUT,
                 universal_newlines=True)
    tend = time.time()
    benchmarkTime = tend - tstart
    print(benchmarkTime)
    if (result.returncode == 1):
        str = result.stderr
    else:
        str = result.stdout
    print(str)

    with open(os.path.join(app.config['UPLOAD_FOLDER'], "rompbenchmark.txt"),
              "w") as rompfile:
        print("Benchmark time: ", benchmarkTime, file=rompfile)
    return flask.make_response(flask.jsonify({'romp': json.loads(str)}), 200)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    name = ""
    if request.method == "POST":
        if 'file' in request.files:
            f = request.files['file']
            if not f:
                print("file is empty")
                name = ""
            else:
                # f.save(secure_filename(f.filename))
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                name = filename
        else:
            name = ""
        print(name)
        # cmd_list = [
        #     "pwd", "ls -l " + os.path.join(app.config['UPLOAD_FOLDER'], name)
        # ]
        cmd_list = [
            "gcc -g -fopenmp -lomp " +
            os.path.join(app.config['UPLOAD_FOLDER'], name) + " -o " +
            os.path.join(app.config['UPLOAD_FOLDER'], "myApp"),
            "InstrumentMain --program=" +
            os.path.join(app.config['UPLOAD_FOLDER'], "myApp"),
            os.path.join(app.config['UPLOAD_FOLDER'], "myApp.inst")
        ]
        for cmd in cmd_list:
            arr = cmd.split()
            with open(
                    os.path.join(app.config['UPLOAD_FOLDER'],
                                 "rompoutput.txt"), "w") as file:
                run(arr, stdout=file, stderr=file, universal_newlines=True)

        res_path = "python3 RompOutputParser.py " + os.path.join(
            app.config['UPLOAD_FOLDER'], "rompoutput.txt")
        result = run(res_path.split(),
                     stdout=PIPE,
                     stderr=subprocess.STDOUT,
                     universal_newlines=True)
        if (result.returncode == 1):
            str = result.stderr
        else:
            str = result.stdout
        print(str)
        # str = '{"0": {"Memory Address": "0x7fff13f3bb10", "Write_thread": "thread T3", "file loaction": "/home/yshi10/datarace/RaceDetectionService/tools_output/dataRaceTest1", "write file name": "DRB001-antidep1-orig-yes.c", "write line #": "64", "write symbol position": "9", "Read_thread": "thread T2", "read file name": "DRB001-antidep1-orig-yes.c", "read line #": "64", "read symbol position": "10", "tool": "archer"}, "1": {"Memory Address": "0x7fff13f3b4d0", "Write_thread": "thread T1", "file loaction": "/home/yshi10/datarace/RaceDetectionService/tools_output/dataRaceTest1", "write file name": "DRB001-antidep1-orig-yes.c", "write line #": "64", "write symbol position": "9", "Read_thread": "main thread", "read file name": "DRB001-antidep1-orig-yes.c", "read line #": "64", "read symbol position": "10", "tool": "archer"}}'
        if not str:
            str = '{}'
        if request.args.get('type') == 'json':
            return flask.make_response(
                flask.jsonify({'romp': json.loads(str)}), 200)
        else:
            return render_template('index.html', val=str.split('\n'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
