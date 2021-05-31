# -*- coding: utf-8 -*-
"""
Created on Tue May 18 16:52:28 2021

@author: ion_g
"""
import os
from io import BytesIO
from zipfile import ZipFile
import pandas
import requests
url = 'http://atlarge.ewi.tudelft.nl/graphalytics/cloud/GWA-T-13_Materna-Workload-Traces.zip'
content = requests.get(url)
zf = ZipFile(BytesIO(content.content))
#match = [s for s in zf.namelist() if "csv" in s][0]
CPU_file = 'GWA-T-13_Materna-Workload-Traces/Materna-Trace-1/01.csv'
df = pandas.read_csv(zf.open(CPU_file),encoding='latin-1', error_bad_lines=False,
                     delimiter=";", decimal=",")
print(df.info())
cwd = os.getcwd()
df.to_csv('..\\DATA\\Materna-Traces\\01.csv')