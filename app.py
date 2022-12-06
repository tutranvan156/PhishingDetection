from flask import Flask, jsonify, request, render_template
from urllib.request import Request, urlopen
import sys
sys.path.insert(1, '/home/vantu/PTIT/Code/extension/core')
import core_process

app = Flask(__name__)
#
@app.route('/get-url', methods = ['POST'])
def get_url():
        url = request.form['url']
        print("Your url is: " + url)
        #0 is phishing 
        #1 is legitimate
        sanity_check = core_process.cnn_lstm(url)
        #If result is equal -1 meain cnn_lstm model not sure about prediction 
        if sanity_check == -1:
                return str(core_process.machine_learning(url))
        else:
                return str(sanity_check)

app.run(host='0.0.0.0', port=5000)