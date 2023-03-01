# Textify-PDF

Textify-PDF is a Python script that extracts text from all PDF files in a specified folder path and saves them as .txt files. It uses the Tika library to extract text from the PDF files.

## Installation

1. Clone the repository or download the ZIP file and extract it to a folder.
2. Install the required Python libraries using pip: `pip install -r requirements.txt`

## Usage

1. Open a terminal or command prompt in the folder where you extracted the files.
2. Run the script using the command: `python main.py`
3. Enter the path to the folder containing the PDF files when prompted, eg: 'D:\CODES\textify-pdf'

The script will extract text from all PDF files in the specified folder and save them as .txt files in a "txt" subfolder. 
It also generates a zip file containing all the processed .txt files.

New feature: The script now supports processing of password-protected PDF files. If a password-protected PDF file is encountered, the script will skip the file and log a warning message.

## Usage screenshot Samples

![folder_selection.png](assets%2Ffolder_selection.png)

![success.png](assets%2Fsuccess.png)

## License

Textify-PDF is licensed under the [MIT License](https://github.com/username/repo/blob/master/LICENSE).
