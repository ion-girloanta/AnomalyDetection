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

# ## Demo on an ECG time series
# 
# The full process of Time2graph applied on a time series corresponding to an electro-cardiogram from the ATM physiobank dataset (record 803).

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
def graph_one_serie(df, column_name):
   # ## Parameters setting
   
   pattern_length = 50
   query_length = 10
   
   
   
   # In[ ]:
   
   # ## Computing the Graph
   write_log("define model Series2Graph")
   s2g = sg.Series2Graph(pattern_length=pattern_length, latent=1)
   write_log("fit the model")
   s2g.fit(df)
#   s2g.plot_graph()
   
   # In[ ]:
   
   write_log("fit the model Graph Statistics:")
   print("Graph Statistics:")
   print("Number of nodes: {}".format(s2g.graph['Graph'].number_of_nodes()))
   print("Number of edges: {}".format(s2g.graph['Graph'].number_of_edges()))
   
   
   
   # In[ ]:
   
   # ### Visualization of the embedding space
   # write_log("plot graph projection A")
   # plt.figure(figsize=(10,10))
   # plt.plot(s2g.graph['proj_A']['0'],s2g.graph['proj_A']['1'])
   # plt.title("SProj(T,l,lambda)")
   
   
   
   # In[ ]:
   
   
   # ### Visualization of the graph
   write_log("Visualization of the graph:")
   # ==> !!!! s2g.plot_graph()
   
   
   
   # In[ ]:
   
   
   # ## Anomalies detection
   write_log("Anomalies detection")
   s2g.score(query_length)
#   s2g.plot_graph()
   
   
   # In[ ]:
   
   
   ### Visualization of the full time series
   write_log("Visualization of the full time series:")
   fig,ax = plt.subplots(2,1,figsize=(20,4))
   ax[0].plot(df[0].values[0:len(s2g.all_score)])
   ax[1].plot(s2g.all_score)
   ax[0].set_xlim(0,len(s2g.all_score))
   ax[1].set_xlim(0,len(s2g.all_score))
   ax[0].title.set_text(f'G1 - {column_name}')
   plt.show()
     
   
   # In[]
   threshold = 0.8
   # min_score = min(s2g.all_score.values)
   # max_score = max(s2g.all_score.values)
   # threshold = (max_score-min_score)*.5
   # print('threshold:',min_score,max_score, threshold )
   anom_val = []
   anom_score = []
   for i in range(len(s2g.all_score)):
       if(s2g.all_score[i] > threshold):
           anom_val.append(df[0].values[i])
           anom_score.append(s2g.all_score[i])
       else: 
           anom_val.append(np.nan)
           anom_score.append(np.nan)
   len(anom_val)        

   
   # In[Plot anomalies]
   fig, ax = plt.subplots(2,1,figsize=(20,12))
   ax[0].plot(df[0].values[0:len(s2g.all_score)])
   ax[0].plot(anom_val[0:len(anom_val)],"ro")
   ax[0].title.set_text(f'G2 - {column_name}')
   ax[0].set_xlim(0,len(anom_score))

   ax[1].plot(anom_score)
   ax[1].set_xlim(0,len(anom_score))

   plt.show()
   
   # In[ ]:
   
   
   # ### Visualization of a snippet
   scale = len(s2g.all_score) // 5
   scale = len(s2g.all_score)+100
   write_log("Visualization of a snippet")
   fig, ax = plt.subplots(2,1,figsize=(20,12))
   ax[0].plot(df[0].values[:scale])
   ax[0].plot(anom_val[:scale],"ro")
   ax[0].set_xlim(0,scale)
   ax[0].title.set_text(f'G3 - {column_name}')

   ax[1].plot(anom_score)
   ax[1].set_xlim(0,len(anom_score))

   plt.show()

   return anom_val

# In[Reading data]:

write_log("read_csv file /DATA/ATM_ECG_803.ts")
dataset = 2  # select wich file to read

if dataset == 0:
   columns= ['Date','Memory']
   df = pd.read_csv('https://raw.githubusercontent.com/odedns/hackathon/4625c602ff05bc013027a677871ec31f8e66301c/SourceCode/DATA/Memory-data-2021-04-28%2017_06_58.csv',
         skiprows = 1,
         names = columns,
         delimiter = '\t',
         header=None)
   columns= ['Memory']
   measure = 'memory usage'
   
elif dataset == 1:
   columns= ['Received','Sent']
   df = pd.read_csv('https://raw.githubusercontent.com/odedns/hackathon/4625c602ff05bc013027a677871ec31f8e66301c/SourceCode/DATA/Total%20Network%20I_O%20pressure%20-data-as-seriestocolumns-2021-04-28%20%2017_08_56.csv',
     delimiter = '\t')
   measure = 'network i/o'
   
elif dataset == 2:
   columns= ['Time','CPU Usage']
   df = pd.read_excel('https://raw.githubusercontent.com/odedns/hackathon/4625c602ff05bc013027a677871ec31f8e66301c/SourceCode/DATA/CPU-data-2021-04-28%2017_03_23.xlsx',
      sheet_name=0)
   columns= ['CPU Usage']
   measure = 'CPU usage'
   
elif dataset == 3:
   df = pd.read_csv("../DATA/ATM_ECG_803.ts",header=None)[:100000]
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
print("Number of points: {}".format(len(df)))
print("Data frame: {}",df)
print("Data frame: {}",df.info())

# In[Visualize datasets]
# ### Visualization of a snippet
write_log("Visualization of dataset")
fig,ax = plt.subplots(len(columns)+1,1,figsize=(20,20))
for i in range(len(columns)):
   ax[i].title.set_text(f'{measure} - {columns[i]}')
   ax[i].plot(df[columns[i]].values)
   ax[i].set_ylim(min(df),max(df))
plt.show()

# In[compute graph for each serie]
anomal_values=pd.DataFrame([])

for i in columns:
   tmp = pd.DataFrame(df[i])
   tmp.rename(columns = {i:0}, inplace = True)
   tmp.dropna(subset = [0], inplace=True)
   anomal_values[i]=graph_one_serie(tmp, i)
   
# In[Visualize all datasets]
# ### Visualization of a snippet
write_log("Visualization of a snippet")
fig,ax = plt.subplots(len(columns)+1,1,figsize=(20,20))
for i in range(len(columns)):
   ax[i].title.set_text(f'{measure} - {columns[i]}')
   ax[i].plot(df[columns[i]].values[-len(anomal_values[columns[i]])])
   ax[i].plot(anomal_values[columns[i]],"-g")
   #ax[i].set_xlim(0,1)
plt.show()
# In[ ]:

write_log("Done!")


