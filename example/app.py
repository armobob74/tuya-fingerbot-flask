from flask import Flask, render_template, request, redirect, url_for
import json
import time
import logging
from tuya_connector import TuyaOpenAPI, TUYA_LOGGER
 
app = Flask(__name__)
 
ACCESS_ID = "qptp3ufv9gpuu9ehpfre"
ACCESS_KEY = "43af19c2ff1f4762a725909adc84edaf"
API_ENDPOINT = "https://openapi.tuyaus.com"
 
# Enable debug log
TUYA_LOGGER.setLevel(logging.DEBUG)
 
# Init OpenAPI and connect
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()
 
# Set up device_id
DEVICE_ID = "eb0e50utng8gvk7o"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pman/control', methods=['POST'])
def pmanControl():
    """
    Meant to be called by the Unified UI, or any PMAN runner.
    args format: [delay_time]
    Presses button, waits for delay_time sec, and presses button again.
    """
    d = json.loads(request.data)
    args = d['args']
    delay_time = args[0]
    commands = {'commands': [{'code': 'switch', 'value': False}]}

    openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICE_ID), commands)
    time.sleep(delay_time)
    openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICE_ID), commands)
    return {'status':'No Error', 'message':'Done'}

@app.route('/pman/single-press', methods=['POST'])
def pmanSinglePress():
    """
    Meant to be called by the Unified UI, or any PMAN runner.
    Presses button once
    """
    commands = {'commands': [{'code': 'switch', 'value': True}]}
    openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICE_ID), commands)
    return {'status':'No Error', 'message':'Done'}
 
@app.route('/control', methods=['POST'])
def control():
    delay_time = float(request.form['delay_time'])
   
    commands = {'commands': [{'code': 'switch', 'value': False}]}
   
    # Send commands
    openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICE_ID), commands)
   
    # Get the status of a single device
    response = openapi.get("/v1.0/iot-03/devices/{}/status".format(DEVICE_ID))
 
    time.sleep(delay_time)
 
    openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICE_ID), commands)
 
    # Get the status of a single device
    response = openapi.get("/v1.0/iot-03/devices/{}/status".format(DEVICE_ID))
 
    return redirect(url_for('index'))
 
@app.route('/single_press', methods=['POST'])
def single_press():
    # Execute lines of code specific to the "Single Press" button
    # For example, you can add your own logic here
    commands = {'commands': [{'code': 'switch', 'value': True}]}
    # Replace the following lines with your actual code
    # print("Executing code for Single Press")
    # Your code here
    openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICE_ID), commands)
    # Get the status of a single device
    response = openapi.get("/v1.0/iot-03/devices/{}/status".format(DEVICE_ID))
 
    return redirect(url_for('index'))
 
if __name__ == "__main__":
    app.run(debug=True, port=5800)
 
