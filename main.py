import glob
import logging
import os
import tkinter as tk
import tkinter.messagebox as messagebox
import warnings
import zipfile
from pathlib import Path
from tkinter import filedialog

from PIL import Image, ImageTk
from tika import parser

warnings.filterwarnings("ignore", category=DeprecationWarning)


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


def extract_text_from_folder(data_path, generate_zip=True):
    """Extract text from all PDF files in the specified folder path."""
    all_files = glob.glob(os.path.join(data_path, '*.pdf'))
    _results = dict()
    for pdf_file in all_files:
        _results[pdf_file] = extract_text_pdf(pdf_file)

    if generate_zip:
        txt_path = os.path.join(data_path, 'Results')
        Path(txt_path).mkdir(parents=True, exist_ok=True)
        txt_files = []
        for pdf_path, text in _results.items():
            txt_file_path = pdf_path.replace(data_path, txt_path).replace('.pdf', '.txt')
            txt_files.append(txt_file_path)
            with open(txt_file_path, 'w', encoding='utf-8') as f:
                f.write(text)

        zip_path = os.path.join(txt_path, 'Results.zip')
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            for txt_file in txt_files:
                zip_file.write(txt_file)

    return _results


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.extract_button_photo = None
        self.folder_path = None
        self.generate_zip = None

        self.master = master
        self.master.title("PDF Text Extractor")
        self.master.geometry("530x160")
        self.master.configure(bg="#333333")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self, bg="#333333")
        main_frame.pack(fill="both")

        folder_frame = tk.Frame(main_frame, bg="#333333", pady=10)
        folder_frame.pack(fill="x", padx=5)

        folder_label = tk.Label(folder_frame, text="Select a folder:", bg="#333333", fg="white")
        folder_label.pack(side="left")

        self.folder_path = tk.StringVar()
        folder_entry = tk.Entry(folder_frame, textvariable=self.folder_path, width=50)
        folder_entry.pack(side="left", padx=10)

        folder_button = tk.Button(folder_frame, text="Browse", command=self.browse_folder, bg="#4e8752", fg="white",
                                  padx=10)
        folder_button.pack(side="left")

        options_frame = tk.Frame(main_frame, bg="#333333")
        options_frame.pack(fill="x")

        self.generate_zip = tk.BooleanVar()
        zip_checkbutton = tk.Checkbutton(options_frame,
                                         text="Generate zip file",
                                         variable=self.generate_zip,
                                         bg="#333333",
                                         fg="white",
                                         activebackground="#4e8752",
                                         selectcolor="#333333")
        zip_checkbutton.pack(side="left")

        extract_frame = tk.Frame(main_frame,
                                 bg="#333333")
        extract_frame.pack(fill="x")

        extract_button_photo = Image.open("assets/extract_button.png")
        extract_button_photo = extract_button_photo.resize((50, 50), Image.ANTIALIAS)
        self.extract_button_photo = ImageTk.PhotoImage(extract_button_photo)
        extract_button = tk.Button(extract_frame, image=self.extract_button_photo, command=self.extract_text,
                                   bg="#333333", borderwidth=0)
        extract_button.pack(side="left")

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        self.folder_path.set(folder_path)

    def extract_text(self):
        folder_path = self.folder_path.get()
        generate_zip = self.generate_zip.get()
        results = extract_text_from_folder(folder_path, generate_zip)
        message = f"Text extraction complete. Processed {len(results)} PDF files in total."
        if generate_zip:
            message += f" Text files saved in {os.path.join(folder_path, 'Results')}. Zip file saved in " \
                       f"{os.path.join(folder_path, 'Results.zip')}."
        else:
            message += f" Text files saved in {os.path.join(folder_path, 'Results')}."
        tk.messagebox.showinfo("Extraction Results", message)


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
