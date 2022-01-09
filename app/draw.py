import globals
import query
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from math import *

#
# Crée et retourne une checkbox.
#

def get_checkbox(name, title, checked):
    return html.Tr([
        dcc.Checklist(
            id='checkbox_' + name,
            options=[{'label': title, 'value': name}],
            value=[name] if checked else [],
            style={"white-space": "nowrap", "font-size": 12},
        ),
    ])

#
# Crée et retourne un input numérique.
#

def get_slider(name, title, min, max, step):
    return html.Tr([
        html.Td([
            html.P(title, style={"font-weight": 'bold'}),
        ], style={"width": "30%"}),
        html.Td([
            html.Div([
                dcc.Input(
                    id='input_' + name,
                    type="number",
                    min=min,
                    max=max,
                    step=step,
                    value=min,
                    style={"width": "100%"}
                ),
            ], style={"width": "10%", "display": "inline-block"}),
            html.Div([
                dcc.Slider(
                    id='slider_' + name,
                    min=min,
                    max=max,
                    step=step,
                    value=min,
                    tooltip={"placement": "bottom", "always_visible": False},
                ),
            ], style={"width": "90%", "height": "15px", "vertical-align": "center", "display": "inline-block"}),
        ], style={"width": "70%"}),
    ])

#
# Crée et retourne une liste déroulante.
#
    
def get_dropdown(name, title, options, value):
    return html.Tr([
        html.Td([
            html.P(title, style={"font-weight": 'bold'}),
        ], style={"width": "30%"}),
        html.Td([
            dcc.Dropdown(
                id='dropdown_' + name,
                options=options,
                value=value,
            ),
        ], style={"width": "70%"}),
    ])

#
# Retourne la description et la taille de l'astéroïde.
#

def get_asteroid_description_and_size(asteroid, details, size):
    text = ""
    if details is not None and len(details) != 0:
        if "diameter" in details:
            text += "Diamètre : " + "{:.2f}".format(asteroid['diameter']) + " km<br>"
        if "semi_major_axis" in details:
            text += "Demi grand-axe : " + "{:.2f}".format(asteroid['semi_major_axis']) + " UA<br>"
        if "eccentricity" in details:
            text += "Excentricité : " + "{:.2f}".format(asteroid['eccentricity']) + "<br>"
        if "inclination" in details:
            text += "Inclinaison : " + "{:.2f}".format(asteroid['inclination']) + "°<br>"
        if "longitude_ascending_node" in details:
            text += "Longitude du noeud ascendant : " + "{:.2f}".format(asteroid['longitude_ascending_node']) + "°<br>"
        if "argument_perihelion" in details:
            text += "Argument du périastre : " + "{:.2f}".format(asteroid['argument_perihelion']) + "°<br>"
        if "mean_anomaly" in details:
            text += "Anomalie moyenne : " + "{:.2f}".format(asteroid['mean_anomaly']) + "°<br>"
        if "dist" in details:
            earth = query.get_planet("Terre")
            earth_pos = [
                earth["x"][0],
                earth["y"][0],
                earth["z"][0],
            ]
            earth_dist = sqrt(
                (asteroid["x0"] - earth_pos[0]) ** 2 +
                (asteroid["y0"] - earth_pos[1]) ** 2 +
                (asteroid["z0"] - earth_pos[2]) ** 2
            )
            text += "Distance au Soleil : " + "{:.2f}".format(asteroid['dist'] * globals.km_to_ua) + " UA<br>"
            text += "Distance à la Terre : " + "{:.2f}".format(earth_dist * globals.km_to_ua) + " UA<br>"
    else:
        text = "Asteroïde"
    return text, size * max(1.0, log(asteroid["diameter"]))

#
# Retourne un objet graphique représentant l'étoile du système.
#

def get_star():
    star = query.get_star()
    return go.Scatter3d(
        x=[0],
        y=[0],
        z=[0],
        mode='markers',
        opacity=1,
        hoverinfo ="text",
        text=star["name"],
        marker_color=star["color"],
        marker_size=(2 * log(star["diameter"])),
    )

#
# Retourne une liste d'objets graphiques représentant les planètes du système.
#

def get_planets(bounds, planets):
    figs = []
    for planet in query.get_planets():
        x = planet["x"][0]
        y = planet["y"][0]
        z = planet["z"][0]
        is_visible = planets is None or planet["name"] in planets
        
        # Si la planète est en dehors de la zone de traçage, inutile de la dessiner
        dist = 1.1 * sqrt(x * x + y * y + z * z)
        if dist > bounds:
            continue
        
        # Planète
        figs.append(go.Scatter3d(
            x=[x],
            y=[y],
            z=[z],
            mode="markers",
            opacity=1,
            hoverinfo="text",
            text=planet["name"],
            marker_color=planet["color"],
            marker_size=(1.5 * log(planet["diameter"])),
            visible=is_visible,
        ))
        
        # Orbite
        figs.append(go.Scatter3d(
            x=planet["x"],
            y=planet["y"],
            z=planet["z"],
            mode="lines",
            connectgaps=True,
            opacity=1,
            hoverinfo="skip",
            marker_color=planet["color"],
            line_width=5,
            visible=is_visible,
        ))
    return figs

