import globals
import query
import draw
import ml
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from math import *

#
# Définition de l'application
#

tab_style = {
    "background-color": "#303840",
    "display": "inline-block",
    'color': '#AAAAAA',
    'border': '2px solid grey',
    'border-radius': '4px',
    'align-items': 'center',
    'justify-content': 'center',
    "text-align": "center",
    "margin-left": "2px",
    "margin-right": "2px",
    "margin-top": "8px",
    "margin-bottom": "8px",
}

tab_selected_style = {
    "background-color": "#485460",
    "display": "inline-block",
    'color': '#FFFFFF',
    'border': '2px solid grey',
    'border-radius': '4px',
    'align-items': 'center',
    'justify-content': 'center',
    "text-align": "center",
    "margin-left": "2px",
    "margin-right": "2px",
    "margin-top": "8px",
    "margin-bottom": "8px",
}

app = dash.Dash(__name__, title="Astéroïdes", external_stylesheets=[dbc.themes.SLATE])
server = app.server
app.layout =\
html.Div([
    html.Div([
        html.H1(
            children='Astéroïdes',
            style={"color": "#fff", 'textAlign': 'center'}
        ),
        dcc.Tabs(id="tabs", value="tab-1", children=[
            dcc.Tab(id="tab-1", label="Système Solaire Interactif", children=[
                html.Table([
                    html.Tbody([
                        html.Tr([
                            html.Td([
                                html.Table([
                                    html.Tbody([
                                        html.Tr([
                                            html.Td([
                                                html.P("Informations des astéroïdes", style={"font-weight": 'bold'}),
                                                html.Table([
                                                    html.Tbody([
                                                        html.Tr([
                                                            html.Td([
                                                                draw.get_checkbox("diameter", "Diamètre", True),
                                                                draw.get_checkbox("semi_major_axis", "Demi grand-axe", False),
                                                                draw.get_checkbox("eccentricity", "Excentricité", False),
                                                                draw.get_checkbox("inclination", "Inclinaison", False),
                                                            ]),
                                                            html.Td([
                                                                draw.get_checkbox("longitude_ascending_node", "Long. noeud asc.", False),
                                                                draw.get_checkbox("argument_perihelion", "Arg. du périastre", False),
                                                                draw.get_checkbox("mean_anomaly", "Anomalie moy.", False),
                                                                draw.get_checkbox("dist", "Distances", False),
                                                            ]),
                                                        ]),
                                                    ]),
                                                ], style={"width": "100%", "table-layout": "fixed"}),
                                            ]),
                                            html.Td([
                                                html.P("Affichage des planètes", style={"font-weight": 'bold'}),
                                                html.Table([
                                                    html.Tbody([
                                                        html.Tr([
                                                            html.Td([
                                                                draw.get_checkbox("Mercure", "Mercure", True),
                                                                draw.get_checkbox("Venus", "Venus", True),
                                                                draw.get_checkbox("Terre", "Terre", True),
                                                                draw.get_checkbox("Mars", "Mars", True),
                                                            ]),
                                                            html.Td([
                                                                draw.get_checkbox("Jupiter", "Jupiter", True),
                                                                draw.get_checkbox("Saturne", "Saturne", True),
                                                                draw.get_checkbox("Uranus", "Uranus", True),
                                                                draw.get_checkbox("Neptune", "Neptune", True),
                                                            ]),
                                                        ]),
                                                    ]),
                                                ], style={"width": "100%", "table-layout": "fixed"}),
                                            ]),
                                        ]),
                                    ]),
                                ], style={"width": "100%", "table-layout": "fixed"}),
                                html.P("Distance d'affichage", style={"font-weight": 'bold'}),
                                html.Div(children=[
                                    dcc.Slider(
                                        id='slider_bounds',
                                        min=-10,
                                        max=70,
                                        step=1,
                                        value=40,
                                        marks={
                                            (40 * log10((1.1 * sqrt(planet["x"][0] ** 2 + planet["y"][0] ** 2 + planet["z"][0] ** 2)) / 100000000)): {
                                                'label' : planet["name"],
                                                'style': {
                                                    "white-space": "nowrap",
                                                    "font-weight": 'bold',
                                                    "font-size": 10
                                                }
                                            } for planet in query.get_planets()
                                        },
                                    ),
                                ]),
                                html.P("Position des astéroïdes", style={"font-weight": 'bold'}),
                                html.Div(children=[
                                    dcc.RangeSlider(
                                        id='rslider_distance',
                                        min=-10,
                                        max=70,
                                        step=1,
                                        value=[-10, 70],
                                        marks={
                                            (40 * log10((1.1 * sqrt(planet["x"][0] ** 2 + planet["y"][0] ** 2 + planet["z"][0] ** 2)) / 100000000)): {
                                                'label' : planet["name"],
                                                'style': {
                                                    "white-space": "nowrap",
                                                    "font-weight": 'bold',
                                                    "font-size": 10
                                                }
                                            } for planet in query.get_planets()
                                        },
                                    ),
                                ]),
                                html.P("Diamètre des astéroïdes", style={"font-weight": 'bold'}),
                                html.Div(children=[
                                    dcc.RangeSlider(
                                        id='rslider_diameter',
                                        min=0,
                                        max=200,
                                        step=1,
                                        value=[0, 200],
                                        marks={ x * 25: str(x * 25) for x in range((200 // 25) + 1) },
                                    ),
                                ]),
                                html.P("Taille d'affichage des astéroïdes", style={"font-weight": 'bold'}),
                                html.Div(children=[
                                    dcc.Slider(
                                        id='slider_asteroid_size',
                                        min=1,
                                        max=10,
                                        step=0.01,
                                        value=5,
                                        marks={
                                            1: {'label' : "-", 'style': {"font-weight": 'bold', "font-size": 14}},
                                            5: "",
                                            10: {'label' : "+", 'style': {"font-weight": 'bold', "font-size": 14}},
                                        },
                                    ),
                                ]),
                                html.P("Nombre maximal d'astéroïdes", style={"font-weight": 'bold'}),
                                html.Div(children=[
                                    dcc.Input(
                                        id="input_num_asteroids",
                                        type="number",
                                        min=0,
                                        max=100000,
                                        value=1000,
                                    ),
                                    html.Button('Afficher', id='button_display', n_clicks=0),
                                ]),
                                html.Div(children=[
                                    html.P(
                                        id="info_num_asteroids",
                                        children="Nombre d'astéroïdes affichés : 1000",
                                        style={"font-family": "monospace", "color": "#bbb"}
                                    ),
                                ]),
                            ], style={"width": "33%"}),
                            html.Td([
                                dcc.Graph(
                                    id='planetary_system',
                                    figure=draw.get_planetary_system(),
                                    style={'width': '100%', 'height': '100%'}
                                ),
                            ], style={"width": "67%", "height": "85vh"}),
                        ]),
                    ]),
                ], style={"height": "85vh"}),
            ], style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(id="tab-2", label="Modèle de Prédiction du Diamètre et de la Trajectoire", children=[
                html.Table([
                    html.Tbody([
                        *[
                            draw.get_slider(k, v["name"], v["min"], v["max"], v["step"])
                            for k, v in globals.ml_features.items() if v["type"] == "slider"
                        ],
                        *[
                            draw.get_dropdown(k, v["name"], v["values"], v["value"])
                            for k, v in globals.ml_features.items() if v["type"] == "dropdown"
                        ],
                        html.Tr([
                            html.Td([], style={"width": "30%"}),
                            html.Td([
                                html.Button('Prédire', id='button_predict', n_clicks=0),
                                html.Button('Visualiser', id='button_view', n_clicks=0),
                            ], style={"width": "70%"}),
                        ])
                    ]),
                ], style={"width": "100%"}),
                html.Table([
                    html.Tbody([
                        html.Tr([
                            html.Td([
                                html.P("Diamètre prédit", style={"font-weight": 'bold'}),
                            ], style={"width": "30%"}),
                        html.Td([
                                html.H5(id="predicted_diameter", children=["-"]),
                            ], style={"width": "70%", "color": "#ccc", "font-family": "monospace", "font-weight": 'bold'}),
                        ]),
                        html.Tr([
                            html.Td([
                                html.P("Trajectoire prédite", style={"font-weight": 'bold'}),
                            ], style={"width": "30%"}),
                            html.Td([
                                html.Table([
                                    html.Tbody([
                                        html.Tr([
                                            html.Td([
                                                html.H5(id="predicted_trajectory", children=["-"]),
                                            ], style={"width": "300px"}),
                                            html.Td([
                                                html.Div([
                                                    dcc.Slider(
                                                        id='slider_predicted_trajectory',
                                                        min=0,
                                                        max=180,
                                                        step=1,
                                                        value=0,
                                                        updatemode='drag',
                                                    ),
                                                ], style={"width": "100%", "height": "15px", "vertical-align": "center", "display": "inline-block"}),
                                            ], style={"width": "60%"}),
                                        ]),
                                    ]),
                                ]),
                            ], style={"width": "70%", "color": "#ccc", "font-family": "monospace", "font-weight": 'bold'}),
                        ]),
                        html.Tr([
                            html.Td([
                                html.P("Distances prédites", style={"font-weight": 'bold'}),
                            ], style={"width": "30%"}),
                            html.Td([
                                html.H5(id="predicted_distances", children=["-"]),
                            ], style={"width": "70%", "color": "#ccc", "font-family": "monospace", "font-weight": 'bold'}),
                        ]),
                    ]),
                ], style={"width": "100%"}),
            ], style=tab_style, selected_style=tab_selected_style),
        ]),
    ], style={'margin-left': '2%', 'margin-right': '2%'}),
    html.Footer("© Karim Selami, Quentin Braem - 2021~2022", style={
        "position": "fixed",
        "right": "8px",
        "bottom": "4px",
        "font-size": 14,
    }),
], style={
    "background-image": "url(./assets/background.jpg)",
    "background-attachment": "fixed",
    "background-size": "cover",
})

#
# Callbacks
#

def state_has_changed(name):
    for triggered in dash.callback_context.triggered:
        if triggered["prop_id"] == name:
            return True
    return False

#
# Met à jour la visualisation du système planétaire
#

@app.callback(
    [ Output('planetary_system', 'figure'),
      Output('info_num_asteroids', 'children') ],
    [ Input('planetary_system', 'figure'),
      Input('planetary_system', 'clickData'),
      Input('checkbox_diameter', 'value'),
      Input('checkbox_semi_major_axis', 'value'),
      Input('checkbox_eccentricity', 'value'),
      Input('checkbox_inclination', 'value'),
      Input('checkbox_longitude_ascending_node', 'value'),
      Input('checkbox_argument_perihelion', 'value'),
      Input('checkbox_mean_anomaly', 'value'),
      Input('checkbox_dist', 'value'),
      Input('checkbox_Mercure', 'value'),
      Input('checkbox_Venus', 'value'),
      Input('checkbox_Terre', 'value'),
      Input('checkbox_Mars', 'value'),
      Input('checkbox_Jupiter', 'value'),
      Input('checkbox_Saturne', 'value'),
      Input('checkbox_Uranus', 'value'),
      Input('checkbox_Neptune', 'value'),
      Input('slider_bounds', 'value'),
      Input('rslider_distance', 'value'),
      Input('rslider_diameter', 'value'),
      Input('slider_asteroid_size', 'value'),
      Input('button_display', 'n_clicks'), ],
      Input('button_view', 'n_clicks'),
    [ Input('input_num_asteroids', 'value'),
      State("planetary_system", "relayoutData") ]
)
def update_planetary_system(
    figure,
    click_data,
    checkbox_diameter,
    checkbox_semi_major_axis,
    checkbox_eccentricity,
    checkbox_inclination,
    checkbox_longitude_ascending_node,
    checkbox_argument_perihelion,
    checkbox_mean_anomaly,
    checkbox_dist,
    checkbox_Mercure,
    checkbox_Venus,
    checkbox_Terre,
    checkbox_Mars,
    checkbox_Jupiter,
    checkbox_Saturne,
    checkbox_Uranus,
    checkbox_Neptune,
    slider_bounds,
    rslider_distance,
    rslider_diameter,
    slider_asteroid_size,
    button_view,
    button_display,
    input_num_asteroids,
    relayout_data
):
    bounds = 100000000 * (10 ** (slider_bounds / 40) if slider_bounds is not None else 0)
    dist_min = 100000000 * (10 ** (rslider_distance[0] / 40) if rslider_distance is not None else 0)
    dist_max = 100000000 * (10 ** (rslider_distance[1] / 40) if rslider_distance is not None else 0)
    diameter_min = rslider_diameter[0]
    diameter_max = rslider_diameter[1]
    limit = input_num_asteroids
    planets = checkbox_Mercure + checkbox_Venus + checkbox_Terre + checkbox_Mars + checkbox_Jupiter + checkbox_Saturne + checkbox_Uranus + checkbox_Neptune
    details = checkbox_diameter + checkbox_semi_major_axis + checkbox_eccentricity + checkbox_inclination + checkbox_longitude_ascending_node + checkbox_argument_perihelion + checkbox_mean_anomaly + checkbox_dist
    size = slider_asteroid_size

    # Affichage de l'astéroïde prédit et sa trajectoire quand l'utilisateur clique sur le bouton "Visualiser"
    if state_has_changed("button_view.n_clicks") and globals.ml_predicted is not None:
        figure["data"][-4]["x"] = [globals.ml_predicted["x0"]]
        figure["data"][-4]["y"] = [globals.ml_predicted["y0"]]
        figure["data"][-4]["z"] = [globals.ml_predicted["z0"]]
        figure["data"][-3]["x"] = globals.ml_predicted["x"]
        figure["data"][-3]["y"] = globals.ml_predicted["y"]
        figure["data"][-3]["z"] = globals.ml_predicted["z"]
        figure["data"][-3]["visible"] = True

    # Changement du nombre d'astéroïdes
    # Changement de l'affichage des astéroïdes en fonction du diamètre
    # Changement de la distance d'affichage des astéroïdes
    # Changement de la distance d'affichage
    if (state_has_changed("button_display.n_clicks") or
        state_has_changed("rslider_diameter.value") or
        state_has_changed("rslider_distance.value") or
        state_has_changed("slider_bounds.value")):
        figure2 = draw.get_planetary_system(bounds, dist_min, dist_max, diameter_min, diameter_max, limit, planets, details, size)
        figure["data"] = figure2["data"]
        info_num_asteroids = "Nombre d'astéroïdes affichés : " + str(len(figure["data"][-2]["x"]))
        return figure, info_num_asteroids
    
    # Sélection d'un astéroïde
    if click_data is not None and len(click_data["points"]) > 0:
        draw.highlight_asteroid(figure, click_data["points"][0]["pointNumber"])
    else:
        draw.highlight_asteroid(figure, -1)
        
    # Affichage des détails et/ou changement de la taille des astéroïdes
    if (state_has_changed("checkbox_diameter.value") or
        state_has_changed("checkbox_semi_major_axis.value") or
        state_has_changed("checkbox_eccentricity.value") or
        state_has_changed("checkbox_inclination.value") or
        state_has_changed("checkbox_longitude_ascending_node.value") or
        state_has_changed("checkbox_argument_perihelion.value") or
        state_has_changed("checkbox_mean_anomaly.value") or
        state_has_changed("checkbox_dist.value") or
        state_has_changed("slider_asteroid_size.value") or
        state_has_changed("button_view.n_clicks")):
        asteroids = globals.db_asteroids
        for i in range(len(asteroids)):
            text_size = draw.get_asteroid_description_and_size(asteroids[i], details, size)
            figure["data"][-2]["text"][i] = text_size[0]
            figure["data"][-2]["marker"]["size"][i] = text_size[1]
        if globals.ml_predicted is not None:
            text_size = draw.get_asteroid_description_and_size(globals.ml_predicted, details, size)
            figure["data"][-4]["text"] = ["Astéroïde prédit<br>" + text_size[0]]
            figure["data"][-4]["marker"]["size"] = [text_size[1]]
            figure["data"][-4]["visible"] = True
            
    # Affichage ou masquage des planètes
    if any([state_has_changed("checkbox_" + planet["name"] + ".value") for planet in query.get_planets()]):
        for i, fig in enumerate(figure["data"]):
            if "text" in fig and type(fig["text"]) == str and fig["text"] != "Soleil":
                if fig["text"] in planets:
                    figure["data"][i]["visible"] = True
                    figure["data"][i + 1]["visible"] = True
                else:
                    figure["data"][i]["visible"] = False
                    figure["data"][i + 1]["visible"] = False
                    
    # Permet de garder la position et le zoom de la caméra
    figure2 = figure
    figure2["layout"]["uirevision"] = True
    try:
        figure2["layout"]["scene"]["camera"] = relayout_data["scene.camera"]
    except:
        pass
    info_num_asteroids = "Nombre d'astéroïdes affichés : " + str(len(figure["data"][-2]["x"]))
    return figure2, info_num_asteroids

#
# Synchronise les valeurs des inputs avec celles des sliders.
#

@app.callback(
    [ Output("input_" + k, "value") for k, v in globals.ml_features.items() if v["type"] == "slider" ] +
    [ Output("slider_" + k, "value") for k, v in globals.ml_features.items() if v["type"] == "slider" ],
    [ Input("input_" + k, "value") for k, v in globals.ml_features.items() if v["type"] == "slider" ] +
    [ Input("slider_" + k, "value") for k, v in globals.ml_features.items() if v["type"] == "slider" ],
)
def update_inputs_and_sliders(*args):
    sliders = [ k for k, v in globals.ml_features.items() if v["type"] == "slider" ]
    input_values = list(args[:len(sliders)])
    slider_values = list(args[len(sliders):])
    for i, k in enumerate(sliders):
        if state_has_changed("input_" + k + ".value"):
            slider_values[i] = input_values[i]
        elif state_has_changed("slider_" + k + ".value"):
            input_values[i] = slider_values[i]
    return input_values + slider_values

#
# Calcule et affiche la prédiction quand l'utilisateur clique sur le bouton "Prédire" ou
# change la position prédite affichée en fonction de la valeur du slider associé.
#

@app.callback(
    [ Output('predicted_diameter', 'children'),
      Output('predicted_trajectory', 'children'),
      Output('predicted_distances', 'children'), ],
    [ Input('button_predict', 'n_clicks'),
      Input('slider_predicted_trajectory', 'value'), ],
    [ State(v["type"] + "_" + k, "value") for k, v in globals.ml_features.items() ]
)
def predict(n_clicks, pos, *args):
    
    # L'utilisateur a cliqué sur "Prédire"
    if state_has_changed("button_predict.n_clicks"):
        features = { k: args[i] for i, k in enumerate(globals.ml_features.keys()) }
        try:
            globals.ml_predicted = ml.predict_asteroid_diameter_trajectory_and_distances(features)
        except:
            globals.ml_predicted = None
            
    # Met à jour l'affichage de la prédiction
    if pos is None: pos = 0
    if globals.ml_predicted is not None:
        return (
            "{:.2f}".format(
                globals.ml_predicted["diameter"]
            ) + " km",
            "({:.2f}, {:.2f}, {:.2f})".format(
                globals.ml_predicted["x"][pos] * globals.km_to_ua,
                globals.ml_predicted["y"][pos] * globals.km_to_ua,
                globals.ml_predicted["z"][pos] * globals.km_to_ua
            ) + " UA^3",
            "{:.2f}".format(
                globals.ml_predicted["dist_sun"][pos] * globals.km_to_ua
            ) + " UA (Soleil) | " +
            "{:.2f}".format(
                globals.ml_predicted["dist_earth"][pos] * globals.km_to_ua
            ) + " UA (Terre)",
        )
    else:
        return ("-", "-", "-")

#
# Revient sur la première page (Système Solaire 3D) quand l'utilisateur clique sur le bouton "Visualiser",
# uniquement si un astéroïde a été prédit.
#

@app.callback(
      Output("tabs", "value"),
    [ Input("button_view", "n_clicks") ]
)
def view_predicted_asteroid(n_clicks):
    if globals.ml_predicted is not None:
        return "tab-1"
    else:
        raise PreventUpdate

#
# Point d'entrée de l'application
#

if __name__ == '__main__':
    app.run_server(debug=False)
