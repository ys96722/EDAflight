
# coding: utf-8

# # Import Libraries

# In[85]:


# Wrangling
import pandas as pd
import numpy as np
# Plotting
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import os


# In[2]:


# Set Plotting Styles
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = 15,15


# In[3]:


from jupyterthemes import jtplot
jtplot.style(figsize=(15,15))


# # Import Datasets

# ### Original Datasets

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


# ### Modified Datasets (From Hive Code)

# In[9]:


byCarrier = pd.read_csv('generated_datasets/byCarr.csv')
byCord = pd.read_csv('generated_datasets/byCord.csv')
byModel = pd.read_csv('generated_datasets/bymodel.csv')
byManu = pd.read_csv('generated_datasets/bymyear.csv')
byState = pd.read_csv('generated_datasets/byState.csv')


# ### Subset Datasets

# In[10]:


oldCancel = oldData[oldData['Cancelled'] == 1]
newCancel = newData[newData['Cancelled'] == 1]


# # Plots

# ## Plots from 1998

# In[11]:


# Generate the Plot
sns.countplot(data=oldCancel, x='Month').set_title("Number of Cancellations by Month in 1998")
# Save the Plot
plt.savefig('Number of Cancellations by Month in 1998', dpi=100)


# ## Plots from 2006

# In[15]:


# Set Subplot Grids
f,ax=plt.subplots(1,2,figsize=(20,8))

# Generate the Plots
newCancel['CancellationCode'].value_counts().plot.pie(explode=[0.05,0.05,0.05,0.05],autopct='%1.1f%%',ax=ax[0],shadow=True)
ax[0].set_ylabel('')
sns.countplot('CancellationCode', order = newCancel['CancellationCode'].value_counts().index, data=newCancel, ax=ax[1])

# Save the Plots
plt.savefig('Distribution of Cancellation Codes')
print('A = carrier, B = weather, C = NAS, D = security')


# In[19]:


# Generate the Plot
sns.countplot(data=newCancel, x='Month', hue="CancellationCode").set_title("Number of Cancellations by Code in 2006")

# Save the Plot
plt.savefig("Number of Cancellations by Code in 2006")


# # Rate of Cancellation by Carrier

# In[21]:


# Generate the Plot
cancelRateCarrier = sns.barplot(data = byCarrier, x = 'year', y= byCarrier['num_cancl']/byCarrier['num_flight'] , 
                                        ci =None , hue = 'carrier')

# Set the Plot's title
cancelRateCarrier.set_title('Rate of Cancellation by Carrier')
# Rotate the Plot's X-axis Ticks
cancelRateCarrier.set_xticklabels(cancelRateCarrier.get_xticklabels(), 
                                          rotation=40, ha="right")
plt.tight_layout()

#Save the Plot
plt.savefig("Rate of Cancellation by Carrier")


# In[84]:


# Subset the Dataset 
cleanedManu = byManu[~((byManu.year == 1998) & (byManu.manu_year > 1998))]

# Generate Color Palette 
palette = sns.color_palette("mako_r", 2)

# Generate the Plot
delayByManuYear = sns.lineplot(data = cleanedManu, x = 'manu_year',y= 'avg_dely', 
                               hue='year', ci =None, estimator='mean', palette=palette)

# Set the Plot's Style
delayByManuYear.set_title('Mean Delay by Manufactured Year')
delayByManuYear.set_aspect(2.4)
plt.xlim(1956,2007)
delayByManuYear.legend()

# Save the Plot
plt.savefig("Mean Delay by Manufactured Year")
plt.show()


# # Map Plot for Cancellation Rate

# In[23]:


# Generate the Heatmap
plt.matshow(byManu.corr())

# Adjust Y and X labels and ticks
plt.xticks(range(len(byManu.columns)), byManu.columns)
plt.yticks(range(len(byManu.columns)), byManu.columns)

# Generate the Legend (Color Bar)
plt.colorbar()

# Save the Plot
plt.savefig("Correlation Heatmap")


# In[28]:


# Set Relative Path to the States Json File
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


# In[29]:


# Initialize the map:
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


# In[30]:


# Initialize the map:
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

