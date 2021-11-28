# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

unique_launch_sites = spacex_df['Launch Site'].unique().tolist()
launch_sites = []
launch_sites.append({'label': 'All Sites', 'value': 'All Sites'})
for launch_site in unique_launch_sites:
    launch_sites.append({'label': launch_site, 'value': launch_site})

marks_dict = {}
for i in range(0,11000,1000):
    marks_dict[i] = {'label': str(i)+' Kg'}

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(
                                    id = 'site-dropdown',
                                    options = launch_sites,
                                    placeholder = 'Select a Launch Site',
                                    searchable = True ,
                                    value = 'All Sites'
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div([
                                    dcc.RangeSlider(
                                        id = 'payload_slider',
                                        min = 0,
                                        max = 10000,
                                        step = 1000,
                                        marks = marks_dict,
                                        value = [min_payload, max_payload]
                                    ),
                                ], style={'padding': '40px 30px'}),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
     Output(component_id = 'success-pie-chart', component_property = 'figure'),
     [Input(component_id = 'site-dropdown', component_property = 'value')]
)
def piegraph_update(site_dropdown):
    if site_dropdown == 'All Sites' or site_dropdown == 'None':
        data  = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(
                data,
                names = 'Launch Site',
                title = 'Total Success Launches by Site'
            )
    else:
        data = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        fig = px.pie(
                data,
                names = 'class',
                title = 'Total Success Launches for Site ' + site_dropdown,
            )
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
     Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
     [Input(component_id = 'site-dropdown', component_property = 'value'), 
     Input(component_id = "payload_slider", component_property = "value")]
)
def scattergraph_update(site_dropdown, payload_slider):
    low, high = payload_slider
    if (site_dropdown == 'All Sites' or site_dropdown == 'None'):
        print(payload_slider)
        low, high = payload_slider
        data = spacex_df[spacex_df['Payload Mass (kg)'].between(low, high)]
        fig = px.scatter(
                data, 
                x = "Payload Mass (kg)", 
                y = "class",
                title = 'Correlation between Payload and Success for all Sites',
                color = "Booster Version Category"
            )
    else:
        print(payload_slider)
        low, high = payload_slider
        data = spacex_df[spacex_df['Payload Mass (kg)'].between(low, high)]
        data_filtered = data[data['Launch Site'] == site_dropdown]
        fig = px.scatter(
                data_filtered,
                x = "Payload Mass (kg)",
                y = "class",
                title = 'Correlation between Payload and Success for site '+ site_dropdown,
                color = "Booster Version Category"
            )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
