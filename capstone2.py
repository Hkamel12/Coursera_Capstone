#!/usr/bin/env python
# coding: utf-8

# In[26]:



import pandas as pd # library for data analsysis

import json # library to handle JSON files

import requests # library to handle requests

from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe

import matplotlib.cm as cm
import matplotlib.colors as colors # Matplotlib and associated plotting modules

from sklearn.cluster import KMeans # import k-means from clustering stage

get_ipython().system('conda install -c conda-forge beautifulsoup4 --yes')
from bs4 import BeautifulSoup # website scraping libraries and packages in Python from BeautifulSoup 

get_ipython().system('conda install -c conda-forge geopy --yes')
from geopy.geocoders import Nominatim  # convert an address into latitude and longitude values

print("Libraries imported.")


# In[ ]:



from pandas.io.json import json_normalize 


# In[ ]:


data = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M').text


# In[ ]:


soup = BeautifulSoup(data, 'html.parser')


# In[27]:



postalCodeList = []
boroughList = []
neighborhoodList = []


# In[28]:


soup.find('table').find_all('tr')

# find all the rows of the table
soup.find('table').find_all('tr')

# for each row of the table, find all the table data
for row in soup.find('table').find_all('tr'):
    cells = row.find_all('td')


# In[29]:



for row in soup.find('table').find_all('tr'):
    cells = row.find_all('td')
    if(len(cells) > 0):
        postalCodeList.append(cells[0].text)
        boroughList.append(cells[1].text)
        neighborhoodList.append(cells[2].text.rstrip('\n'))


# In[30]:


toronto_df = pd.DataFrame({"PostalCode": postalCodeList,
                           "Borough": boroughList,
                           "Neighborhood": neighborhoodList})

toronto_df.head()


# In[31]:



toronto_df_drop = toronto_df[toronto_df.Borough != "Not assigned"].reset_index(drop=True)
toronto_df_drop.head()


# In[32]:



toronto_df_grouped = toronto_df_drop.groupby(["PostalCode", "Borough"], as_index=False).agg(lambda x: ", ".join(x))
toronto_df_grouped.head()


# In[33]:



for index, row in toronto_df_grouped.iterrows():
    if row["Neighborhood"] == "Not assigned":
        row["Neighborhood"] = row["Borough"]
        
toronto_df_grouped.head()


# In[34]:


column_names = ["PostalCode", "Borough", "Neighborhood"]
test_df = pd.DataFrame(columns=column_names)

test_list = ["M5G", "M2H", "M4B", "M1J", "M4G", "M4M", "M1R", "M9V", "M9L", "M5V", "M1B", "M5A"]

for postcode in test_list:
    test_df = test_df.append(toronto_df_grouped[toronto_df_grouped["PostalCode"]==postcode], ignore_index=True)
    
test_df


# In[ ]:




