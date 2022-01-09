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

launch_sites = spacex_df['Launch Site'].unique()
options = [{"label": "All Sites", "value": "ALL"}]
for index, site in enumerate(launch_sites):
    options.append(dict({"label": site, "value" : site}))

#filtered_df = spacex_df.loc[(spacex_df['Payload Mass (kg)'] >= 0) & (spacex_df['Payload Mass (kg)'] <= 1000)]
#import sys
#sys.exit()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                # dcc.Dropdown(id='site-dropdown',
                                #    options=[
                                #        {'label': 'All Sites', 'value': 'ALL'},
                                #        {'label': 'site1', 'value': 'site1'},
                                #    ],
                                #    value='ALL',
                                #    placeholder="place holder here",
                                #    searchable=True
                                #    ),
                                
                                dcc.Dropdown(id='site-dropdown',
                                    options=options,
                                    value="ALL",
                                    placeholder="Select a Launch Site here",
                                    searchable=True),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                    min=min_payload, max=max_payload, step=(max_payload-min_payload)/4,
                                    marks={int(min_payload): str(min_payload),
                                        int((max_payload-min_payload)*25/100): str((max_payload-min_payload)*25/100),
                                        int((max_payload-min_payload)*50/100): str((max_payload-min_payload)*50/100),
                                        int((max_payload-min_payload)*75/100): str((max_payload-min_payload)*75/100),
                                        int(max_payload): str(max_payload)},
                                    value=[min_payload, max_payload]),
                                #dcc.RangeSlider(id='payload-slider',
                                #    min=min_payload,
                                #    max=max_payload,
                                #    step=max_payload/4,
                                #    value=[min_payload, max_payload]
                                #    ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
            names='Launch Site', 
            title='Total Success Launches by Sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, #values='class', 
            names='class', 
            title='Total Success by ' + entered_site)
        return fig
        
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, entered_payload):
    
    filtered_df = spacex_df.loc[(spacex_df['Payload Mass (kg)'] >= entered_payload[0]) & (spacex_df['Payload Mass (kg)'] <= entered_payload[1])]

    if entered_site == 'ALL':
        fig=px.scatter(data_frame=filtered_df, 
                x="Payload Mass (kg)", 
                y="class",
                color="Booster Version Category",
                title=str(entered_payload) + ":" + str(filtered_df.shape))
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig=px.scatter(data_frame=filtered_df, 
                x="Payload Mass (kg)", 
                y="class",
                color="Booster Version Category")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
