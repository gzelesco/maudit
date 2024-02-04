import glob

import xmltodict
from deepdiff import DeepDiff
from colorama import Fore, Style

from colorama import just_fix_windows_console
just_fix_windows_console()

# CONSTANTS:
SUBSTRING = '<irs>'
EXCLUDED_TAGS = [
    "root['irs']['header']['source_technical_reference']",
    "root['irs']['header']['source_linked_id']",
    "root['irs']['header']['related_id']",
    "root['irs']['mifid']['trade_date_time']",
    "root['irs']['action']['fo_creation_date']",
]

initial_message = '''Differences identified between the two files:
'''


# FUNCTIONS:

def find_xml_files():
    """
    Find XML files in the current directory and ensure there are exactly two.

    Returns:
        Tuple[str, str]: Filenames of the two XML files.
    """
    files = glob.glob('*.xml')
    if len(files) != 2:
        print("Error: Exactly two XML files are required.")
        exit(1)
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
        exit(1)
    except Exception as e:
        print(f"Error reading file '{file_name}': {e}")
        exit(1)

 
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
        exit(1)


def create_diff_list(diff_dic):
    #This is the only item that is created as list, not dictionary (workaround)
    try:
        diff_list = diff_dic.pop('dictionary_item_added')
    except:
        diff_list = None
    return diff_list


def message_generator(tag, old_value="None", new_value="None"):
    message = f'''\
Value of {tag} changed from \
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


def printer(diff_dic, diff_list=None):
    """
    Print the identified differences and new items in a readable format.

    Args:
        diff_dic (dict): Dictionary of differences.
        diff_list (list): List of differences.
    """
    print(initial_message)
    for key in diff_dic:
        message_box(key)
        for tag in diff_dic[key]:
            try:
                old_value = diff_dic[key][tag]["old_value"]
                new_value = diff_dic[key][tag]["new_value"]
                message = message_generator(tag,old_value,new_value)
                print(message)
            except Exception as e:
                print(f'ERROR: {tag} - {e}')
        print('\n')
    
    if not diff_list:
        message_box('No new items found.')
    else:
        message_box('New Items:')
        for new_item in diff_list:
            print(f'New item {new_item}')



def main():

    file1, file2 = find_xml_files()
    
    xml_string1 = read_file(file1)
    xml_string2 = read_file(file2)
    
    xml_string1 = split_string_from(xml_string1,SUBSTRING)
    xml_string2 = split_string_from(xml_string2,SUBSTRING)
    
    python_dict1 = xmltodict.parse(xml_string1)
    python_dict2 = xmltodict.parse(xml_string2)
    
    if python_dict1 == python_dict2:
        print("XML 1 is equal to XML 2")
        exit(0)
    
    diff_dic = DeepDiff(python_dict1, python_dict2,
                        verbose_level=1, exclude_paths=EXCLUDED_TAGS)
    
    diff_list = create_diff_list(diff_dic)
    
    printer(diff_dic, diff_list)


if __name__ == '__main__':
    main()
    exit()
