#!/usr/bin/env python
# coding: utf-8

# # Series2Graph Demo
# 
# This notebook describe and display all the step that series2graph preforms in order to detect abnormal subsequences in a time series.

# In[ ]:


import matplotlib.pyplot as plt
from series2graph import series2graph as sg, series2graph_tools as sg_tools
import  numpy as np
import pandas as pd


# In[Setup log function]
import sys
from datetime import datetime
import logging

log_file = "logfile.txt"
def write_log(*args): 
   now = datetime.now()
   current_time = now.strftime("%H:%M:%S")

   #logger = get_logger()
   line = ' '.join([str(a) for a in args])
   line = f'{current_time} ' + line 
   f_log = open(log_file,'a', encoding='utf-8')
   f_log.write(line+'\n')
   f_log.close()
   print(line)
# In[Compute graph for one serie]:
def graph_one_serie(df, column_name, measure):
   # ## Parameters setting
   
   pattern_length = 100
   query_length = 25
   latent = 15
   
   
   # In[ ]:
   
   # ## Computing the Graph
   write_log("define model Series2Graph")
   s2g = sg.Series2Graph(pattern_length = pattern_length,latent = latent)
   write_log("fit the model")
   s2g.fit(df)
   #s2g.plot_graph()
   
   # In[ ]:
   
   write_log("fit the model Graph Statistics:")
   print("Graph Statistics:")
   print("Number of nodes: {}".format(s2g.graph['Graph'].number_of_nodes()))
   print("Number of edges: {}".format(s2g.graph['Graph'].number_of_edges()))
        
   # In[ ]:
      
   # ## Anomalies detection
   write_log("Anomalies detection - compute scores")
   s2g.score(query_length)
   # s2g.plot_graph()
      
   # In[ ]:
      
   ### Visualization of the full time series
   write_log("Visualization of the full time series:")
   tmp_score = s2g.all_score
   xlim=min(len(df[0]),len(tmp_score))
   delta=len(df[0])-xlim

   # fig,ax = plt.subplots(1,1,figsize=(20,8))
   # ax.plot(df[0].values[-xlim:])
   # ax.set_xlim(0,xlim)
   # ax.title.set_text(f'{measure} {column_name}')
   # plt.show()     
   
   # In[Create anomalies data frame]
   
   # Set threshold = mean + standrdDeviation
   threshold = tmp_score.mean() + tmp_score.std()
   
   anom_val = []
   anom_score = []
   df_data = []
   for i in range(xlim):
       df_data.append(df[0].values[i+delta])
       if(tmp_score[i] > threshold):
           anom_val.append(df[0].values[i+delta])
           anom_score.append(tmp_score[i])
       else: 
           anom_val.append(np.nan)
           anom_score.append(np.nan)
                  
   # In[Plot anomalies]

   fig, ax = plt.subplots(2,1,figsize=(20,12))
   ax[0].plot(df_data[-xlim:])
   ax[0].plot(anom_val[-xlim:],"ro")
   ax[0].title.set_text(f'{measure} {column_name}')
   ax[0].set_xlim(0,xlim)

   ax[1].plot(anom_val[-xlim:])
   ax[1].set_xlim(0,xlim)
   ax[1].title.set_text(f'Score - {measure} {column_name} - threshold {threshold:.2f}')
   plt.show()   
   return pd.DataFrame(anom_val)

# In[Reading data]:

