import os
import pytest
import shutil
from config import base_path_concat, log_dir, unique_identifier_for_test_results
from helpers.helpers import setup_loggers, load_xml_files, handle_test_case ,handle_test_case_bulk

work_directory_folder_name = '7_Bulk_Submission'
xml_store_folder_name = 'xml_files_for_7_Bulk Submission'
test_file_name = '7_Bulk_testing_csv_results'

work_directory = os.path.join(base_path_concat, work_directory_folder_name)
print(work_directory)
if not os.path.exists(log_dir):
    print('LOG DIR', log_dir)
    os.makedirs(log_dir)

logger1, logger2 = setup_loggers(log_dir)

xml_file_path = os.path.join(work_directory, xml_store_folder_name)
filename_for_csv_with_results = test_file_name  + unique_identifier_for_test_results
filename_for_csv_with_results_full_path = os.path.join(work_directory, 'test_results', f'{filename_for_csv_with_results}.csv')
base_df_filepath = os.path.join(work_directory, 'df_full.csv')

full_response_text_storage = 'full_response_text_storage'
full_response_text_storage_path = os.path.join(work_directory, full_response_text_storage)
print('FULL PATH FOR TEXT STORAGE')
print(full_response_text_storage_path)
if os.path.exists(full_response_text_storage_path):
    shutil.rmtree(full_response_text_storage_path)
os.makedirs(full_response_text_storage_path, exist_ok=True)
print(filename_for_csv_with_results_full_path)
if os.path.exists(filename_for_csv_with_results_full_path):
    print('REMOVING OLD CSV RESULTS FILE')
    os.remove(filename_for_csv_with_results_full_path)
    print(f"File {filename_for_csv_with_results_full_path} removed %%%.")

json_filepath_folder = os.path.join(work_directory, f'{work_directory_folder_name}_json_results')

xml_files = load_xml_files(xml_file_path)

@pytest.mark.parametrize("xml_file", xml_files)
def test_print_xml_content(xml_file):
    handle_test_case_bulk(
        xml_file,
        xml_file_path,
        base_df_filepath,
        json_filepath_folder,
        work_directory,
        filename_for_csv_with_results,
        full_response_text_storage_path, 
        logger1,
        logger2
    )

