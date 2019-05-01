
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import os


# In[2]:


sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = 15,15


# In[3]:


from jupyterthemes import jtplot
jtplot.style(figsize=(15,15))


# # Import

# In[4]:


airports = pd.read_csv('original_datasets/airports.csv')


# In[5]:


carriers = pd.read_csv('original_datasets/carriers.csv')


# In[6]:


planes = pd.read_csv('original_datasets/plane-data.csv')


# In[7]:


oldData = pd.read_csv('original_datasets/1998.csv')


# In[8]:


newData = pd.read_csv('original_datasets/2006.csv')


# In[9]:


byCarrier = pd.read_csv('generated_datasets/byCarr.csv')
byCord = pd.read_csv('generated_datasets/byCord.csv')
byModel = pd.read_csv('generated_datasets/bymodel.csv')
byManu = pd.read_csv('generated_datasets/bymyear.csv')
byState = pd.read_csv('generated_datasets/byState.csv')


# # Wrangling

# In[10]:


oldCancel = oldData[oldData['Cancelled'] == 1]
newCancel = newData[newData['Cancelled'] == 1]


# # Plots

# ## 1998

# In[ ]:


sns.countplot(data=oldCancel, x='Month').set_title("Number of Cancellations by Month in 1998")
plt.savefig('Number of Cancellations by Month in 1998', dpi=100)


# In[ ]:


sns.countplot(data=oldCancel, x='DayofMonth').set_title("Count of Cancellations by Date in 1998")


# In[ ]:


sns.countplot(data=oldCancel, x='DayOfWeek').set_title("Count of Cancellations by Day in 1998")


# In[ ]:


sns.countplot(data=oldCancel, x='UniqueCarrier')


# ## 2006

# In[ ]:


f,ax=plt.subplots(1,2,figsize=(20,8))

newCancel['CancellationCode'].value_counts().plot.pie(explode=[0.05,0.05,0.05,0.05],autopct='%1.1f%%',ax=ax[0],shadow=True)
ax[0].set_ylabel('')
sns.countplot('CancellationCode', order = newCancel['CancellationCode'].value_counts().index, data=newCancel, ax=ax[1])
plt.savefig('Distribution of Cancellation Codes')
print('A = carrier, B = weather, C = NAS, D = security')


# In[ ]:


sns.countplot(data=newCancel, x='Month').set_title("Count of Cancellations in 2006")
plt.show()


# In[ ]:


sns.countplot(data=newCancel, x='DayofMonth').set_title("Count of Cancellations by Date in 2006")


# In[ ]:


sns.countplot(data=newCancel, x='DayOfWeek').set_title("Count of Cancellations by Day in 2006")


# In[ ]:


sns.countplot(data=newCancel, x='Month', hue="CancellationCode").set_title("Number of Cancellations by Code in 2006")
plt.savefig("Number of Cancellations by Code in 2006")


# In[ ]:


sns.countplot(data=newCancel, x='UniqueCarrier')


# # Rate of Cancellation by Carrier

# In[ ]:


cancelRateCarrier = sns.barplot(data = byCarrier, x = 'year', y= byCarrier['num_cancl']/byCarrier['num_flight'] , 
                                        ci =None , hue = 'carrier')
cancelRateCarrier.set_title('Rate of Cancellation by Carrier')
cancelRateCarrier.set_xticklabels(cancelRateCarrier.get_xticklabels(), 
                                          rotation=40, ha="right")
plt.tight_layout()
plt.savefig("Rate of Cancellation by Carrier")


# In[ ]:


palette = sns.color_palette("mako_r", 2)
delayByManuYear = sns.lineplot(data = byManu, x = 'manu_year',y= 'avg_dely', 
                               hue='year', ci =None, palette=palette)
delayByManuYear.set_title('Mean Delay by Manufactured Year')
delayByManuYear.set_aspect(2.4)
# plt.axvline(1997, 0, color='r', linestyle='--', lw=2, label="IMF Crisis")
# plt.axvline(2002, 0, color='w', linestyle='--', lw=2, label="2002 World Cup")
# plt.axvline(2008, 0, color='b', linestyle='--', lw=2, label="Global Financial Crisis")
# plt.axvline(2014, 0, color='y', linestyle='--', lw=2, label="Sinking of Sewol Ship")
plt.xlim(1956,2007)
delayByManuYear.legend({'1996': 'red', '2008': 'blue'})
plt.savefig("Mean Delay by Manufactured Year")
plt.show()


# # Map Plot for Cancellation Rate

# In[ ]:


plt.matshow(byManu.corr())
plt.xticks(range(len(byManu.columns)), byManu.columns)
plt.yticks(range(len(byManu.columns)), byManu.columns)
plt.colorbar()
plt.savefig("Correlation Heatmap")


# In[ ]:


faster = newData[['CRSElapsedTime','ActualElapsedTime','DepDelay','ArrDelay']].dropna()


# In[ ]:


faster['TimeAir'] = faster['ActualElapsedTime'] - faster['CRSElapsedTime']
faster['DelayDiff'] = faster['ArrDelay'] - faster['DepDelay']


# In[ ]:


# relationPlot = sns.scatterplot(data = faster, 
#                       x = 'DelayDiff',
#                       y= 'TimeAir', 
#                       ci =None)
# relationPlot.set_title('Delay Difference vs Flight Time Difference')
# plt.show()


# In[ ]:


# fasterPlot = sns.scatterplot(data = faster, 
#                       x = 'DepDelay',
#                       y= faster['CRSElapsedTime'] - faster['ActualElapsedTime'], 
#                       ci =None)
# fasterPlot.set_title('Departure Delay versus Flight Time')
# plt.show()


# In[ ]:


state_geo = os.path.join('generated_datasets/', 'us-states.json')
 
# Initialize the map:
rateCancellationMap = folium.Map(location=[37, -102], zoom_start=5)
 
# Add the color for the chloropleth:
rateCancellationMap.choropleth(
 geo_data=state_geo,
 name='choropleth',
 data=byState,
 columns=['state', 'r_cancl'],
 key_on='feature.id',
 fill_color='YlGn',
 fill_opacity=0.7,
 line_opacity=0.2,
 legend_name='Cancellation Rate (%)'
)
folium.LayerControl().add_to(rateCancellationMap)
 
# Save to html
rateCancellationMap.save('rateCancellationMap.html')


# In[ ]:


rateDelayMap = folium.Map(location=[37, -102], zoom_start=5)
 
# Add the color for the chloropleth:
rateDelayMap.choropleth(
 geo_data=state_geo,
 name='choropleth',
 data=byState,
 columns=['state', 'r_dely'],
 key_on='feature.id',
 fill_color='YlGn',
 fill_opacity=0.7,
 line_opacity=0.2,
 legend_name='Delay Rate (%)'
)
folium.LayerControl().add_to(rateDelayMap)
 
# Save to html
rateDelayMap.save('rateDelayMap.html')


# In[ ]:


numFlightMap = folium.Map(location=[37, -102], zoom_start=5)
 
# Add the color for the chloropleth:
numFlightMap.choropleth(
 geo_data=state_geo,
 name='choropleth',
 data=byState,
 columns=['state', 'num_flight'],
 key_on='feature.id',
 fill_color='YlGn',
 fill_opacity=0.7,
 line_opacity=0.2,
 legend_name='Number of Flights'
)
folium.LayerControl().add_to(numFlightMap)
 
# Save to html
numFlightMap.save('numFlightMap.html')

