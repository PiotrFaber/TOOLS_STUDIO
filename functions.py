# Copyright (C) 2023 Łebi

import os
import ctypes
import fnmatch
import traceback
from pathlib import Path
from PySide6.QtWidgets import QFileDialog


def messagebox(button_style, title, text, icon):
    ctypes.windll.user32.MessageBoxW(icon, text, title, button_style)


def count_files(path, file_ext):
    nr_of_files = 0
    for file in os.listdir(path):
        if fnmatch.fnmatch(file, file_ext):
            nr_of_files += 1
    if nr_of_files == 0:
        messagebox(0, "Uwaga", "Brak plików " + file_ext + " w katalogu z danymi !", 0)
        return 0
    else:
        return nr_of_files


def get_path():
    dir_name = QFileDialog.getExistingDirectory(caption="Wybierz katalog")
    dir_name = dir_name.replace("/", "\\")
    return dir_name


def get_file_dxf():
    file_name = QFileDialog.getOpenFileName(caption="Wybierz plik .dxf", filter="*.dxf")
    file_name = file_name[0]
    file_name = file_name.replace("/", "\\")
    return file_name


def check_path(path, path_type):
    if Path(path).is_dir() == False or path == "":
        if path_type == "input":
            messagebox(0, "Uwaga", "Błędna ścieżka do katalogu z danymi !", 0)
        elif path_type == "output":
            messagebox(0, "Uwaga", "Błędna ścieżka do katalogu wynikowego !", 0)
    else:
        return True


def check_file(file, file_type):
    if Path(file).is_file() == False or file == "":
        messagebox(0, "Uwaga", "Błędna ścieżka do pliku !", 0)
    else:
        if file_type != file[-4:]:
            messagebox(0, "Uwaga", "Błędny plik !", 0)
        else:
            return True


def compare_path(path_input, path_output):
    if path_input == path_output:
        messagebox(0, "Uwaga", "Takie same ścieżki !", 0)
    else:
        return True


def error(path_input, path_output, file):
    if path_output == "":
        logfile = open(os.path.join(path_input, "logfile.log"), "a")
    else:
        logfile = open(os.path.join(path_output, "logfile.log"), "a")
    traceback.print_exc(file=logfile)
    logfile.close()
    messagebox(0, "Error", "Problem z plikiem:  "
               + file + "\n\nWięcej informacji w pliku logfile !", 0)


def summary(nr_of_files_all, nr_of_files_processed):
    messagebox(0, "Podsumowanie", "Ilość wszystkich plików:  " + str(nr_of_files_all)
               + "\n\nIlość przetworzonych plików:  " + str(nr_of_files_processed), 0)


def check_ov(ov):
    if ov == "":
        messagebox(0, "Uwaga", "Wskaż overview do wygenerowania !", 0)
    else:
        return True


def compress_message():
    messagebox(0, "Uwaga", "Jeżeli chcesz skompresować tify wskaż katalog wynikowy !", 0)


def overview_message():
    messagebox(0, "Uwaga", "Wybierz co ma wykonać program !", 0)


def dxf_IOerror_message():
    messagebox(0, "Uwaga", "To nie jest plik dxf lub błąd I/O !", 0)


def dxf_StructureError_message():
     messagebox(0, "Uwaga", "Nieprawidłowy lub uszkodzony plik dxf !", 0)
