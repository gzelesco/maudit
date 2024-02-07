import glob
import time  # Used only for a more pleasurable experience


import xmltodict
from deepdiff import DeepDiff
from colorama import Fore, Style, Back

from colorama import just_fix_windows_console
just_fix_windows_console()

# CONSTANTS:
SUBSTRING = '<'
EXCLUDED_TAGS = [
    "root['irs']['header']['source_technical_reference']",
    "root['irs']['header']['source_linked_id']",
    "root['irs']['header']['related_id']",
    "root['irs']['mifid']['trade_date_time']",
    "root['irs']['action']['fo_creation_date']",
]

initial_message = '''
WELCOME TO MAUDIT

Usage
1. Ensure your XML files (with a ".xml" extension) are located in the same directory as this program.
2. Two XML files are required to run this program. If more or fewer files are present in the directory, an error message will be raised.
3. The differences between the two XML files will be displayed on the command screen with distinct colors for clarity.
4. For access to the source code, visit https://github.com/gzelesco/maudit

Differences identified between the two files:
'''


# FUNCTIONS:
def exit_error():
    close = input('Press ENTER to close this window.')
    exit(1)
    
def find_xml_files():
    """
    Find XML files in the current directory and ensure there are exactly two.

    Returns:
        Tuple[str, str]: Filenames of the two XML files.
    """
    files = glob.glob('*.xml')
    if len(files) != 2:
        print("Error: Exactly two XML files are required.")
        exit_error()
    file1, file2 = files
    return file1, file2


def read_file(file_name):
    """
    Read the content of the specified file.

    Args:
        file_name (str): Name of the file to read.

    Returns:
        str: Content of the file.
    """
    try:
        with open(file_name, "r") as file:
            file_str = file.read()
        return file_str
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        exit_error()
    except Exception as e:
        print(f"Error reading file '{file_name}': {e}")
        exit_error()

 
def split_string_from(input_string, substring):
    """
    Split the input string from the specified substring and return the substring onwards.

    Args:
        input_string (str): Input string to be split.
        substring (str): Substring to split from.

    Returns:
        str: Substring onwards.
    """
    try:
        index_of_substring = input_string.find(substring)
        if index_of_substring != -1:
            return input_string[index_of_substring:]
        else:
            raise ValueError(f"{substring} not found in the input string.")
    except Exception as e:
        print(f"Error: {e}")
        exit_error()


def create_diff_list(diff_dic, item_to_pop):
    #This is the only item that is created as list, not dictionary (workaround)
    try:
        diff_list = diff_dic.pop(item_to_pop)
    except:
        diff_list = None
    return diff_list


def message_generator(tag, old_value="None", new_value="None"):
    message = f'''\
Value of {tag} changed from  \
{Fore.RED + str(old_value)} \
{Style.RESET_ALL}to \
{Fore.GREEN + str(new_value)}\
{Style.RESET_ALL}.\
    '''
    return message


def message_box(input_str):
    #Print a stylized box around the input string.
    print(len(input_str)*"_")
    print(f"{'\033[4m' + input_str}{Style.RESET_ALL}")



def printer(diff_dic):
    """
    Print the identified differences and new items in a readable format.

    Args:
        diff_dic (dict): Dictionary of differences.
        diff_list (list): List of differences.
    """
    for key in diff_dic:
        message_box(key)
        time.sleep(0.5)
        for tag in diff_dic[key]:
            try:
                old_value = diff_dic[key][tag]["old_value"]
                new_value = diff_dic[key][tag]["new_value"]
                message = message_generator(tag,old_value,new_value)
                print(message)
                time.sleep(0.01)
            except Exception as e:
                print(f'ERROR: {tag} - {e}')
        print('\n')
    
    
def print_list(diff_list=None,type_list="Chenged"):
    if not diff_list:
        message_box(f'No {type_list} found.')
    else:
        message_box(f'{type_list}:')
        for new_item in diff_list:
            print(f'{type_list} {new_item}')



def main(file1, file2):
    
    xml_string1 = read_file(file1)
    xml_string2 = read_file(file2)
    
    xml_string1 = split_string_from(xml_string1,SUBSTRING)
    xml_string2 = split_string_from(xml_string2,SUBSTRING)
    
    python_dict1 = xmltodict.parse(xml_string1)
    python_dict2 = xmltodict.parse(xml_string2)
    
    if python_dict1 == python_dict2:
        print("XML 1 is equal to XML 2")
        exit_error()
    
    diff_dic = DeepDiff(python_dict1, python_dict2,
                        verbose_level=1, exclude_paths=EXCLUDED_TAGS)
    
    diff_add= create_diff_list(diff_dic, "dictionary_item_added")
    diff_removed= create_diff_list(diff_dic, "dictionary_item_removed")
    
    printer(diff_dic)
    print_list(diff_add, "New Itens")
    print_list(diff_removed, "Itens Removed")
    close = input('Press ENTER to close this window.')


if __name__ == '__main__':
    print(initial_message)
    file1, file2 = find_xml_files()
    main(file1,file2)
    exit()