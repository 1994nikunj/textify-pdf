# glob: used to find all .pdf files in the specified folder
import glob
# logging: used for logging error messages
import logging
# os: used for file path manipulation and joining
import os
# zipfile: used for creating a zip file
import zipfile
# configparser: used for reading configuration settings from a .ini file
from configparser import ConfigParser
# datetime: used for measuring the execution time of the script
from datetime import datetime
# pathlib: used for creating directories if they don't exist
from pathlib import Path

# tika.parser: used for extracting text from PDF files
from tika import parser


def extract_text_pdf(file_path):
    """Extract text from a given PDF file (full path required)."""
    try:
        raw_text = parser.from_file(file_path)
        text = raw_text['content']
    except KeyError:
        logging.warning(f'No "content" key found in the extracted PDF file: {file_path}')
        text = ''
    except ValueError:
        logging.warning(f'The PDF file {file_path} appears to be encrypted or corrupted')
        text = ''
    except Exception as e:
        logging.warning(f'Could not extract text from {file_path}. Reason: {str(e)}')
        text = ''

    return text


def extract_text_from_folder(folder_path, generate_zip=True):
    """Extract text from all PDF files in the specified folder path."""
    all_files = glob.glob(os.path.join(folder_path, '*.pdf'))
    _results = dict()
    for pdf_file in all_files:
        _results[pdf_file] = extract_text_pdf(pdf_file)

    if generate_zip:
        txt_path = os.path.join(folder_path, 'txt')
        Path(txt_path).mkdir(parents=True, exist_ok=True)
        txt_files = []
        for pdf_path, text in _results.items():
            txt_file_path = pdf_path.replace(folder_path, txt_path).replace('.pdf', '.txt')
            txt_files.append(txt_file_path)
            with open(txt_file_path, 'w', encoding='utf-8') as f:
                f.write(text)

        zip_path = os.path.join(folder_path, 'txt.zip')
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            for txt_file in txt_files:
                zip_file.write(txt_file)

    return _results


if __name__ == '__main__':
    create_zip = True

    config = ConfigParser()
    config.read('config.ini')
    log_path = config['DEFAULT'].get('log_path')
    if log_path:
        logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    start_time = datetime.now()
    logging.info(f'Start time: {start_time}')

    path = input('Enter the path to the folder containing the PDF files: ')

    results = extract_text_from_folder(path, generate_zip=create_zip)

    end_time = datetime.now()
    logging.info(f'End time: {end_time}')
    logging.info(f'Total time taken: {end_time - start_time}')

    print('\nText extraction complete.')
    print(f'Processed {len(results)} PDF files in total.')
    print(f'Text files saved in {os.path.join(path, "txt")}.')
    print(f'Zip file saved in {os.path.join(path, "txt.zip")}.')
