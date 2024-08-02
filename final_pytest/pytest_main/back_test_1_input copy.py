#back up
import os
import requests
import pytest
from handle_df.handle_df import get_expected_json
from handle_df.handle_df import save_results_to_csv
import json
import logging
work_directory = '/Users/cheongray/iras_api_clean_1/1_Input_Validation'

xml_file_path = work_directory + "/xml_files_for_1_Input Validation"
filename_for_csv_with_results = '1_input_testing_csv_results'
filename_for_csv_with_results_full_path  = work_directory + '/test_results/'+ filename_for_csv_with_results + '.csv'
base_df_filepath = work_directory + '/df_full.csv'

if os.path.exists(filename_for_csv_with_results_full_path ):
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

@pytest.mark.parametrize("xml_file", xml_files)
def test_post_xml_to_api(xml_file):
    temp_xml_name_hold = xml_file.split('_')
    print(temp_xml_name_hold)
    test_case_id = int(temp_xml_name_hold[3])
 
    rule_id = temp_xml_name_hold[0]
    xml_data = load_xml_data(xml_file_path, xml_file)


    url = "https://public-stg.api.gov.sg/uat/gst/einvoicing/v1/submit"
    headers = {'Content-Type': 'application/xml; charset=utf-8','User-Agent': 'IRAS_TEST_AGENT'}


    response = requests.post(url, data=xml_data.encode('utf-8'), headers=headers)
    
    
    assert_result = "Passed"
    expected_json , expected_status= get_expected_json(base_df_filepath,test_case_id)
    

    actual_response = json.loads(response.text)
    #no key errors
    if actual_response['success']:#it passed.but passed when expecting fail is still a fail,error not caught
         temp_errors = ['']
         
         actual_status = actual_response['code']

         save_results_to_csv(work_directory,base_df_filepath,filename_for_csv_with_results,test_case_id,temp_errors,actual_status)
         try:
            assert int(expected_status) == actual_status, (
                f"Expected status: {expected_status}\n\n"
                f"Expected response: {expected_json}\n\n"
                f"Got: {actual_status}\n\n"
            )
         except AssertionError as e:
            raise e

    #means can access key errors
    elif not actual_response['success']: #failed,but could mean pass as caught error,or mean fail as supposed to  pass
        temp_errors = []
        temp_errors_string = ''
        actual_status = actual_response['code']
        for errors in actual_response['errors']:#could be
            temp_errors.append(errors['description'])
            temp_errors_string = temp_errors_string + errors['description']
        save_results_to_csv(work_directory,base_df_filepath,filename_for_csv_with_results,test_case_id,temp_errors,actual_status)
        try:
            assert int(expected_status) == actual_status, ( #could be 400 but exepecting 200.could also be 400 and exepcting 400
                f"Expected status: {expected_status}\n\n"
                f"Expected response: {expected_json}\n\n"
                f"Got: {actual_status}\n"
            )

            assert expected_json == temp_errors_string, (
                f"Expected response: {expected_json}\n\n"
                f"Got: {actual_response['errors']}\n\n"
            )
        except AssertionError as e:
            raise e





    # if expected_status == 400:#expecting 400 status.in no case where u are trying for 400 but u get 200 resulting in key error since no errors
        
    #     actual_status = response_json['code']
    #     actual_response = response_json['errors'][0]['description']
    #     if (expected_json != actual_response):
    #         print('______________*******________________')
    #         print(expected_json)
    #     assert expected_status == actual_status, (
    #         f"Expected status: {expected_status}\n"
    #         f"Got: {actual_status}\n"
    #     )
    #     assert expected_json == actual_response, (
    #         f"Expected response: {expected_json}\n"
    #         f"Got: {actual_response}\n"
    #     )


    # else:  # 200
        
    #     actual_status = response_json['code']
    #     print(response_json)
    #     assert expected_status == actual_status, (
    #         f"Expected status: {expected_status}\n"
    #         f"Got: {actual_status}\n"
    #     )

    #     # actual_response_200 = f'acknowledgment_id : {response_json["acknowledgementId"]}'#dk what else to store



