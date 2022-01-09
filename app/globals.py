#
# Données et constantes
#

ua_to_km = 149597870.7

km_to_ua = 1.0 / ua_to_km

db_planets = None

db_asteroids = None

ml_predicted = None

ml_features = {
    "semi_major_axis": {
        "type": "slider",
        "name": "Demi-grand axe (ua)",
        "min": 1.8,
        "max": 5.2,
        "step": 0.01
    },
    "eccentricity": {
        "type": "slider",
        "name": "Excentricité",
        "min": 0,
        "max": 0.999,
        "step": 0.001
    },
    "absolute_magnitude_parameter": {
        "type": "slider",
        "name": "Magnitude absolue",
        "min": 9,
        "max": 24,
        "step": 0.01
    },
    "distance_perihelion": {
        "type": "slider",
        "name": "Distance au périhélie (ua)",
        "min": 0,
        "max": 5.2,
        "step": 0.01
    },
    "distance_aphelion": {
        "type": "slider",
        "name": "Distance à l'aphélie (ua)",
        "min": 1.8,
        "max": 7.5,
        "step": 0.01
    },
    "nb_observations": {
        "type": "slider",
        "name": "Nombre d'observations",
        "min": 5,
        "max": 6500,
        "step": 1
    },
    "data_arc_span": {
        "type": "slider",
        "name": "Arc d'observation (j)",
        "min": 1,
        "max": 55000,
        "step": 1
    },
    "albedo": {
        "type": "slider",
        "name": "Albédo",
        "min": 0.001,
        "max": 1,
        "step": 0.001
    },
    "inclination": {
        "type": "slider",
        "name": "Inclinaison de l'orbite (deg)",
        "min": 0,
        "max": 180,
        "step": 0.1
    },
    "mean_anomaly": {
        "type": "slider",
        "name": "Anomalie moyenne (deg)",
        "min": 0,
        "max": 360,
        "step": 0.1
    },
    "argument_perihelion": {
        "type": "slider",
        "name": "Argument du périastre (deg)",
        "min": 0,
        "max": 360,
        "step": 0.1
    },
    "longitude_ascending_node": {
        "type": "slider",
        "name": "Longitude du noeud ascendant (deg)",
        "min": 0,
        "max": 360,
        "step": 0.1
    },
    "near_earth_object": {
        "type": "dropdown",
        "name": "Objet géocroiseur",
        "values": [
            {"label": "Oui", "value": 1},
            {"label": "Non", "value": 0}
        ],
        "value": 0,
    },
    "hazardous_asteroid": {
        "type": "dropdown",
        "name": "Astéroide potentiellement dangereux",
        "values": [
            {"label": "Oui", "value": 1},
            {"label": "Non", "value": 0}
        ],
        "value": 0,
    },
    "known_orbit": {
        "type": "dropdown",
        "name": "Orbite connue",
        "values": [
            {"label": "Oui", "value": 1},
            {"label": "Non", "value": 0}
        ],
        "value": 1,
    },
    "asteroid_orbit_class": {
        "type": "dropdown",
        "name": "Classe d'orbite",
        "values": [
            {"label": "AMO - Amor", "value": 1},
            {"label": "APO - Apollo", "value": 0},
            {"label": "MCA - Mars-crossing Asteroid", "value": 3},
            {"label": "IMB - Inner Main-belt Asteroid", "value": 2},
            {"label": "MBA - Main-belt Asteroid", "value": 4},
            {"label": "OMB - Outer Main-belt Asteroid", "value": 5},
            {"label": "TJN - Jupiter Trojan", "value": 6},
        ],
        "value": 1,
    },
}
