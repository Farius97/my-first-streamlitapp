# Streamlit live coding script
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy


 #heißt Decorator, das @ vor der Funktion bestimmt das
@st.cache_data   #packt die sachen die aus der Funktion kommen in den Cache
def load_data(path):
    df = pd.read_csv(path)
    return df

mpg_df_raw = load_data(path='./data/mpg.csv')
mpg_df = deepcopy(mpg_df_raw) # Sachen im Cache können nicht geändert werden, deswegen copy

#mpg_df = pd.read_csv("./data/mpg.csv")

st.title("Introduction to Streamlit")
st.header('MPG Data Exploration')

#if st.checkbox('Show DataFrame'):       # Checkbox in der Mitte
if st.sidebar.checkbox('Show DataFrame'): # Checkbox an der Seite
    st.subheader('Now this is shown')
    #st.table(data=mpg_df)
    st.dataframe(data=mpg_df)
else:
    st.subheader('Now it isnt')

st.sidebar.checkbox('This is a checkbox!')

years = ['All'] + sorted(pd.unique(mpg_df['year']))

# left_column, right_column = st.columns(2) # Columns erstellen
left_column, middle_column, right_column = st.columns([3,1,1]) # die liste sind der Anteil
# left_column belegt 3/5 der plätze gerade


#year = st.selectbox('Choose a year' , years)  # So belegt das den ganzen Platz von links nach rechts
year = left_column.selectbox('Choose a year' , years) # Variable year = Wert der in der Liste ausgewählt wird

if year == 'All':
    reduced_df = mpg_df
else:
    reduced_df = mpg_df[mpg_df['year']==year]

means = reduced_df.groupby('class').mean(numeric_only=True)

show_means = middle_column.radio(label='Show Means', options=['Yes','No'])
st.subheader(show_means)

plot_type = right_column.radio('Choose Plot type', options= ['Matplotlib','plotly'])


m_fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(reduced_df['displ'], reduced_df['hwy'], alpha=0.7)
ax.set_title("Engine Size vs. Highway Fuel Mileage")
ax.set_xlabel('Displacement (Liters)')
ax.set_ylabel('MPG')

if show_means == 'Yes':
    ax.scatter(means['displ'],means['hwy'], alpha = 0.7, color = 'red', label = 'Class Means')

#st.pyplot(m_fig) # plot erstellen


# plotly

p_fig = px.scatter(reduced_df, x='displ', y='hwy', opacity=0.5,
                   range_x=[1, 8], range_y=[10, 50],
                   width=750, height=600,
                   labels={"displ": "Displacement (Liters)",
                           "hwy": "MPG"},
                   title="Engine Size vs. Highway Fuel Mileage")
p_fig.update_layout(title_font_size=22)

if show_means == "Yes":
    p_fig.add_trace(go.Scatter(x=means['displ'], y=means['hwy'],
                               mode="markers"))
    p_fig.update_layout(showlegend=False)

#st.plotly_chart(p_fig)

if plot_type == 'Matplotlib':
    st.pyplot(m_fig)
else:
    st.plotly_chart(p_fig)

# Sample streamlit map
st.subheader('Streamlit Map')
ds_geo = px.data.carshare()

ds_geo['lat'] = ds_geo['centroid_lat']
ds_geo['lon'] = ds_geo['centroid_lon']

st.map(ds_geo)