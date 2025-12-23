import math
import json
import os

class LoadData:
    def parse_data_json(json_data):
        accelData = {
            'x': json_data['x'],
            'y': json_data['y'],
            'z': json_data['z'],
            'timestamp': json_data['accel_timestamp']
        }
        HRData = {
            'HR': json_data['heartRate'],
            'timestamp': json_data['heartRate_timestamp']
        }
        absolute_start_time = json_data.get('absoluteStartTime', None)

        print(f"x length: {len(accelData['x'])}")
        print(f"y length: {len(accelData['y'])}")
        print(f"z length: {len(accelData['z'])}")
        print(f"time length: {len(accelData['timestamp'])}")
        print(f"hr length: {len(HRData['HR'])}")
        print(f"hr time length: {len(HRData['timestamp'])}")

        return accelData, HRData, absolute_start_time

    def write_data_to_files(accelData, HRData, file_number, absolute_start_time, docker_root):
        data_dir = os.path.join(docker_root, 'data')

        file_mode = 'a'

        print(f"timestamp: {accelData['timestamp'][0]}")
        # if new data session, reset files
        if accelData['timestamp'][0] < 10:
            file_mode = 'w'

        accel_path = os.path.join(data_dir, 'motion', file_number + '_acceleration.txt')
        with open(accel_path, file_mode) as file:
            for index, i in enumerate(accelData['timestamp']):
                newLine = str(i) + ' ' + str(accelData['x'][index]) + ' ' + str(accelData['y'][index]) + ' ' + str(accelData['z'][index]) + '\n'
                file.write(newLine)

        hr_path = os.path.join(data_dir, 'heart_rate', file_number + '_heartrate.txt')
        with open(hr_path, file_mode) as file:
            for index, i in enumerate(HRData['timestamp']):
                newLine = str(i) + ',' + str(HRData['HR'][index]) + '\n'
                file.write(newLine)

        labels_path = os.path.join(data_dir, 'labels', file_number + '_labeled_sleep.txt')
        with open(labels_path, 'w') as file:
            iteration_amount = math.floor(accelData['timestamp'][-1] / 30) + 1

            for i in range(iteration_amount):
                newLine = str(i * 30) + ' ' + '0' + '\n'
                file.write(newLine)

        start_path = os.path.join(data_dir, 'start_time', file_number + '_start_time.json')
        with open(start_path, 'w') as f:
                json.dump({"startTime": absolute_start_time}, f)

    def write_apple_sleep_data_to_file(sleep_data, file_number, docker_root):
        save_dir = os.path.join(docker_root, 'data', 'apple_sleep')

        sleep_path = os.path.join(save_dir, f"{file_number}_apple_sleep.json")
        with open(sleep_path, 'w') as f:
            json.dump(sleep_data, f, indent=4)

        print(f"Apple sleep data saved to {sleep_path}")