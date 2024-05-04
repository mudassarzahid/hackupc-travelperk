import random
import time

from sqlalchemy import create_engine, text

connection_string = "postgresql://{user}:{password}@{host}:{port}/{dbname}".format(
    user="postgres.dktoepfshpjofqehfvlx",
    password="S$Rkc7fdtL,-$p!",
    host="aws-0-eu-central-1.pooler.supabase.com",
    port=5432,
    dbname="postgres",
)

engine = create_engine(connection_string)
for i in range(1, 900):
    set_stmt = f"""
    update dataset set acousticness = {round(random.uniform(0, 1), 3)} where trip_id = {i};
    update dataset set danceability = {round(random.uniform(0, 1), 3)} where trip_id = {i};
    update dataset set energy = {round(random.uniform(0, 1), 3)} where trip_id = {i};
    update dataset set key = {round(random.uniform(0, 1), 3)} where trip_id = {i};
    update dataset set loudness = {round(random.uniform(0, 1), 3)} where trip_id = {i};
    update dataset set mode = {round(random.uniform(0, 1), 3)} where trip_id = {i};
    update dataset set speechiness = {round(random.uniform(0, 1), 3)} where trip_id = {i};
    update dataset set instrumentalness = {round(random.uniform(0, 1), 3)} where trip_id = {i};
    update dataset set liveness = {round(random.uniform(0, 1), 3)} where trip_id = {i};
    update dataset set valence = {round(random.uniform(0, 1), 3)} where trip_id = {i};
    update dataset set tempo = {round(random.uniform(0, 1), 3)} where trip_id = {i};
    update dataset set duration_ms = {round(random.uniform(0, 1), 3)} where trip_id = {i};
    update dataset set time_signature = {round(random.uniform(0, 1), 3)} where trip_id = {i};
    """

    with engine.connect() as connection:
        connection.execute(text(set_stmt))
        connection.commit()

    time.sleep(1)
