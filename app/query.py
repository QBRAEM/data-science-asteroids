import globals
import os
from math import *
from google.cloud import bigquery
from astropy import units as u
from poliastro.twobody import Orbit
from poliastro.bodies import Sun

#
# Retourne les données de l'étoile (Soleil).
#

def get_star():
    return {
        "name": "Soleil",
        "color": "#FFFF00",
        "diameter": 1392680,
    }
    
#
# Charge et retourne les données des planètes.
#

def get_planets():
    if globals.db_planets is None:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Administrateur\Desktop\Formation\projet\asteroids-335014-30ac06c837f2.json"
        client = bigquery.Client()
        table_id = client.project + ".dataset.planets"
        sql = "SELECT * FROM `" + table_id + "`;"
        globals.db_planets = client.query(sql).to_dataframe().to_dict('records')
        for planet in globals.db_planets:
            for coord in ["x", "y", "z"]:
                planet[coord] = eval(planet[coord])
                planet[coord][-1] = planet[coord][0]
    return globals.db_planets

#
# Retourne les données de la planète 'name'.
#

def get_planet(name):
    planets = get_planets()
    for planet in planets:
        if planet["name"] == name:
            return planet
    return None

#
# Requête et retourne les données des astéroïdes.
#

def get_asteroids(bounds, dist_min, dist_max, diameter_min, diameter_max, limit):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Administrateur\Desktop\Formation\projet\asteroids-335014-30ac06c837f2.json"
    client = bigquery.Client()
    table_id = client.project + ".dataset.asteroids_details"
    sql = \
        "SELECT * FROM `" + table_id + "` " + \
        "WHERE dist < " + str(bounds) + " " + \
        "AND dist < " + str(dist_max) + " " + \
        "AND dist > " + str(dist_min) + " " + \
        "AND diameter < " + str(diameter_max) + " " + \
        "AND diameter > " + str(diameter_min) + " " + \
        "ORDER BY RAND() " + \
        "LIMIT " + str(limit) + " ;"
    asteroids = client.query(sql).to_dataframe().to_dict('records')
    print("Loaded", len(asteroids), "asteroids.")
    globals.db_asteroids = asteroids
    return asteroids

#
# Retourne les données de l'astéroïde 'n'.
#

def get_asteroid(n):
    if n >= 0 and n < len(globals.db_asteroids):
        return globals.db_asteroids[n]
    return None
    
#
# Retourne la position de l'astéroïde en fonction de ses composantes.
#

def get_asteroid_position(semi_major_axis, eccentricity, inclination, longitude_ascending_node, argument_perihelion, mean_anomaly, delta_anomaly=0):
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

#
# Retourne la trajectoire de l'astéroïde en fonction de ses composantes.
#

def get_asteroid_trajectory(semi_major_axis, eccentricity, inclination, longitude_ascending_node, argument_perihelion, mean_anomaly):
    trajectory = { "x": [], "y": [], "z": [] }
    for i in range(181):
        point = get_asteroid_position(semi_major_axis, eccentricity, inclination, longitude_ascending_node, argument_perihelion, mean_anomaly, (2 * i) % 360)
        trajectory["x"].append(point[0])
        trajectory["y"].append(point[1])
        trajectory["z"].append(point[2])
    return trajectory
