from query import *

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


from astropy import units as u
from poliastro.twobody import Orbit
from poliastro.bodies import Sun



def get_asteroid_description_and_size(asteroid, displayDetails, displaySize):
    text = "Diamètre : " + "{:.2f}".format(asteroid['diameter']) + " km<br>"
    if displayDetails:
        text += "Demi grand-axe : " + "{:.2f}".format(asteroid['semi_major_axis']) + " UA<br>"
        text += "Excentricité : " + "{:.2f}".format(asteroid['eccentricity']) + "<br>"
        text += "Inclinaison : " + "{:.2f}".format(asteroid['inclination']) + "°<br>"
        text += "Longitude du noeud ascendant : " + "{:.2f}".format(asteroid['longitude_ascending_node']) + "°<br>"
        text += "Argument du périastre : " + "{:.2f}".format(asteroid['argument_perihelion']) + "°<br>"
        text += "Anomalie moyenne : " + "{:.2f}".format(asteroid['mean_anomaly']) + "°<br>"
        text += "Distance au Soleil : " + "{:.2f}".format(asteroid['dist'] / 150000000) + " UA<br>"
    size = displaySize * max(1.0, np.log(asteroid["diameter"]))
    return text, size
    
    



def draw_star(figure):
    star = query_star()
    fig = go.Scatter3d(
        x=[0],
        y=[0],
        z=[0],
        mode='markers',
        opacity=1,
        hoverinfo ="text",
        text=star["name"],
        marker_color=star["color"],
        marker_size=(2 * np.log(star["diameter"])),
    )
    figure.add_trace(fig)
    

def draw_planets(figure, bounds, displayPlanets):
    planets = query_planets()
    for planet in planets:
        x = planet["x"][0]
        y = planet["y"][0]
        z = planet["z"][0]
        isVisible = displayPlanets == None or planet["name"] in displayPlanets
        
        # Si la planète est en dehors de la zone de traçage, inutile de la dessiner
        dist = 1.1 * sqrt(x * x + y * y + z * z)
        if dist > bounds:
            continue
        
        # Planète
        fig = go.Scatter3d(
            x=[x],
            y=[y],
            z=[z],
            mode="markers",
            opacity=1,
            hoverinfo="text",
            text=planet["name"],
            marker_color=planet["color"],
            marker_size=(1.5 * np.log(planet["diameter"])),
            visible=isVisible,
        )
        figure.add_trace(fig)
        
        # Orbite
        fig = go.Scatter3d(
            x=planet["x"],
            y=planet["y"],
            z=planet["z"],
            mode="lines",
            connectgaps=True,
            opacity=1,
            hoverinfo="skip",
            marker_color=planet["color"],
            line_width=5,
            visible=isVisible,
        )
        figure.add_trace(fig)


def draw_asteroids(figure, bounds, distMin, distMax, diameterMin, diameterMax, limit, displayDetails, displaySize):
    asteroids = query_asteroids(bounds, distMin, distMax, diameterMin, diameterMax, limit)
    drawData = {
        "x": [],
        "y": [],
        "z": [],
        "text": [],
        "color": [],
        "size": []
    }
    
    # Récupère les astéroïdes à dessiner
    for i, asteroid in enumerate(asteroids):
        text, size = get_asteroid_description_and_size(asteroid, displayDetails, displaySize)
        drawData["x"].append(asteroid["x0"])
        drawData["y"].append(asteroid["y0"])
        drawData["z"].append(asteroid["z0"])
        drawData["text"].append(text)
        drawData["color"].append("#606060")
        drawData["size"].append(size)
        
    # Astéroïdes
    fig = go.Scatter3d(
        x=drawData["x"],
        y=drawData["y"],
        z=drawData["z"],
        mode="markers",
        opacity=1,
        hoverinfo="text",
        name="drawData",
        text=drawData["text"],
        marker_color=drawData["color"],
        marker_size=drawData["size"],
    )
    figure.add_trace(fig)
    
    # Trajectoire
    fig = go.Scatter3d(
        x=np.zeros(181),
        y=np.zeros(181),
        z=np.zeros(181),
        mode="lines",
        opacity=1,
        connectgaps=True,
        name="trajectory",
        hoverinfo="skip",
        marker_color="#FFFFFF",
        line_width=5,
    )
    figure.add_trace(fig)


def draw_planetary_system(bounds=1000000000, distMin=0, distMax=50000000000, diameterMin=0, diameterMax=100, limit=1000, displayPlanets=None, displayDetails=False, displaySize=5):
    figure = go.FigureWidget()
    draw_star(figure)
    draw_planets(figure, bounds, displayPlanets)
    draw_asteroids(figure, bounds, distMin, distMax, diameterMin, diameterMax, limit, displayDetails, displaySize)
    figure.update_layout({
        "clickmode": "event+select",
        "showlegend": False,
        "autosize": False,
        "width": 1500,
        "height": 1500,
        "paper_bgcolor":'rgba(0,0,0,0.75)',
        "plot_bgcolor":'rgba(0,0,0,0.75)',
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




def compute_body_position(semi_major_axis, eccentricity, inclination, longitude_ascending_node, argument_perihelion, mean_anomaly, delta_anomaly=0):
    true_anomaly = (mean_anomaly + delta_anomaly) + 2 * eccentricity * sin(mean_anomaly + delta_anomaly)
    o = Orbit.from_classical(
        Sun,
        semi_major_axis * u.AU,
        eccentricity * u.one,
        inclination * u.deg,
        longitude_ascending_node * u.deg,
        argument_perihelion * u.deg,
        true_anomaly * u.deg
    )
    return (o.r[0].value, o.r[1].value, o.r[2].value)


def compute_body_trajectory(semi_major_axis, eccentricity, inclination, longitude_ascending_node, argument_perihelion, mean_anomaly):
    trajectory = { "x": [], "y": [], "z": [] }
    for i in range(181):
        point = compute_body_position(semi_major_axis, eccentricity, inclination, longitude_ascending_node, argument_perihelion, mean_anomaly, (2 * i) % 360)
        trajectory["x"].append(point[0])
        trajectory["y"].append(point[1])
        trajectory["z"].append(point[2])
    return trajectory




def highlight_asteroid(figure, point_number):
    colors = np.repeat(["#606060"], len(figure["data"][-2]["marker"]["color"]))

    # Sélectionne l'astéroïde cliqué
    if point_number != -1:
        asteroid = query_asteroid(point_number)
        trajectory = compute_body_trajectory(
            asteroid["semi_major_axis"],
            asteroid["eccentricity"],
            asteroid["inclination"],
            asteroid["longitude_ascending_node"],
            asteroid["argument_perihelion"],
            asteroid["mean_anomaly"]
        )
        trajectoryX = trajectory["x"]
        trajectoryY = trajectory["y"]
        trajectoryZ = trajectory["z"]
        colors[point_number] = "#FFFFFF"
    else:
        trajectoryX = np.zeros(181)
        trajectoryY = np.zeros(181)
        trajectoryZ = np.zeros(181)
        
    # Met à jour le graphique
    figure["data"][-2]["marker"]["color"] = tuple(colors)
    figure["data"][-1]["x"] = trajectoryX
    figure["data"][-1]["y"] = trajectoryY
    figure["data"][-1]["z"] = trajectoryZ
    pass
    
