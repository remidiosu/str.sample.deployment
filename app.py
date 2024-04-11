import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import geopandas as gpd
import geoplot
import geoplot.crs as gcrs



@st.cache_data
def load_df():
    df = pd.read_excel('dashboard.xlsx')
    return df

df = load_df()
df['Date'] = df['Date'].dt.strftime('%Y/%m/%d')

s = df[df['Outcome']=='Success']
fail = df[df['Outcome']=='Failure']
to = df[df['Outcome']=='Time out']
total = df.groupby('Date')['Outcome'].count().reset_index(name='Total')
s_d = s.groupby('Date')['Outcome'].count().reset_index(name='Success')
f_d = fail.groupby('Date')['Outcome'].count().reset_index(name='Failure')
to_d = to.groupby('Date')['Outcome'].count().reset_index(name='Time out')

# merge all these tables in total
total = pd.merge(total, s_d, on='Date', how='left')
total = pd.merge(total, f_d, on='Date', how='left')
total = pd.merge(total, to_d, on='Date', how='left')
total.fillna(0, inplace=True)
total['Ratio'] = total['Success']/total['Total']


st.markdown("<h1 style='text-align: center; color: blue;'>My Dash</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: darkblue;'>Data</h4>", unsafe_allow_html=True)
st.table(df.head())
filtered_data1 = total
st.markdown("<h4 style='text-align: left; color: darkblue;'>Outcomes per date</h4>", unsafe_allow_html=True)
outcome = st.multiselect("Choose an outcome", options=['Success', 'Failure', 'Ratio', 'Total'])

if outcome:
    for item in outcome:
        if item == 'Ratio':
            plt.plot(filtered_data1['Date'], filtered_data1[item], label='Success/Total')
        else:
            plt.plot(filtered_data1['Date'], filtered_data1[item], label=item)
    plt.legend(fontsize=9)
    plt.title('A')
    plt.xticks(filtered_data1['Date'], rotation=90, ha='center', fontsize=8)
    
    st.pyplot(plt.gcf())


st.markdown("<br><br><h4 style='text-align: left; color: darkblue;'>Outcomes per State</h4>", unsafe_allow_html=True)

s_s = s.groupby('State')['Outcome'].count().reset_index(name='Success')
f_s = fail.groupby('State')['Outcome'].count().reset_index(name='Failure')
t = df.groupby('State')['Outcome'].count().reset_index(name='Total')

s_s = pd.merge(s_s, f_s, on='State', how='left')
s_s = pd.merge(s_s, t, on='State', how='left')
s_s.fillna(0, inplace=True)


col1, col2 = st.columns(2, gap='medium')
with col1:
    state = st.multiselect("Select State/s", s_s['State'])
    all_options = st.button("Select all options")

with col2:
    outcome = st.multiselect("Choose an outcome", options=['Success', 'Failure', 'Total'])

if all_options:
        state = s_s['State'].tolist()
        outcome = ['Success', 'Failure', 'Total']
        
if state and outcome:
    filtered_data1 = s_s[s_s['State'].isin(state)]
    filtered_data1.plot(x='State', y=outcome, kind='bar')
    plt.legend(fontsize=4)
    st.pyplot(plt.gcf())


st.markdown("<br><br><h4 style='text-align: left; color: darkblue;'>My Map</h4>", unsafe_allow_html=True)

data = gpd.read_file("https://github.com/open-data-kazakhstan/geo-boundaries-kz/blob/master/datapackage.geojson")
geoplot.polyplot(data, projection=gcrs.AlbersEqualArea(), edgecolor='darkgrey', facecolor='lightgrey', linewidth=.3,figsize=(12, 8))

st.pyplot(plt.gcf())

