from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, State, Output
import dash_bootstrap_components as dbc
import pandas as pd
import os

# Load data
data1 = pd.read_csv("data/2023Calendar.csv")
data2 = pd.read_csv("data/circuits.csv").rename(columns={"name": "Circuit Name"})
df = pd.merge(data1, data2)
columns = [
    "Country", 
    "City", 
    "GP Name", 
    "Round", 
    "Race Date", 
    "Number of Laps", 
    "Circuit Length(km)", 
    "Race Distance(km)", 
    "Turns", 
    "DRS Zones", 
    "First GP"
]

# Create app
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
app.title = "F1 2022 Calendar"

# Create server
server = app.server

# Define layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1([
                "The", 
                html.Span(" Formula 1 ", style={'color': 'red', "font-style": "italic"}), 
                "2023 Season Calendar"
                ], 
                style={
                    'textAlign': 'center', 
                    'color': 'white'
                }
            )
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Row([
                html.H2(id="track_name", style={'text-align': 'center'})
            ]),
            dbc.Row([
                html.Img(id="image", style={'width':'60%'})
            ], justify="center"),
            dbc.Row([
                html.Table(id='table', style = {'text-align': 'center'})
            ], justify="center"),
        ], 
        width=4,
        style={'border': '1px solid #d3d3d3', 'border-radius': '10px'}, align='center'),
        
        dbc.Col([
            dcc.Graph(
                id="map",
                figure={
                    "data": [
                        {
                            "type": "scattermapbox",
                            "lat": df["lat"],
                            "lon": df["lng"],
                            "mode": "markers",
                            "marker": {"size": 10},
                            "hovertemplate": "%{text}<extra></extra>",
                            "text": df["Circuit Name"],
                        }
                    ],
                    "layout": {
                        "mapbox": {
                            "style": "carto-darkmatter",
                            "center": {"lat": df["lat"].mean(), "lon": df["lng"].mean()},
                            "zoom": 1,
                        },
                        "margin": {"l": 0, "r": 0, "t": 0, "b": 0},
                        "height": 600,
                        "showlegend": False
                    },
                },
            ),
            dcc.RadioItems(
                id="toggle-lines",
                options=[
                    {"label": "Show Route", "value": "on"},
                    {"label": "Hide Route", "value": "off"},
                ],
                value="off",
                labelStyle={"display": "inline-block", "margin-right": "20px"},
            ),
        ], width=8)
    ]),
])


# Track title
@app.callback(
    Output('track_name', 'children'),
    Input('map', 'clickData')
)
def update_title(clickData):
    if clickData is None:
        selected_row = df.iloc[0]
    else:
        point_index = clickData['points'][0]['pointNumber']
        selected_row = df.iloc[point_index]
    return selected_row["Circuit Name"]

# Table contents
@app.callback(
    Output('table', 'children'),
    Input('map', 'clickData')
)
def update_table(clickData):
    if clickData is None:
        selected_row = pd.DataFrame(df.iloc[0])
    else:
        point_index = clickData['points'][0]['pointNumber']
        selected_row = pd.DataFrame(df.iloc[point_index])
    rows = [html.Tr([html.Td([i], style={'border': '1px solid'})] + [html.Td(selected_row.loc[i], style={'border': '1px solid'})], style={'border': '1px solid black'}) for i in columns]
    return  rows

# Track layout
@app.callback(
    Output("image", "src"),
    Input("map", "clickData"),
)
def update_image(click_data):
    if not click_data:
        return os.path.join("assets", f"{df.iloc[0]['GP Name']}.png")
    point_index = click_data["points"][0]["pointNumber"]
    row = df.iloc[point_index]
    image_path = os.path.join("assets", f"{row['GP Name']}.png")
    return image_path if os.path.exists(image_path) else ""

# Toggle route
@app.callback(
    Output("map", "figure"),
    Input("toggle-lines", "value"),
    State("map", "figure"),
)
def toggle_lines(value, fig):
    if value == "on":
        # add lines to the map
        fig["data"].append(
            {
                "type": "scattermapbox",
                "lat": df["lat"],
                "lon": df["lng"],
                "mode": "lines",
                "line": {"width": 2, "color": "red"},
                "hovertemplate": "%{text}<extra></extra>",
                "text": df["Round"]
            }
        )
    else:
        # remove lines from the map
        fig["data"] = fig["data"][:1]
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)