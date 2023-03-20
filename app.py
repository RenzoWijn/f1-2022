import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_table
import os

# Load data
data1 = pd.read_csv("https://raw.githubusercontent.com/toUpperCase78/formula1-datasets/master/Formula1_2022season_calendar.csv")
data2 = pd.read_csv("data/circuits.csv").rename(columns={"name": "Circuit Name"})
df = pd.merge(data1, data2)

# Create app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
app.title = "F1 Dash"
app._favicon = (os.path.join('image', 'f1.ico'))

# Define layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("The Formula 1 2022 Season, Visualised", style={'textAlign': 'center'})
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
            id="table",
            columns=[
                {"name": "Column", "id": "Column"},
                {"name": "Value", "id": "Value"},
            ],
            style_cell={
                "textAlign": "center",
                "padding": "5px",
            },
            style_table={
                "width": "100%",
                "height": "800px",
                "overflowY": "auto",
            },
            fill_width=False,
            cell_selectable=False
        ),
        ], width=4),
        
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
                        "zoom": 2,
                    },
                    "margin": {"l": 0, "r": 0, "t": 0, "b": 0},
                    "height": 400,
                },
            },
        ),
        ], width=8)
    ]),
    
])

# Define callback to update table
@app.callback(
    dash.dependencies.Output("table", "data"),
    dash.dependencies.Input("map", "clickData"),
)
def update_table(click_data):
    if not click_data:
        return []
    point_index = click_data["points"][0]["pointNumber"]
    row = df.iloc[point_index]
    data = [
        {"Column": "Round", "Value": row["Round"]},
        {"Column": "Race Date", "Value": row["Race Date"]},
        {"Column": "Grand Prix Name", "Value": row["GP Name"]},
        {"Column": "Country", "Value": row["Country"]},
        {"Column": "City", "Value": row["City"]},
        {"Column": "Number of Laps", "Value": row["Number of Laps"]},
        {"Column": "Circuit Length(km)", "Value": row["Circuit Length(km)"]},
        {"Column": "Race Distance(km)", "Value": row["Race Distance(km)"]},
        {"Column": "Turns", "Value": row["Turns"]},
        {"Column": "DRS Zones", "Value": row["DRS Zones"]},
        {"Column": "Year of First GP", "Value": row["First GP"]},
    ]
    return data

if __name__ == "__main__":
    app.run_server(debug=True)