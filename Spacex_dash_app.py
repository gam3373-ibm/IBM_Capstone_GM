#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install dash')
get_ipython().system('pip install dash==1.19.0!')
get_ipython().system('pip install jupyter_dash')
get_ipython().system('pip install --upgrade plotly')

import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
#import dash_core_components as dcc
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px


# In[2]:


#import pandas as pd
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#spacex_df


# In[3]:


# Create a dash application
app = dash.Dash(__name__)
#app = JupyterDash(__name__) 

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Div(
                                    dcc.Dropdown(id='site-dropdown',
                                                 options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},],
                                                 value = 'ALL',
                                                 placeholder = "Launch Sites",
                                                 searchable=True
                                                    )
                                        ),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0 Kg',
                                                    2000: '2000',
                                                    4000: '4000',
                                                    6000: '6000',
                                                    8000: '8000',
                                                    10000: '10000',},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
#@app.callback( Output(component_id='success-pie-chart', component_property='figure'), 
#                Input(component_id='site-dropdown', component_property='value'))

@app.callback(Output(component_id='success-pie-chart', component_property='figure'), 
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', names='Launch Site', title='Launch Site Success Counts')
        #return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered_df = filtered_df.groupby('class').count().reset_index()
        fig = px.pie(filtered_df,values='Unnamed: 0',names='class',title='Total Launches for site {}'.format(entered_site))
       
    return fig


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'), 
                Input(component_id="payload-slider", component_property="value")])

def get_scatter(entered_site, slider_range):

    low, high = slider_range
    slide=(spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    dropdown_scatter=spacex_df[slide]

    if entered_site == 'ALL':
        fig= px.scatter(
            dropdown_scatter, x="Payload Mass (kg)", y="class",
            color="Booster Version Category",
            hover_data=['Booster Version'],
            title="Correlation between Payload and Success for all Sites")
        return fig
    else:
        dropdown_scatter = dropdown_scatter[spacex_df['Launch Site'] == entered_site]
        title_scatter = f'Success by Payload Size for {entered_site}'
        fig=px.scatter(dropdown_scatter,x="Payload Mass (kg)", y="class", title = title_scatter, color='Booster Version Category')
        return fig


# In[ ]:


# Run the app
if __name__ == '__main__':
    app.run_server()

