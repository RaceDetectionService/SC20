import flask
from flask import Flask, request, render_template, jsonify
from subprocess import PIPE, run
import requests
import subprocess
import os
import json
import time
from werkzeug import secure_filename
import MetaService 
import threading

UPLOAD_FOLDER = '/tmp/rds'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html', val="")


@app.route("/uploader", methods=['GET', 'POST'])
def uploader():
    if request.method == "POST":
        if 'file' in request.files:
            f = request.files['file']
            if not f:
                print("file is empty")
                return render_template('index.html',
                                       val={"Please insert the file"})
                name = ""
            else:
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                name = filename
        else:
            name = ""
        print(name)
        as_dict = request.form.getlist('racedetection')
        print(as_dict)
        res_archer = ""
        res_inspector = ""
        res_tsan = ""
        res = {}
        if not as_dict:
            print("nothing")
            res_archer = callArcher(name)
            res_inspector = callIntellInspector(name)
            res_tsan = callTsan(name)
            res_romp = callRomp(name)
            res["archer"] = res_archer
            res["intellspector"] = res_inspector
            res["tsan"] = res_tsan
            res["romp"] = res_romp
        else:
            for rd in as_dict:
                if (rd == "archer"):
                    print("archer")
                    res_archer = callArcher(name)
                    print(type(res_archer))
                    res["archer"] = res_archer
                if (rd == "intellspector"):
                    print("intellspector")
                    res_inspector = callIntellInspector(name)
                    res["intellspector"] = res_inspector
                if (rd == "tsan"):
                    print("tsan")
                    res_tsan = callTsan(name)
                    res["tsan"] = res_tsan
                if (rd == "romp"):
                    print("romp")
                    res_romp = callRomp(name)
                    res["romp"] = res_romp
        print(res)
        return render_template('index.html', val=res)


@app.route('/test', methods=['GET', 'POST'])
def test():
    timeRecord = open('metaservice_time.csv', 'a')
    majorityVoteRecord = open('majority_vote.log', 'a')
    weightVoteRecord = open('weight_vote.log', 'a')
    randomVoteRecord = open('random_vote.log', 'a')
    totalStartTime = time.time()
    try:
        os.makedirs(UPLOAD_FOLDER)
    except FileExistsError:
        pass
    name = ""
    if request.method == "POST":
        if 'file' in request.files:
            f = request.files['file']
            if not f:
                print("file is empty")
                name = ""
            else:
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                name = f.filename
        else:
            name = ""

        # Use empty list as parameter to hold the return value
        jsonArcher = []
        jsonIntel = []
        jsonTsan = []
        jsonRomp = []

        # Create multiple threads to send requests
        threadArcher = threading.Thread(target=callArcher, args=(name, jsonArcher))
        threadInspector = threading.Thread(target=callInspector, args=(name, jsonIntel))
        threadTsan = threading.Thread(target=callTsan, args=(name, jsonTsan))
        threadRomp = threading.Thread(target=callRomp, args=(name, jsonRomp))

        microserviceStartTime = time.time()
        # Send all requests withblocking
        threadArcher.start()
        threadInspector.start()
        threadTsan.start()
        threadRomp.start()

        # Wait for all responses
        threadArcher.join()
        threadInspector.join()
        threadTsan.join()
        threadRomp.join()

        # All the JSON responses are received.
        rawResult = [jsonArcher[0].json(), jsonIntel[0].json(), jsonTsan[0].json(), jsonRomp[0].json()]
        for i in range(len(rawResult)):
            if len(rawResult[i]) == 0:
                rawResult[i] = None

        '''
        # Return combined results
        result = {}
        for i in range(4):
            result[str(i)] = rawResult[i]
        jsonResult = json.dumps(result, indent=4)
        return flask.make_response(jsonResult, 200)
        '''

        # Send the JSON dict objects from microservices to the voting function
        votingResult = {}

        majorityVoteStartTime = time.time()
        majorityVoteResult = MetaService.majorityVote(rawResult)
        votingResult['Majority Vote'] = majorityVoteResult

        weightVoteStartTime = time.time()
        weightVoteResult = MetaService.weightVote(rawResult)
        votingResult['Weight Vote'] = weightVoteResult

        randomVoteStartTime = time.time()
        randomVoteResult = MetaService.randomVote(rawResult)
        votingResult['Random Vote'] = randomVoteResult

        votingEndTime = time.time()
        jsonResult = json.dumps(votingResult, indent=4)


        totalEndTime = time.time()
        # Write the time record
        timeRecord.write(name + ',' + str(totalStartTime) + ',' + str(microserviceStartTime) + ',' + str(majorityVoteStartTime) + ',' + str(weightVoteStartTime) + ',' + str(randomVoteStartTime) + ',' + str(votingEndTime) + ',' + str(totalEndTime) + '\n')
        timeRecord.close()

        # Write the majority vote record
        voteRecord = {name: majorityVoteResult}
        majorityVoteRecord.write(json.dumps(voteRecord))
        majorityVoteRecord.write('\n')
        majorityVoteRecord.close()

        # Write the weight vote record
        voteRecord = {name: weightVoteResult}
        weightVoteRecord.write(json.dumps(voteRecord))
        weightVoteRecord.write('\n')
        weightVoteRecord.close()

        # Write the random vote record
        voteRecord = {name: randomVoteResult}
        randomVoteRecord.write(json.dumps(voteRecord))
        randomVoteRecord.write('\n')
        randomVoteRecord.close()

        if request.args.get('type') == 'json':
            return flask.make_response(jsonResult, 200)
        else:
            return render_template('index.html', val=output.split('\n'))


def callArcher(name, result):
    url = 'http://localhost:5011/upload?type=json'
    files = {
        'file': open(os.path.join(app.config['UPLOAD_FOLDER'], name), 'rb')
    }
    result.append(requests.post(url, files=files))
    return result

def callInspector(name, result):
    url = 'http://localhost:5012/upload?type=json'
    files = {
        'file': open(os.path.join(app.config['UPLOAD_FOLDER'], name), 'rb')
    }
    result.append(requests.post(url, files=files))
    return result

def callTsan(name, result):
    url = 'http://localhost:5013/upload?type=json'
    files = {
        'file': open(os.path.join(app.config['UPLOAD_FOLDER'], name), 'rb')
    }
    result.append(requests.post(url, files=files))
    return result

def callRomp(name, result):
    url = 'http://localhost:5014/upload?type=json'
    files = {
        'file': open(os.path.join(app.config['UPLOAD_FOLDER'], name), 'rb')
    }
    result.append(requests.post(url, files=files))
    return result

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
