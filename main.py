import os

import glob
from transit_app_utils import pickle_to_json, uncompress_files, read_json_to_excel, load_excel



#file = '20210522.pckl'
compressed_files_folder = 'mtajan19'


class TransitApp:
    def __init__(self, folder_name=None):
        """
            The class is initialized with the folder that has the compressed files
        """
        self.folder_name = folder_name     

    # def _decorator(**args):
    #     def run_job(self):
    #         job1(self)
    #         job2(self)
    #         job3(self)
    #         print("job running done...")
    #     return run_job

    
    def extract_zip_files(self):
        compressed_files = os.listdir(self.folder_name)
        for file in compressed_files:
            #loops through all files in the 
            # #compressed zip folder than call the uncompressed_file function
            uncompress_files(file)

            
        print("listing complete")

    def pickle_to_json(self):
        pickle_files = os.listdir(self.folder_name)
        pickle_to_json(pickle_files)
        print("unpickling complete")
    
    def prepare_metrics(self):
        json_files = os.listdir(self.folder_name)
        read_json_to_excel(json_files)
        print("Done converting")

    
    def run(self):
        print("execution mode started... ")
        # self.extract_zip_files()
        # self.pickle_to_json()
        self.prepare_metrics()


new_work = TransitApp(compressed_files_folder)

# new_work.extract_zip_files()

# new_work.pickle_to_json()

new_work.run()