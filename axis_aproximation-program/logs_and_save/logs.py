import csv
import os
from datetime import datetime
import NXOpen
import traceback
import sys

def log(name, val1):
    file_path = r"C:\Users\dawid\Desktop\praca magisterska\axis_aproximation-program\logs_and_save\logs.csv"

    
    next_index = 0
    if os.path.isfile(file_path):
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            lines = list(reader)
            next_index = len(lines)  # Liczba linii (w tym nagłówka) w pliku
    else:
        next_index = 0
   
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer = csv.writer(file)
        writer.writerow([f"{next_index}. {current_datetime} - {name}: Value - {val1}"])

def errorLog():

    file_path = r"C:\Users\dawid\Desktop\praca magisterska\axis_aproximation-program\logs_and_save\logs.csv"
    next_index = 0
    theSession  = NXOpen.Session.GetSession()
    logFile = theSession.LogFile
    errorMSG = traceback.format_exc()
    if os.path.isfile(file_path):
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            lines = list(reader)
            next_index = len(lines)  # Liczba linii (w tym nagłówka) w pliku
    else:
        next_index = 0
   
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer = csv.writer(file)
        writer.writerow([f"{next_index}. {current_datetime} - LogError: {errorMSG}"])
def errorExit():
    sys.exit("Critical error. Check logs.csv file for more information.")
        