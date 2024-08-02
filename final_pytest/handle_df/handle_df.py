import pandas as pd
import json
import os
#need to clear csv results if not the old results will stick to the new one
def get_expected_json(base_df_filepath,test_case_id):

    path = base_df_filepath#base template
    pd.set_option('display.max_colwidth', None)
    df = pd.read_csv(path)

    # df = df_base.copy()#copy over


    # if len(actual_res) == 0: #get responses
    e_j = df[df['Test Case ID'] == test_case_id]['Expected Result Response (for 400 response)'].to_string(index=False)
    e_s = df[df['Test Case ID'] == test_case_id]['Expected Result'].to_string(index=False)
    e_d = df[df['Test Case ID'] == test_case_id]['Test Case Description'].to_string(index=False)
    if e_s.endswith('.0'):
        e_s = int(e_s[:-2])
    e_j_formatted = e_j.replace("\\n", "")
    return(e_j_formatted,e_s)
    # else:
    #     if df['Actual Result'].dtype != 'object':
    #         df['Actual Result'] = df['Actual Result'].astype('object')
    
    #     actual_response = json.dumps(actual_res)
    #     # if assert_result is not None:
    #     #     if 'Assertion Result' not in df.columns:
    #     #         df['Assertion Result'] = ''
    #     #     df.loc[df['Test Case ID'] == test_case_id, 'Assertion Result'] = assert_result
    #     df.loc[df['Test Case ID'] == test_case_id,'Actual Result'] = actual_response
    #     df.to_csv('/Users/cheongray/iras_api_pytest_1/df_s_peppol.csv',index=False)

def save_results_to_csv(work_dir,base_df_filepath,filename_for_results,test_case_id,actual_res,actual_status):

    results_folder = '/test_results/'
    results_folder_path = work_dir + results_folder 
    if not os.path.exists(results_folder_path):
        os.makedirs(results_folder_path)
    path_results = work_dir + results_folder + filename_for_results + '.csv'

    

    # base_df_path = '/Users/cheongray/iras_api_make_xml/df_full.csv'

    if not os.path.exists(path_results):#if it doesnt exist,then read in the base template from df_full.csv
        print('-------DOES NOT EXITST')
        base_df_path = base_df_filepath

        df_base = pd.read_csv(base_df_path)

        df_base.to_csv(path_results,index=False)

        
    pd.set_option('display.max_colwidth', None)
    df = pd.read_csv(path_results)

    if 'Actual Response Pass/Fail' not in df.columns:
        df['Actual Response Pass/Fail'] = ''
    if 'Acutal Status Pass/Fail' not in df.columns:
        df['Acutal Status Pass/Fail'] = ''
    if 'Both status and result Pass/Fail' not in df.columns:
        df['Both status and result Pass/Fail']=''

    if df['Both status and result Pass/Fail'].dtype != 'object':
        df['Both status and result Pass/Fail'] =  df['Both status and result Pass/Fail'].astype('object')



    if df['Actual Result'].dtype != 'object':
        df['Actual Result'] = df['Actual Result'].astype('object')

    if df['Actual Result Response (for 400 response)'].dtype != 'object':

        df['Actual Result Response (for 400 response)'] = df['Actual Result Response (for 400 response)'].astype('object')


    if df['Actual Response Pass/Fail'].dtype != 'object':
        df['Actual Response Pass/Fail'] = df['Actual Response Pass/Fail'].astype('object')


    expected_json =  df.loc[df['Test Case ID'] == test_case_id,'Expected Result Response (for 400 response)'].values[0]
    print('TEST CASE ID')
    print(test_case_id)
    expected_status = df.loc[df['Test Case ID'] == test_case_id,'Expected Result'].values[0]

    print(f'expected status:{expected_status}')
    if pd.isna(expected_json):
        print('-----------++++++++______')
        print('its nan!')

    print(f'expected json:{expected_json}')

    result_full =''
   
    
    for result in actual_res:
        result = str(result) + '\n'
        result_full = result_full + result
    result_full = result_full.strip()
    
    df.loc[df['Test Case ID'] == test_case_id,'Actual Result'] = actual_status
    if expected_status == int(actual_status):
         df.loc[df['Test Case ID'] == test_case_id,'Acutal Status Pass/Fail'] = f'Pass'

    else:
         df.loc[df['Test Case ID'] == test_case_id,'Acutal Status Pass/Fail'] = f'Fail'
        #  df.loc[df['Test Case ID'] == test_case_id,'Actual Response Pass/Fail'] = 'Fail'#if status fail response of course fails

    if expected_json == result_full:
         df.loc[df['Test Case ID'] == test_case_id,'Actual Response Pass/Fail'] = f'Pass'

    else:
        # df.loc[df['Test Case ID'] == test_case_id,'Actual Response Pass/Fail'] = f'Fail'
        if pd.isna(expected_json):
            df.loc[df['Test Case ID'] == test_case_id,'Actual Response Pass/Fail'] = ''
        else:
            df.loc[df['Test Case ID'] == test_case_id,'Actual Response Pass/Fail'] = f'Fail'
         
    if actual_status == 400:
         df.loc[df['Test Case ID'] == test_case_id,'Actual Result Response (for 400 response)'] = result_full


    actual_response_condition = (df.loc[df['Test Case ID'] == test_case_id, 'Actual Response Pass/Fail'] == 'Pass').any()
    print('####################################')
    print('      ')
    print(actual_response_condition)
    print('####################################')

    df.loc[(df['Actual Response Pass/Fail']=='Pass')&(df['Acutal Status Pass/Fail']=='Pass'), 'Both status and result Pass/Fail'] = 'Pass'


    
    df.to_csv(path_results,index=False)


def save_error_as_json():
    pass
if __name__ == '__main__':
    expected_json , expected_status = get_expected_json(644,'1')
    print(expected_json)  


#will not match if there are multiple errors to match
#need handle new lines