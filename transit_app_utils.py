import pickle
import os
import json

import gzip
import shutil
import csv

parent_dir = os.getcwd()
mta_folder = os.path.join(parent_dir, "mtajan21")



def uncompress_files(file):
    first_dot_pos = file.index(".")
    # print(first_dot_pos)
    # print(type(file))
    os.chdir(mta_folder)
    with gzip.open(file, 'rb') as f_in:
        with open(f"{file[:first_dot_pos+1]}pckl", 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(file)
    
    os.chdir(parent_dir)


def pickle_to_json(files):
    os.chdir(mta_folder)
    
    for file in files:
        first_dot_pos = file.index(".")
        # print(f"{file[:first_dot_pos+1]}")
        with open(file, 'rb') as pickle_file:
            data = pickle.load(pickle_file)

        with open(f'{file[:first_dot_pos+1]}json', 'w') as json_file:
            json.dump(data, json_file)
        os.remove(file)
    
    os.chdir(parent_dir)

def load_excel(mta_metrics):
    csv_file = os.path.join(parent_dir, 'mta_metrics.csv')
    with open(csv_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(mta_metrics)

def read_json_to_excel(json_files):
    mta_metrics = [["SN", "FileName", "OntimeStopCount", "DelayedStopCount", "Total", "PercentageOntime"]]
    print(json_files)
    counter = 1
    for file in json_files:
        print("into", file)
        new_row = []
        stop_without_delay_record = 0
        ontime_stop_count = 0
        delayed_stop_count = 0
        #print(type(json_to_count))
        with open(os.path.join(mta_folder, file), 'r', encoding='utf-8') as new_json_file:
            data = json.load(new_json_file)
        #print(type(data))
        parent_key = 0

        for trip_id , trip_id_value in data.items():
            
            for trip_actual_data_by_rt_trip_id, trip_actual_data_by_rt_trip_id_value in trip_id_value.items():
                if trip_actual_data_by_rt_trip_id == "trip_actual_data_by_rt_trip_id":
                    for stop, stop_data in trip_actual_data_by_rt_trip_id_value.items():
                        for trip in stop_data:
                            if trip.get("actual_arrival_delay") == None:
                                stop_without_delay_record += 1

                            elif -120 <= trip.get("actual_arrival_delay") <= 420:
                                ontime_stop_count += 1
                            
                            else:
                                delayed_stop_count += 1 
                    
        total_in = sum([ontime_stop_count, delayed_stop_count])
        percentage_ontime = ontime_stop_count/total_in
        new_row.extend([counter, file, ontime_stop_count, delayed_stop_count, total_in, percentage_ontime])
        counter += 1
        mta_metrics.append(new_row)
    load_excel(mta_metrics)
        #print(new_row)
    print("Done procsing metrics")
    





# print(os.path.isdir(mta_folder))


