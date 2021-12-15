from query import *
from draw import *

from elasticsearch import Elasticsearch

import json
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask import Flask, render_template, url_for, request
from flask.wrappers import JSONMixin
from markupsafe import Markup
import numpy as np
import pandas as pd
import locale
from random import randint
import warnings
import pickle as pk
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import plotly as ply
import plotly.graph_objects as go
import multiprocessing
import os

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import random
import numpy as np
import pandas as pd
from statsmodels.graphics.gofplots import qqplot
from sklearn.model_selection import train_test_split
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff
import pickle as pk

from math import *
from datetime import date
from plotly.subplots import make_subplots
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
from xgboost import XGBRegressor
from multiprocessing import Pool
from tqdm.notebook import tqdm




### Application

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server





### Point d'entrée de l'application

app.layout = html.Div([
    
    html.H1(
      children='Astéroïdes',
      style={
         'textAlign': 'center'
      }
    ),
    
    dcc.Markdown(children= '''
        coucou
    '''
    ),
    
    html.Br(),
    
    dcc.Tabs([
        
        dcc.Tab(label="Système Solaire 3D", children=[
            
            html.H5("Informations des astéroïdes"),
            dcc.Checklist(
                id='checklist_asteroid_details',
                options=[
                    { 'label': 'Afficher le détail', 'value': 'checkbox_asteroid_details' },
                ],
                value=[]
            ),
            
            html.H5("Affichage des planètes"),
            dcc.Checklist(
                id='checklist_planets',
                options=[
                    { 'label': 'Mercure', 'value': 'Mercure' },
                    { 'label': 'Venus', 'value': 'Venus' },
                    { 'label': 'Terre', 'value': 'Terre' },
                    { 'label': 'Mars', 'value': 'Mars' },
                    { 'label': 'Jupiter', 'value': 'Jupiter' },
                    { 'label': 'Saturne', 'value': 'Saturne' },
                    { 'label': 'Uranus', 'value': 'Uranus' },
                    { 'label': 'Neptune', 'value': 'Neptune' },
                ],
                value=[
                    "Mercure",
                    "Venus",
                    "Terre",
                    "Mars",
                    "Jupiter",
                    "Saturne",
                    "Uranus",
                    "Neptune",
                ],
                labelStyle={
                    "width": "10%"
                },
            ),
            
            html.H5("Taille d'affichage des astéroïdes"),
            html.Div(children=[
                dcc.Slider(
                    id='slider_asteroid_size',
                    min=1,
                    max=10,
                    step=1,
                    value=5,
                    marks={ x: str(x) for x in range(1, 11) },
                ),
                ],
                style={
                    "width": "20%"
                },
            ),
            
            html.H5("Distance d'affichage"),
            html.Div(children=[
                dcc.Slider(
                    id='slider_bounds',
                    min=0,
                    max=70,
                    step=1,
                    value=40,
                    marks={
                        (40 * log10((1.1 * sqrt(planet["x"][0] ** 2 + planet["y"][0] ** 2 + planet["z"][0] ** 2)) / 100000000)):
                            planet["name"] for planet in query_planets()
                    },
                ),
                ],
                style={
                    "width": "40%"
                },
            ),
            
            html.H5("Astéroïdes entre x et y"),
            html.Div(children=[
                dcc.RangeSlider(
                    id='rslider_distance',
                    min=0,
                    max=70,
                    step=1,
                    value=[0, 70],
                    marks={
                        (40 * log10((1.1 * sqrt(planet["x"][0] ** 2 + planet["y"][0] ** 2 + planet["z"][0] ** 2)) / 100000000)):
                            planet["name"] for planet in query_planets()
                    },
                ),
                ],
                style={
                    "width": "40%"
                },
            ),
            
            html.H5("Diamètre min et max des astéroïdes"),
            html.Div(children=[
                dcc.RangeSlider(
                    id='rslider_diameter',
                    min=0,
                    max=100,
                    step=1,
                    value=[0, 100],
                    marks={
                        x * 10: str(x * 10) for x in range(11)
                    },
                ),
                ],
                style={
                    "width": "40%"
                },
            ),
            
            html.H5("Nombre maximal d'astéroïdes"),
            html.Div(children=[
                dcc.Input(
                    id="input_num_asteroids",
                    type="number",
                    min=0,
                    max=100000,
                    value=1000,
                )
                ],
                style={
                    "width": "40%"
                },
            ),
            
            dcc.Graph(
                id='planetary_system',
                figure=draw_planetary_system()
            ),
            
        ]),
        
        dcc.Tab(label="Modèle de prédiction du diamètre et de la trajectoire", children=[
            
        ]),
        
        dcc.Tab(label="Quelques jolis graphiques", children=[
            
        ]),
    ]),
], style={'background-image': 'url("https://images4.alphacoders.com/748/74804.jpg")',
        'background-repeat':'repeat',
        'background-attachment':'fixed',
        'overflow':'scroll',
          
          'width': '96%', 'textAlign': 'center', 'margin-left':'2%', 'margin-right':'2%'})





