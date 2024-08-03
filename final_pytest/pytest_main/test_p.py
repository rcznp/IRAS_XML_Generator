import os
import pytest
from config import base_path_concat, log_dir, unique_identifier_for_test_results
from helpers.helpers import setup_loggers,load_xml_files, handle_test_case

work_directory_folder_name = '4_Format_Validation'
xml_store_folder_name = 'xml_files_for_4_Format Validation'
test_file_name = '4_Format_testing_csv_results'

work_directory = os.path.join(base_path_concat,work_directory_folder_name)
print('work_directory', work_directory)
if os.path.exists(work_directory):
    print('lol')
