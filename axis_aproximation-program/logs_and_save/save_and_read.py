import csv
import os

def save_to(name, value):
    file_path = r"C:\Users\dawid\Desktop\praca magisterska\makra\logs_and_save\actions.csv"

    next_index = 1
    if os.path.isfile(file_path):
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            lines = list(reader)
            next_index = len(lines)  # Liczba linii (w tym nagłówka) w pliku
    else:
        next_index = 1
   
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([next_index,name, value])

def read_actions(index):
    file_path = r"C:\Users\dawid\Desktop\praca magisterska\makra\logs_and_save\actions.csv" 
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        lines = list(reader)
        return lines[index]

def read_logs(index):
    file_path = r"C:\Users\dawid\Desktop\praca magisterska\makra\logs_and_save\logs.csv" 
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        lines = list(reader)
        return lines[index]

