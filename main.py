import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading


class PrintStatementConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Print Statement Converter')
        self.geometry('400x150')

        # Button to select files
        self.btn_select_files = tk.Button(self, text='Select Files', command=self.select_files)
        self.btn_select_files.pack(pady=10)

        # Button to select directory
        self.btn_select_directory = tk.Button(self, text='Select Directory', command=self.select_directory)
        self.btn_select_directory.pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress.pack(pady=20)

    def convert_print_statements(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        pattern = re.compile(r'print\s+"(.*?)"')
        updated_content = pattern.sub(r'print("\1")', content)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)

    def update_files(self, files):
        for index, file in enumerate(files):
            if file.endswith('.py'):
                self.convert_print_statements(file)
                # Update progress bar
                progress = (index + 1) / len(files) * 100
                self.progress['value'] = progress
                self.update_idletasks()
        messagebox.showinfo("Completion", "All files have been updated.")

    def select_files(self):
        files = filedialog.askopenfilenames(title='Select Python Files', filetypes=(('Python Files', '*.py'),))
        if files:
            threading.Thread(target=self.update_files, args=(files,), daemon=True).start()

    def select_directory(self):
        directory = filedialog.askdirectory(title='Select Directory')
        if directory:
            files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.py')]
            threading.Thread(target=self.update_files, args=(files,), daemon=True).start()


if __name__ == "__main__":
    app = PrintStatementConverterApp()
    app.mainloop()
