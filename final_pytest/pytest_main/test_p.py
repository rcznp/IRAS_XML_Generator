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

# logger1, logger2 = setup_loggers(log_dir)

# xml_file_path = os.path.join(work_directory, xml_store_folder_name)
# filename_for_csv_with_results = test_file_name + unique_identifier_for_test_results


# filename_for_csv_with_results_full_path = os.path.join(work_directory, 'test_results', f'{filename_for_csv_with_results}.csv')
# base_df_filepath = os.path.join(work_directory, 'df_full.csv')

# if os.path.exists(filename_for_csv_with_results_full_path):
#     os.remove(filename_for_csv_with_results_full_path)
#     print(f"File {filename_for_csv_with_results_full_path} removed %%%.")
# print(xml_file_path)