#
# Retourne une liste d'objets graphiques représentant les astéroïdes du système.
#

def get_asteroids(bounds, dist_min, dist_max, diameter_min, diameter_max, limit, details, size):
    asteroids = query.get_asteroids(bounds, dist_min, dist_max, diameter_min, diameter_max, limit)
    draw_data = {
        "x": [],
        "y": [],
        "z": [],
        "text": [],
        "color": [],
        "size": []
    }
    
    # Récupère les astéroïdes à dessiner
    for i, asteroid in enumerate(asteroids):
        text_size = get_asteroid_description_and_size(asteroid, details, size)
        draw_data["x"].append(asteroid["x0"])
        draw_data["y"].append(asteroid["y0"])
        draw_data["z"].append(asteroid["z0"])
        draw_data["text"].append(text_size[0])
        draw_data["color"].append("#606060")
        draw_data["size"].append(text_size[1])
    
    return [
        
    # Astéroïde prédit
    go.Scatter3d(
        x=[0],
        y=[0],
        z=[0],
        mode="markers",
        opacity=1,
        hoverinfo="text",
        text="",
        marker_color="#FF80FF",
        marker_size=0,
        visible=False,
    ),
    
    # Trajectoire de la prédiction
    go.Scatter3d(
        x=[0 for i in range(181)],
        y=[0 for i in range(181)],
        z=[0 for i in range(181)],
        mode="lines",
        connectgaps=True,
        opacity=1,
        hoverinfo="skip",
        marker_color="#FF80FF",
        line_width=5,
        visible=False,
    ),
        
    # Astéroïdes
    go.Scatter3d(
        x=draw_data["x"],
        y=draw_data["y"],
        z=draw_data["z"],
        mode="markers",
        opacity=1,
        hoverinfo="text",
        text=draw_data["text"],
        marker_color=draw_data["color"],
        marker_size=draw_data["size"],
    ),
    
    # Trajectoire de l'astéroïde sélectionné
    go.Scatter3d(
        x=[0 for i in range(181)],
        y=[0 for i in range(181)],
        z=[0 for i in range(181)],
        mode="lines",
        opacity=1,
        connectgaps=True,
        hoverinfo="skip",
        marker_color="#FFFFFF",
        line_width=5,
    )
    ]

#
# Retourne la figure sur laquelle est représenté le système planétaire.
#

def get_planetary_system(bounds=1000000000, dist_min=0, dist_max=50000000000, diameter_min=0, diameter_max=100, limit=1000, planets=None, details=["diameter"], size=5):
    figure = go.FigureWidget()
    figure.add_trace(get_star())
    for fig in get_planets(bounds, planets): figure.add_trace(fig)
    for fig in get_asteroids(bounds, dist_min, dist_max, diameter_min, diameter_max, limit, details, size): figure.add_trace(fig)
    figure.update_layout({
        "clickmode": "event+select",
        "showlegend": False,
        "paper_bgcolor":'rgba(0,0,0,0.5)',
        "plot_bgcolor":'rgba(0,0,0,0.5)',
        "margin": { "l": 0, "r": 0, "t": 0, "b": 0 },
        "scene": {
            "aspectmode": "cube",
            "xaxis": {
                "range": [-5000000000, +5000000000],
                "visible": False,
                "showgrid": False,
                "showticklabels": False,
                "showbackground": False,
                "zerolinecolor": "#000000"
            },
            "yaxis": {
                "range": [-5000000000, +5000000000],
                "visible": False,
                "showgrid": False,
                "showticklabels": False,
                "showbackground": False,
                "zerolinecolor": "#000000"
            },
            "zaxis": {
                "range": [-5000000000, +5000000000],
                "visible": False,
                "showgrid": False,
                "showticklabels": False,
                "showbackground": False,
                "zerolinecolor": "#000000"
            },
        }
    })
    return figure

#
# Modifie les paramètres de l'astéroïde sélectionné pour le mettre au premier plan et afficher sa trajectoire.
#

def highlight_asteroid(figure, point_number):
    colors = ["#606060" for i in range(len(figure["data"][-2]["marker"]["color"]))]

    # Sélectionne l'astéroïde cliqué
    asteroid = query.get_asteroid(point_number)
    if asteroid is not None:
        trajectory = query.get_asteroid_trajectory(
            asteroid["semi_major_axis"],
            asteroid["eccentricity"],
            asteroid["inclination"],
            asteroid["longitude_ascending_node"],
            asteroid["argument_perihelion"],
            asteroid["mean_anomaly"]
        )
        trajectory_x = trajectory["x"]
        trajectory_y = trajectory["y"]
        trajectory_z = trajectory["z"]
        colors[point_number] = "#FFFFFF"
    else:
        trajectory_x = [0 for i in range(181)]
        trajectory_y = [0 for i in range(181)]
        trajectory_z = [0 for i in range(181)]
        
    # Met à jour le graphique
    figure["data"][-2]["marker"]["color"] = tuple(colors)
    figure["data"][-1]["x"] = trajectory_x
    figure["data"][-1]["y"] = trajectory_y
    figure["data"][-1]["z"] = trajectory_z
