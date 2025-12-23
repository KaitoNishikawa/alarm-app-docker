import os
import sys
from datetime import datetime
from flask import Flask, jsonify, request

current_dir = os.path.dirname(os.path.abspath(__file__))
docker_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, docker_root)

from data_processing.load_data import LoadData

# file_number = datetime.now().strftime("%Y%m%d")
file_number = "20241222"
print(f"date: {file_number}")
app = Flask(__name__)

@app.route('/hello')
def hello_world():
    # runner.run_preprocessing(["20251213", "20251214", "20251215", "20251217"])
    return jsonify(message='Hello World')

@app.route('/data', methods=["POST"])
def receive():
    if request.is_json:
        json_data = request.get_json()

        accelData, HRData, absolute_start_time = LoadData.parse_data_json(json_data)

        LoadData.write_data_to_files(accelData, HRData, file_number, absolute_start_time, docker_root)
        
        return jsonify(message="Data received and saved successfully"), 200
    else:
        return jsonify(message="Request was not JSON"), 400
    
@app.route('/sleep_data', methods=["POST"])
def receive_sleep_data():
    if request.is_json:
        sleep_data = request.get_json()
        
        LoadData.write_apple_sleep_data_to_file(sleep_data, file_number, docker_root)            
        
        return jsonify(message="Sleep data saved successfully"), 200            
    else:
        return jsonify(message="Request was not JSON"), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)