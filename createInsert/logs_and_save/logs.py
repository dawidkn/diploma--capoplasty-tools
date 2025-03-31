import csv
import os
from datetime import datetime
import NXOpen
import traceback
import sys
from pathlib import Path

def log(name, val1):
    base_path = Path(__file__).parent
    file_path = base_path / "logsInsert.csv"

    
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

    base_path = Path(__file__).parent
    file_path = base_path / "logsInsert.csv"
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
    sys.exit("Critical error. Check logsInsert.csv file for more information.")
        