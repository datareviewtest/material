
from my_gpt import save_chat_history
from utils import save_to_excel, get_logcat
from datetime import datetime



def log_and_save_history(reprot_file_name, start_time, response_time, total_commands, history, package_name, error_type):
    execution_time = (datetime.now() - start_time).total_seconds()
    print(f"!!!{error_type}!!!. Execution time: {execution_time} seconds")
    print(f"!!!Response Times: {response_time}. Total Commands: {total_commands}")
    #save_to_excel({'Issue': [reprot_file_name[:-4]], 'Time': [execution_time], '#Commands': [total_commands], '#Responses': [response_time] }, 'bug_reproduction_data.xlsx')
    #save_chat_history(history, package_name)


def check_crash(device_port):
    logcat = get_logcat(device_port)
    if 'FATAL' in logcat:
        print('Found fatal')
        return True
    return False

def compare_widget_dicts(prev_widget_dict, current_widget_dict):
    print('prev:', prev_widget_dict)
    print('after:', current_widget_dict)

    prev_widgets = []
    current_widgets = []
    for key in prev_widget_dict:
        for widget in prev_widget_dict[key]:
            non_loc_elem = next((elem for elem in widget if not elem.startswith('[')), None)
            prev_widgets.append(non_loc_elem if non_loc_elem else widget)
        if key in current_widget_dict:
            for widget in current_widget_dict[key]:
                non_loc_elem = next((elem for elem in widget if not elem.startswith('[')), None)
                current_widgets.append(non_loc_elem if non_loc_elem else widget)
    return prev_widgets, current_widgets


def calculate_common_percentage(prev_list, current_list):
    if not prev_list and not current_list:
        return 0.0
    if not prev_list or not current_list:
        return 0.0
    common_elements = set(prev_list).intersection(set(current_list))
    common_percentage = len(common_elements) / len(prev_list) * 100 if prev_list else 0.0
    return common_percentage


def check_EMJD(prev_widget_dict, current_widget_dict):
    return

def check_BD(reprot_file_name, prev_widget_dict, current_widget_dict, execution_data, history, package_name):
    prev_widgets, current_widgets = compare_widget_dicts(prev_widget_dict, current_widget_dict)
    if current_widgets == prev_widgets:
        print('nongthing change')
        return False
    elif all(widget in prev_widgets for widget in current_widgets):
        widget_percentage = calculate_common_percentage(prev_widgets, current_widgets)
        print('common_widgets_percentage', widget_percentage)
        print('include')
        return False
    else:
        widget_percentage = calculate_common_percentage(prev_widgets, current_widgets)
        print('common_widgets_percentage', widget_percentage)
        start_time, response_time, total_commands = execution_data
        log_and_save_history(reprot_file_name, start_time, response_time, total_commands, history, package_name, 'BM')
        return True
def check_BNR():
    return
def check_LNS():
    return

def check_PCCR(reprot_file_name, prev_widget_dict, current_widget_dict, prev_other_text, current_other_text, execution_data, history, package_name):
    prev_widgets, current_widgets = compare_widget_dicts(prev_widget_dict, current_widget_dict)
    if prev_widgets is None or current_widgets is None:
        print("An error occurred: a key in prev_widget_dict was not found in current_widget_dict.")
        return False
    if current_widgets == prev_widgets and prev_other_text == current_other_text:
        print('nongthing change')
        return False
    else:
        text_percentage = calculate_common_percentage(prev_other_text, current_other_text)
        widget_percentage = calculate_common_percentage(prev_widgets, current_widgets)

        print('common_text_percentage', text_percentage)
        print('common_widgets_percentage', widget_percentage)
        if text_percentage > 0.5 and widget_percentage > 0.5:
            print('no change')
            return False
        else:
            start_time, response_time, total_commands = execution_data
            log_and_save_history(reprot_file_name, start_time, response_time, total_commands, history, package_name, 'PCCR')
            return True

    return False






