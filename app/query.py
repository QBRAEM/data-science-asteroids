import math
import numpy as np
import pickle as pk
from google.cloud import bigquery
import os


def log_float_to_16bits(n):
    sign = -1 if n < 0 else 1
    return int(np.ushort(sign * int(np.log(abs(n)) * 1000)))


def get_asteroid_id_from_xyz(x, y, z):
    idX = "%04X" % log_float_to_16bits(x)
    idY = "%04X" % log_float_to_16bits(y)
    idZ = "%04X" % log_float_to_16bits(z)
    return idX + idY + idZ

def get_asteroid_id(asteroid):
    return get_asteroid_id_from_xyz(
        asteroid["x0"],
        asteroid["y0"],
        asteroid["z0"]
    )
    
    




def query_star():
    return {
        "name": "Soleil",
        "color": "#FFFF00",
        "diameter": 1392680,
    }



PLANETS = None
def query_planets():
    global PLANETS
    if PLANETS == None:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Administrateur\Desktop\Formation\projet\asteroids-335014-30ac06c837f2.json"
        client = bigquery.Client()
        table_id = client.project + ".dataset.planets"
        sql = "SELECT * FROM `" + table_id + "`;"
        PLANETS = client.query(sql).to_dataframe().to_dict('records')
        for planet in PLANETS:
            for coord in ["x", "y", "z"]:
                planet[coord] = eval(planet[coord])
                planet[coord][-1] = planet[coord][0]
    return PLANETS



ASTEROIDS = None
def query_asteroids(bounds, distMin, distMax, diameterMin, diameterMax, limit):
    global ASTEROIDS
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Administrateur\Desktop\Formation\projet\asteroids-335014-30ac06c837f2.json"
    client = bigquery.Client()
    table_id = client.project + ".dataset.asteroids_details"
    sql = \
        "SELECT * FROM `" + table_id + "` " + \
        "WHERE dist < " + str(bounds) + " " + \
        "AND dist < " + str(distMax) + " " + \
        "AND dist > " + str(distMin) + " " + \
        "AND diameter < " + str(diameterMax) + " " + \
        "AND diameter > " + str(diameterMin) + " " + \
        "ORDER BY RAND() " + \
        "LIMIT " + str(limit) + " ;"
    asteroids = client.query(sql).to_dataframe().to_dict('records')
    print("Loaded", len(asteroids), "asteroids.")
    ASTEROIDS = asteroids
    return asteroids


def get_asteroids():
    global ASTEROIDS
    return ASTEROIDS
    


def query_asteroid(n):
    return ASTEROIDS[n]
    
    

