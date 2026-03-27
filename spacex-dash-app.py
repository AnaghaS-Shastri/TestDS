# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read dataset
spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create app
app = dash.Dash(__name__)

# Get unique launch sites
sites = spacex_df['Launch Site'].unique()

# App layout
app.layout = html.Div(children=[
    
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # ✅ TASK 1: Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] +
                [{'label': site, 'value': site} for site in sites],
        value='ALL',
        placeholder="Select Launch Site",
        searchable=True
    ),
    
    html.Br(),
    
    # ✅ Pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),
    
    html.Br(),
    
    html.P("Payload range (Kg):"),
    
    # ✅ TASK 3: Range Slider
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: str(i) for i in range(0, 10001, 2000)},
        value=[min_payload, max_payload]
    ),
    
    html.Br(),
    
    # ✅ Scatter plot
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# =========================
# ✅ TASK 2: PIE CHART
# =========================
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie(selected_site):
    
    if selected_site == 'ALL':
        fig = px.pie(
            spacex_df,
            names='Launch Site',
            values='class',
            title='Total Success Launches by Site'
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Success vs Failure for {selected_site}'
        )
    
    return fig


# =========================
# ✅ TASK 4: SCATTER
# =========================
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter(selected_site, payload_range):
    
    low, high = payload_range
    
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]
    
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
    
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload vs Launch Outcome'
    )
    
    return fig


# Run app
if __name__ == '__main__':
    app.run(debug=True)