def read_data(dataset):
   write_log("read_csv file /DATA/ATM_ECG_803.ts")
   #dataset = 1  # select wich file to read
   if dataset == 0:
      columns= ['Date','Memory']
      df = pd.read_csv('https://raw.githubusercontent.com/odedns/hackathon/4625c602ff05bc013027a677871ec31f8e66301c/SourceCode/DATA/Memory-data-2021-04-28%2017_06_58.csv',
            skiprows = 1,
            names = columns,
            delimiter = '\t',
            header=None)
      columns= ['Memory']
      df['Memory'] = df['Memory']/1000000000
      measure = 'memory usage'
      
   elif dataset == 1:
      columns= ['Received','Sent']
      df = pd.read_csv('https://raw.githubusercontent.com/odedns/hackathon/addca50515a1f2749ed62e62f15055dfadc0f916/SourceCode/DATA/Total%20Network%20I_O%20pressure%20-data-as-seriestocolumns-2021-04-28%20%2017_08_56.csv',
        delimiter = '\t')
      measure = 'network i/o'
      
   elif dataset == 2:
      columns= ['Time','CPU Usage']
      df = pd.read_excel('https://raw.githubusercontent.com/odedns/hackathon/4625c602ff05bc013027a677871ec31f8e66301c/SourceCode/DATA/CPU-data-2021-04-28%2017_03_23.xlsx',
         sheet_name=0)
      columns= ['CPU Usage']
      measure = 'CPU usage'
      
   elif dataset == 3:
      df = pd.read_csv("../DATA/ATM_ECG_803.ts",header=None)[-10000:]
      columns= [0]
      measure = 'ATM_ECG_803'
   elif dataset == 4:
      df = pd.read_csv('https://query1.finance.yahoo.com/v7/finance/download/BKHYY?period1=1201824000&period2=1997753600&interval=1d&events=history&includeAdjustedClose=true',)
      measure = 'BKHYY'
      columns= ['Open','High','Low','Close','Adj Close','Volume']
   elif dataset == 5:
      df = pd.read_csv('https://query1.finance.yahoo.com/v7/finance/download/BLMIF?period1=1199145600&period2=1619308800&interval=1d&events=history&includeAdjustedClose=true')
      measure = 'BLMIF'
      columns= ['Open','High','Low','Close','Adj Close','Volume']
   elif dataset == 6:
      df = pd.read_csv('https://query1.finance.yahoo.com/v7/finance/download/JPM?period1=1199145600&period2=1619308800&interval=1d&events=history&includeAdjustedClose=true', )
      columns= ['Open','High','Low','Close','Adj Close','Volume']
      measure='JP Morgan'
   else:
      raise('Invalid dataset selection')
   
   print("Time Series Statistics:")
   print(f'Dataset: {measure}, columns: {columns}')
   print("Number of points: {}".format(len(df)))
   print("Data frame: {}",df)
   print("Data frame: {}",df.info())
   return columns, measure, df

# In[Visualize datasets]
# ### Visualization of a snippet
# write_log("Visualization of dataset")
# if len(columns) == 1:
#    fig,ax = plt.subplots(1,1,figsize=(20,12))
#    ax.title.set_text(f'{measure} - {columns[0]}')
#    ax.plot(df[columns[0]].values)
#    ax.set_ylim(min(df),max(df))
# else:
#    fig,ax = plt.subplots(len(columns),1,figsize=(20,20))
#    for i in range(len(columns)):
#       ax[i].title.set_text(f'{measure} - {columns[i]}')
#       ax[i].plot(df[columns[i]].values)
#       ax[i].set_ylim(min(df),max(df))
# plt.show()

# In[compute graph for each serie]
#anomal_values=pd.DataFrame([])
anomal_values=[]
for dataset in range(6):
   columns, measure, df = read_data(dataset)
   for i in columns:
      tmp = pd.DataFrame(df[i])
      tmp.rename(columns = {i:0}, inplace = True)
      tmp.dropna(subset = [0], inplace=True)
      anomal_values.append(graph_one_serie(tmp, i, measure))
   
# In[Done ]:

write_log("Done!")


# In[test materna]
import requests, zipfile, StringIO
r = requests.get('http://data.octo.dc.gov/feeds/crime_incidents/archive/crime_incidents_2013_CSV.zip')
z = zipfile.ZipFile(StringIO.StringIO(r.content))
crime2013 = pd.read_csv(z.read('crime_incidents_2013_CSV.csv'))