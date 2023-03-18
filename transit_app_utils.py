import pickle
import os
import json

import gzip
import shutil
import csv

parent_dir = os.getcwd()
mta_folder = os.path.join(parent_dir, "mtajan19")



def uncompress_files(file):
    first_dot_pos = file.index(".")
    """
        The function takes a compressed file eg 20190101.pckl.gz
        searched for the first dt. and slices the file name up to the first dot
        the pickle file will be named thus
        20190101.pckl
    """
    # print(first_dot_pos)
    # print(type(file))
    os.chdir(mta_folder)
    with gzip.open(file, 'rb') as f_in:
        #gzip uncompressed the file\
        # the uncompresed file is a pickle file
        with open(f"{file[:first_dot_pos+1]}pckl", 'wb') as f_out:
            # +1 makes sure that the dot is read then pckl is added as an extension
            # creates a file automatically using the file name, reads the binary then
            # using shutil it copies this binary content to the pickle files an removes the file
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
    mta_metrics = [["SN", "Date", "TripID", "FirstDepartureTime", "NoOfStopsOnTime", "NoOfStopsEarly", "NoOfStopsLate", "AverageDelay"]]
    print(json_files)
    counter = 1
    for file in json_files:
        date = file.split('.')[0]
        print("into", file)
        
        
        new_row = []
        stop_without_delay_record = 0
        ontime_stop_count = 0
        delayed_stop_count = 0
        first_departure_time = 0
        #print(type(json_to_count))
        with open(os.path.join(mta_folder, file), 'r', encoding='utf-8') as new_json_file:
            data = json.load(new_json_file)
        #print(type(data))
        parent_key = 0

        for trip_id , trip_id_value in data.items():
            
            for trip_actual_data_by_rt_trip_id, trip_actual_data_by_rt_trip_id_value in trip_id_value.items():
                if trip_actual_data_by_rt_trip_id == "trip_actual_data_by_rt_trip_id":
                    # print("trip actual", trip_actual_data_by_rt_trip_id)
                    counter_trip_level = 0
                    for trip, stops in trip_actual_data_by_rt_trip_id_value.items():
                        new_row_trip_level = []
                        first_departure_time = stops[0]["departure"]
                        no_of_stops_ontime = 0
                        no_of_stops_early = 0
                        no_stop_late = 0
                        stops_without_delay_trip_level = 0
                        average_delay = 0
                        new_row_trip_level.extend([counter_trip_level, date, trip, first_departure_time])
                        
                        for stop in stops:
                            # print("stopoo", stop.key())
                            if stop.get("actual_arrival_delay") == None:
                                # stop_without_delay_record += 1
                                stops_without_delay_trip_level +=1

                            elif -120 <= stop.get("actual_arrival_delay") <= 420:
                                # ontime_stop_count += 1
                                no_of_stops_ontime +=1
                            elif stop.get("actual_arrival_delay") < -120:
                                no_of_stops_early +=1
                            
                            elif stop.get("actual_arrival_delay") > 420:
                                no_stop_late +=1
                        average_delay = sum([no_of_stops_ontime, no_of_stops_early, no_stop_late])/3
                        new_row_trip_level.extend([no_of_stops_ontime, no_of_stops_early, no_stop_late, average_delay])
                    mta_metrics.append(new_row_trip_level)
                    counter_trip_level +=1
                    
        # total_in = sum([ontime_stop_count, delayed_stop_count])
        # percentage_ontime = ontime_stop_count/total_in
        # new_row.extend([counter, file, ontime_stop_count, delayed_stop_count, total_in, percentage_ontime])
        # counter += 1
        # mta_metrics.append(new_row)
        
    load_excel(mta_metrics)
        #print(new_row)
    print("Done procsing metrics")
    





# print(os.path.isdir(mta_folder))


