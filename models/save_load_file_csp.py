import os
import pickle
from tkinter import filedialog


def save_championship(csp_object):
    file_path = filedialog.asksaveasfilename(defaultextension=".pickle")
    if file_path != '':
        with open(file_path, 'wb') as file:
            pickle.dump(csp_object, file)
        return True
    return False


def load_championship():
    file_path = filedialog.askopenfilename()
    if file_path != '':
        with open(file_path, 'rb') as file:
            csp_object = pickle.load(file)
        return csp_object


def save_backup(csp_object):
    if not os.path.exists('backup'):
        os.mkdir('backup')
    with open('backup/backup.pickle', 'wb') as file:
        pickle.dump(csp_object, file)


def load_backup():
    with open('backup/backup.pickle', 'rb') as file:
        csp_object = pickle.load(file)
    return csp_object
