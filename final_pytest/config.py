import os
from datetime import datetime


current_time = datetime.now()


formatted_time = current_time.strftime('%Y%m%d')

unique_name = 'Tiramisu'#unique id change to whatever


parent_1 = os.path.dirname(os.getcwd())


base_path_concat = os.path.join(os.path.dirname(parent_1),'iras_api_clean_1')

log_dir = os.path.dirname(base_path_concat) + '/Full_Logs/logs_2'

unique_identifier_for_test_results = formatted_time + '_' + unique_name
print(unique_identifier_for_test_results)
# work_directory = os.path.join(base_path_concat,'1_Input_Validation')
# print(work_directory)