def state_has_changed(name):
    for triggered in dash.callback_context.triggered:
        if triggered["prop_id"] == name:
            return True
    return False
            
    





@app.callback(
    Output('planetary_system', 'figure'),
    [ Input('planetary_system', 'figure'),
      Input('planetary_system', 'clickData'),
      Input('checklist_asteroid_details', 'value'),
      Input('checklist_planets', 'value'),
      Input('slider_asteroid_size', 'value'),
      Input('slider_bounds', 'value'),
      Input('rslider_distance', 'value'),
      Input('rslider_diameter', 'value'),
      Input('input_num_asteroids', 'value'), ],
    [ State("planetary_system", "relayoutData") ]
)
def display_click_data(figure, clickData, checklistAsteroids, checklistPlanets, asteroidSize, boundsLog, distanceMinMaxLog, diameterMinMax, numAsteroids, relayoutData):
    displayDetails = "checkbox_asteroid_details" in checklistAsteroids
    displaySize = asteroidSize
    displayPlanets = checklistPlanets
    bounds = 100000000 * (10 ** (boundsLog / 40) if boundsLog != None else 0)
    distMin = 100000000 * (10 ** (distanceMinMaxLog[0] / 40) if distanceMinMaxLog != None else 0)
    distMax = 100000000 * (10 ** (distanceMinMaxLog[1] / 40) if distanceMinMaxLog != None else 0)
    diameterMin = diameterMinMax[0]
    diameterMax = diameterMinMax[1]
    limit = numAsteroids
    
    
    # Changement du nombre d'astéroïdes
    # Changement de l'affichage des astéroïdes en fonction du diamètre
    # Changement de la distance d'affichage des astéroïdes
    # Changement de la distance d'affichage
    if state_has_changed("input_num_asteroids.value") or\
        state_has_changed("rslider_diameter.value") or\
        state_has_changed("rslider_distance.value") or\
        state_has_changed("slider_bounds.value"):
        figure2 = draw_planetary_system(bounds, distMin, distMax, diameterMin, diameterMax, limit, displayPlanets, displayDetails, displaySize)
        figure["data"] = figure2["data"]
        return figure


    # Sélection d'un astéroïde
    if clickData != None and len(clickData["points"]) > 0:
        highlight_asteroid(figure, clickData["points"][0]["pointNumber"])
    else:
        highlight_asteroid(figure, -1)
        
        
    # Affichage des détails et/ou changement de la taille des astéroïdes
    if state_has_changed("checklist_asteroid_details.value") or\
        state_has_changed("slider_asteroid_size.value"):
        asteroids = get_asteroids()
        for i in range(len(asteroids)):
            text, size = get_asteroid_description_and_size(asteroids[i], displayDetails, displaySize)
            figure["data"][-2]["text"][i] = text
            figure["data"][-2]["marker"]["size"][i] = size


    # Affichage ou masquage des planètes
    if state_has_changed("checklist_planets.value"):
        for i, fig in enumerate(figure["data"]):
            if "text" in fig and type(fig["text"]) == str and fig["text"] != "Soleil":
                if fig["text"] in displayPlanets:
                    figure["data"][i]["visible"] = True
                    figure["data"][i + 1]["visible"] = True
                else:
                    figure["data"][i]["visible"] = False
                    figure["data"][i + 1]["visible"] = False


    # Permet de garder la position et le zoom de la caméra
    figure2 = figure
    figure2["layout"]["uirevision"] = True
    try:
        figure2["layout"]["scene"]["camera"] = relayoutData["scene.camera"]
    except:
        pass


    return figure2






if __name__ == '__main__':
    app.run_server(debug=True)
