import os
import requests
import pytest
from handle_df.handle_df import get_expected_json
from handle_df.handle_df import save_results_to_csv
import json
import logging
import shutil
from config import base_path_concat
from config import log_dir

work_directory = os.path.join(base_path_concat,'7_Bulk_Submission')
print(work_directory)
if not os.path.exists(log_dir):
    print('LOG DIR',log_dir)
    os.makedirs(log_dir)

logger1 = logging.getLogger('general_logger')
logger1.setLevel(logging.DEBUG)
general_handler = logging.FileHandler(f'{log_dir}/general.log')
general_handler.setLevel(logging.DEBUG)
general_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
general_handler.setFormatter(general_formatter)
logger1.addHandler(general_handler)


logger2 = logging.getLogger('error_logger')
logger2.setLevel(logging.DEBUG)
specific_handler = logging.FileHandler(f'{log_dir}/error.log')
specific_handler.setLevel(logging.DEBUG)
specific_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
specific_handler.setFormatter(specific_formatter)
logger2.addHandler(specific_handler)

def save_to_json(filepath,json_string):
     try:
        # Convert the JSON string to a JSON object
        json_object = json.loads(json_string)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        # Save the JSON object to a file
        with open(filepath, 'w') as json_file:
            json.dump(json_object, json_file, indent=4)  # indent=4 for pretty printing
            print(f"JSON data has been written to {filepath}")
     except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
     except Exception as e:
            print(f"An error occurred: {e}")
# '/Users/cheongray/iras_api_make_xml/input_val_comments_subset'


xml_file_path = work_directory + "/xml_files_for_7_Bulk Submission"
filename_for_csv_with_results = '7_Bulk_testing_csv_results'
filename_for_csv_with_results_full_path  = work_directory + '/test_results/'+ filename_for_csv_with_results + '.csv'
base_df_filepath = work_directory + '/df_full.csv'

full_response_text_storage = 'full_response_text_storage'
full_response_text_storage_path = os.path.join(work_directory, full_response_text_storage)
print('FULL PATH FOR TEXT STORAGE')
print(full_response_text_storage_path)
if os.path.exists(full_response_text_storage_path):
        shutil.rmtree(full_response_text_storage_path)
os.makedirs(full_response_text_storage_path, exist_ok=True)
print(filename_for_csv_with_results_full_path)
if os.path.exists(filename_for_csv_with_results_full_path ):
    print('REMOVING OLD CSV RESULTS FILE')
    os.remove(filename_for_csv_with_results_full_path )
    print(f"File {filename_for_csv_with_results_full_path } removed %%%.")



json_filepath_folder  = work_directory + '/input_val_json_results'


def load_xml_data(xml_file_path, xml_file):
    xml_file_full_path = os.path.join(xml_file_path, xml_file)
    print(xml_file_full_path)
    with open(xml_file_full_path, 'r',encoding='utf-8') as file:
        xml_data = file.read()
    return xml_data

def load_xml_files(xml_file_path):
    xml_files = os.listdir(xml_file_path)
    return xml_files

xml_files = load_xml_files(xml_file_path)

def load_xml_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


xml_folder_path = xml_file_path

# Get a list of all XML files in the folder
xml_files = [f for f in os.listdir(xml_folder_path) if f.endswith('.xml')]

@pytest.mark.parametrize("xml_file", xml_files)
def test_print_xml_content(xml_file):
    print('filepath')
    print(xml_file)
    xml_file_path = os.path.join(xml_folder_path, xml_file)
    test_case_id = int(xml_file.split('_')[0])
    # Load XML data
    xml_data = load_xml_data(xml_file_path)
    

    url = "https://public-stg.api.gov.sg/uat/gst/einvoicing/v1/bulksubmit"
    headers = {'Content-Type': 'application/xml; charset=utf-8','User-Agent': 'IRAS_TEST_AGENT'}


    response = requests.post(url, data=xml_data.encode('utf-8'), headers=headers)

    output_file_path = work_directory + '/'+ full_response_text_storage + '/' + f'test_case_{str(test_case_id)}' + '_text' +'.txt'
    print(output_file_path)

    
    actual_response = json.loads(response.text)
    with open(output_file_path, 'a', encoding='utf-8') as output_file:
        output_file.write(f"Test Case ID: {test_case_id}\n")
        output_file.write(f"Response: {json.dumps(actual_response, indent=2)}\n")
        output_file.write("\n\n")
    
    print(f"Response for test case {test_case_id} saved to {output_file_path}")
    actual_status = actual_response['code']

    expected_json , expected_status = get_expected_json(base_df_filepath,test_case_id)
    assert actual_status == int(expected_status)
    if actual_response['success']:
         temp_errors = ['']
         print('actual_status')
         print(actual_status)
         save_results_to_csv(work_directory,base_df_filepath,filename_for_csv_with_results,test_case_id,temp_errors,actual_status)
    elif not actual_response['success']:
         temp_errors = []
         temp_errors_string = ''
         for errors in actual_response['errors']:#could be
            temp_errors.append(errors['description'])
            temp_errors_string = temp_errors_string + errors['description']
            print('****+++]]]]]]]]')
            print('temp_errors = >',temp_errors)
            print('****+++]]]]]]]]')
            save_results_to_csv(work_directory,base_df_filepath,filename_for_csv_with_results,test_case_id,temp_errors,actual_status)







   