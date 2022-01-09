import globals
import query
import scipy as sp
import pandas as pd
import pickle as pk
from math import *
from catboost import CatBoostRegressor

#
# Prédit et retourne l'astéroïde correspondant aux features d'entrée.
#

def predict_asteroid_diameter_trajectory_and_distances(features):
    
    # Récupération du modèle
    with open("best_model.pkl", 'rb') as f:
        unpickler = pk.Unpickler(f)
        model = unpickler.load()
    
    # Création des features
    gauss = lambda x: 1 + sqrt(2) * 0.2 * sp.special.erfinv(2 * (x / 360) - 1)    
    X = pd.DataFrame(
        data=[[
            features["semi_major_axis"],
            features["eccentricity"],
            features["inclination"],
            features["longitude_ascending_node"],
            features["argument_perihelion"],
            features["distance_perihelion"],
            features["distance_aphelion"],
            features["data_arc_span"],
            features["nb_observations"],
            features["absolute_magnitude_parameter"],
            features["near_earth_object"],
            features["hazardous_asteroid"],
            features["albedo"],
            features["asteroid_orbit_class"],
            features["mean_anomaly"],
            sqrt(features["nb_observations"]),
            log(features["distance_aphelion"]),
            log(features["albedo"]),
            sqrt(features["eccentricity"]),
            sqrt(features["inclination"]),
            gauss(features["mean_anomaly"]),
            gauss(features["argument_perihelion"]),
            gauss(features["longitude_ascending_node"]),
            features["known_orbit"]
        ]],
        columns=[
            'semi_major_axis',
            'eccentricity',
            'inclination',
            'longitude_ascending_node',
            'argument_perihelion',
            'distance_perihelion',
            'distance_aphelion',
            'data_arc_span',
            'nb_observations',
            'absolute_magnitude_parameter',
            'near_earth_object',
            'hazardous_asteroid',
            'albedo',
            'asteroid_orbit_class',
            'mean_anomaly',
            'sqrt_nb_observations',
            'log_distance_aphelion',
            'log_albedo',
            'sqrt_eccentricity',
            'sqrt_inclination',
            'gauss_mean_anomaly',
            'gauss_argument_perihelion',
            'gauss_longitude_ascending_node',
            'known_orbit'
        ]
    )
    
    # Astéroïde prédit
    predicted = {
        "semi_major_axis": features["semi_major_axis"],
        "eccentricity": features["eccentricity"],
        "inclination": features["inclination"],
        "longitude_ascending_node": features["longitude_ascending_node"],
        "argument_perihelion": features["argument_perihelion"],
        "mean_anomaly": features["mean_anomaly"],
        "color": "#FF80FF",
    }
        
    # Prédiction du diamètre
    predicted["diameter"] = float(model["model"].predict(X)[0])
    
    # Prédiction de la trajectoire
    predicted_trajectory = query.get_asteroid_trajectory(
        features["semi_major_axis"],
        features["eccentricity"],
        features["inclination"],
        features["longitude_ascending_node"],
        features["argument_perihelion"],
        features["mean_anomaly"]
    )
    predicted["x"] = predicted_trajectory["x"]
    predicted["y"] = predicted_trajectory["y"]
    predicted["z"] = predicted_trajectory["z"]
    predicted["x0"] = predicted_trajectory["x"][0]
    predicted["y0"] = predicted_trajectory["y"][0]
    predicted["z0"] = predicted_trajectory["z"][0]
    
    # Prédiction des distances
    earth = query.get_planet("Terre")
    predicted["dist_sun"] = []
    predicted["dist_earth"] = []
    for i in range(len(predicted["x"])):
        predicted["dist_sun"].append(sqrt(
            predicted["x"][i] ** 2 +
            predicted["y"][i] ** 2 +
            predicted["z"][i] ** 2
        ))
        predicted["dist_earth"].append(sqrt(
            (predicted["x"][i] - earth["x"][0]) ** 2 +
            (predicted["y"][i] - earth["y"][0]) ** 2 +
            (predicted["z"][i] - earth["z"][0]) ** 2
        ))
    predicted["dist"] = predicted["dist_sun"][0]
    
    # Retourne la prédiction
    return predicted
