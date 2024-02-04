# Maudit
Murex AUDIT

This script is designed to identify and display the differences between two XML files. It utilizes the `xmltodict` library to parse XML files into Python dictionaries and the `deepdiff` library to perform a deep comparison between these dictionaries. The script then presents the identified differences in a human-readable format.


## Installation

### Prerequisites
- Python 3.x
- Donwload this package
- Virtual environment creation

### Download Package
You can clone this directory directly using Git or download it manually and unzip by clicking on `<>Code -> Download ZIP` on this page.

### Set up Virtual Environment and Install Required Packages
1. Open a terminal or command prompt.
2. Navigate to the `maudit` directory where you have saved this package.
3. Run the following commands to create a virtual environment:
   ```bash
   python -m venv venv
4. Run the following commands to activate a virtual environment:
   ```bash
   venv\Scripts\activate       # For Windows
5. You'll notice that the prompt changes to include (venv), indicating that you are now within the Virtual Environment.
5. While in the virtual environment, run the following command to install the required packages:

   ```bash
   pip install -r requirements.txt
## Usage
1. Ensure your XML files (with a ".xml" extension) are located in the same directory as the script.
2. Two XML files are required to run this program. If more or fewer files are present in the directory, an error message will be raised.
3. Execute 'maudit_run.bat' to run the script.

## Note
This script assumes that the structure of both XML files is the same, and the root tag is `<irs><\irs>`.
