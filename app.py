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
            dbc.Row([
                html.Img(id="image")
            ]),
            dbc.Row([
                dash_table.DataTable(
                id="table",
                columns=[
                    {"name": "Stats", "id": "Column"},
                    {"name": "GP", "id": "Value"},
                ],
                style_cell={
                'textAlign': 'center',
                'padding': '5px',
                'backgroundColor': '#222222',  # set background color of cell
                'color': 'white',  # set text color of cell
                'font-size': '16px',  # set font size of cell
                },
                style_header={
                    'backgroundColor': '#333333',  # set background color of header
                    'fontWeight': 'bold',  # set font weight of header
                    'color': 'white',  # set text color of header
                    'font-size': '20px',  # set font size of header
                },
                style_table={
                    "width": "100%",
                    "height": "400px",
                    "overflowY": "auto",
                },
                fill_width=False,
                # className="table-striped table-hover table-bordered"
                )
            ]),
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
                        "zoom": 1,
                    },
                    "margin": {"l": 0, "r": 0, "t": 0, "b": 0},
                    "height": 600,
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
        {"Column": "Country", "Value": row["Country"]},
        {"Column": "City", "Value": row["City"]},
        {"Column": "Grand Prix Name", "Value": row["GP Name"]},
        {"Column": "Round", "Value": row["Round"]},
        {"Column": "Race Date", "Value": row["Race Date"]},
        {"Column": "Number of Laps", "Value": row["Number of Laps"]},
        {"Column": "Circuit Length(km)", "Value": row["Circuit Length(km)"]},
        {"Column": "Race Distance(km)", "Value": row["Race Distance(km)"]},
        {"Column": "Turns", "Value": row["Turns"]},
        {"Column": "DRS Zones", "Value": row["DRS Zones"]},
        {"Column": "Year of First GP", "Value": row["First GP"]},
    ]
    return data

# Define callback to update image
@app.callback(
    dash.dependencies.Output("image", "src"),
    dash.dependencies.Input("map", "clickData"),
)

def update_image(click_data):
    if not click_data:
        return ""
    point_index = click_data["points"][0]["pointNumber"]
    row = df.iloc[point_index]
    image_path = os.path.join("assets", f"{row['GP Name']}.png")
    return image_path if os.path.exists(image_path) else ""

if __name__ == "__main__":
    app.run_server(debug=True)