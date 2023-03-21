from dash import Dash, dcc, html, dash_table, dbc
from dash.dependencies import Input, State, Output
# import dash_bootstrap_components as dbc
import pandas as pd
import os

# Load data
data1 = pd.read_csv("https://raw.githubusercontent.com/toUpperCase78/formula1-datasets/master/Formula1_2022season_calendar.csv")
data2 = pd.read_csv("data/circuits.csv").rename(columns={"name": "Circuit Name"})
df = pd.merge(data1, data2)

# Create app
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
app.title = "F1 Dash"
app._favicon = (os.path.join('image', 'f1.ico'))

# Create server
server = app.server

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
                html.Img(id="image", style={
                    'width':'60%',
                    })
            ], justify="center"),
            dbc.Row([
                dash_table.DataTable(
                id="table",
                columns=[
                    {"name": "Stats", "id": "Column"},
                    {"name": "GP", "id": "Value"},
                ],
                style_cell={
                'textAlign': 'left',
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
            ], justify="center"),
        ], width=4,style={'border': '1px solid #d3d3d3', 'border-radius': '10px'}, align='center'),
        
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

# Define callback to update table
@app.callback(
    Output("table", "data"),
    Input("map", "clickData"),
)

def update_table(click_data):
    if not click_data:
        row = df.iloc[0]
    else:
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
                "hoverinfo": "none",
            }
        )
    else:
        # remove lines from the map
        fig["data"] = fig["data"][:1]
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)