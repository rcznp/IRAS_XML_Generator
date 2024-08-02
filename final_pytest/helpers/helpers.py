import os
import requests
import pytest
import json
import logging

def setup_loggers(log_dir):
    if not os.path.exists(log_dir):
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

    return logger1, logger2
def load_xml_data(xml_file_path, xml_file):
    xml_file_full_path = os.path.join(xml_file_path, xml_file)
    print(xml_file_full_path)
    with open(xml_file_full_path, 'r',encoding='utf-8') as file:
        xml_data = file.read()
    return xml_data

def load_xml_files(xml_file_path):
    xml_files = os.listdir(xml_file_path)
    return xml_files


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

def handle_test_case(xml_file, xml_file_path, base_df_filepath, json_filepath_folder, work_directory, filename_for_csv_with_results, logger1, logger2):
    from handle_df.handle_df import get_expected_json, save_results_to_csv #prevent circular import Error
    temp_xml_name_hold = xml_file.split('_')
    print(temp_xml_name_hold)
    test_case_id = int(temp_xml_name_hold[3])
 
    rule_id = temp_xml_name_hold[0]



    xml_data = load_xml_data(xml_file_path, xml_file)


    url = "https://public-stg.api.gov.sg/uat/gst/einvoicing/v1/submit"
    headers = {'Content-Type': 'application/xml; charset=utf-8','User-Agent': 'IRAS_TEST_AGENT'}


    response = requests.post(url, data=xml_data.encode('utf-8'), headers=headers)

    json_filename = json_filepath_folder + '/' + rule_id + 'testcase_' + str(test_case_id) +'.json'
    

    save_to_json(json_filename,response.text)
    
    assert_result = "Passed"
    expected_json , expected_status= get_expected_json(base_df_filepath,test_case_id)
    
    
    actual_response = json.loads(response.text)
    #no key errors
    if actual_response['success']:#it passed.but passed when expecting fail is still a fail,error not caught
         temp_errors = ['']
         
         actual_status = actual_response['code']

         save_results_to_csv(work_directory,base_df_filepath,filename_for_csv_with_results,test_case_id,temp_errors,actual_status)
         logger1.debug(f'API call passed for test case ID: {test_case_id} with expected status code {expected_status}\n\n')
         try:
             assert (
                int(expected_status) == actual_status
            ), (
                f"Expected status: {expected_status}, Got: {actual_status}\n\n"
                f"Expected response: {expected_json}, Got: {actual_response['errors']}\n"
            )
         except AssertionError as e:
            logger2.error(f'Test case ID: {test_case_id} - Assertion failed: {str(e)}')
            logger2.debug(f'Actual response: {actual_response}')
            logger2.debug(f'Expected status: {expected_status}, Expected response: {expected_json}\n\n')
            logger2.debug('----------------------------------------')
            raise e

    #means can access key errors
    elif not actual_response['success']: #failed,but could mean pass as caught error,or mean fail as supposed to  pass
        temp_errors = []
        temp_errors_string = ''
        actual_status = actual_response['code']
        for errors in actual_response['errors']:#could be
            temp_errors.append(errors['description'])
            temp_errors_string = temp_errors_string + errors['description']
        #now use get_expected_json to 
        print('****+++]]]]]]]]')
        print(temp_errors)
        print('****+++]]]]]]]]')
        save_results_to_csv(work_directory,base_df_filepath,filename_for_csv_with_results,test_case_id,temp_errors,actual_status)
        logger1.debug(f'API call failed for test case ID: {test_case_id} with errors: {temp_errors}\n\n')
        try:
            assert (int(expected_status) == actual_status and expected_json == temp_errors_string), (
                f"Expected status: {expected_status}, Got: {actual_status}\n\n"
                f"Expected response: {expected_json}, Got: {actual_response['errors']}\n"
            )
        except AssertionError as e:
            logger2.error(f'Test case ID: {test_case_id} - Assertion failed: {str(e)}')
            logger2.debug(f'Actual response___(temp_errors_string): {temp_errors_string}')
            logger2.debug(f'Expected status: {expected_status}, Expected response: {expected_json}\n\n')
            logger2.debug('----------------------------------------')
            raise e
def handle_test_case_bulk(xml_file, xml_file_path, base_df_filepath, json_filepath_folder, work_directory, filename_for_csv_with_results, full_response_text_storage, logger1, logger2):
    from handle_df.handle_df import get_expected_json, save_results_to_csv # Prevent circular import error

    test_case_id = int(xml_file.split('_')[0])

    xml_data = load_xml_data(xml_file_path, xml_file)

    url = "https://public-stg.api.gov.sg/uat/gst/einvoicing/v1/bulksubmit"
    headers = {'Content-Type': 'application/xml; charset=utf-8', 'User-Agent': 'IRAS_TEST_AGENT'}

    response = requests.post(url, data=xml_data.encode('utf-8'), headers=headers)

    # Check if full_response_text_storage is a valid path
    if os.path.isdir(full_response_text_storage):
        output_file_path = os.path.join(work_directory, full_response_text_storage, f'test_case_{str(test_case_id)}_text.txt')
        print(output_file_path)

        actual_response = json.loads(response.text)
        with open(output_file_path, 'a', encoding='utf-8') as output_file:
            output_file.write(f"Test Case ID: {test_case_id}\n")
            output_file.write(f"Response: {json.dumps(actual_response, indent=2)}\n")
            output_file.write("\n\n")

        print(f"Response for test case {test_case_id} saved to {output_file_path}")
    else:
        print(f"Skipping response text storage for test case {test_case_id} as {full_response_text_storage} is not a valid directory")

    actual_status = actual_response['code']

    expected_json, expected_status = get_expected_json(base_df_filepath, test_case_id)
    assert actual_status == int(expected_status)
    
    if actual_response['success']:
        temp_errors = ['']
        print('actual_status')
        print(actual_status)
        save_results_to_csv(work_directory, base_df_filepath, filename_for_csv_with_results, test_case_id, temp_errors, actual_status)
    elif not actual_response['success']:
        temp_errors = []
        temp_errors_string = ''
        for errors in actual_response['errors']:
            temp_errors.append(errors['description'])
            temp_errors_string += errors['description']
        print('****+++]]]]]]]]')
        print('temp_errors = >', temp_errors)
        print('****+++]]]]]]]]')
        save_results_to_csv(work_directory, base_df_filepath, filename_for_csv_with_results, test_case_id, temp_errors, actual_status)
