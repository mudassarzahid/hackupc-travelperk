from sqlalchemy import create_engine, text


class Database:
    def __init__(self):
        connection_string = (
            "postgresql://{user}:{password}@{host}:{port}/{dbname}".format(
                user="postgres.dktoepfshpjofqehfvlx",
                password="S$Rkc7fdtL,-$p!",
                host="aws-0-eu-central-1.pooler.supabase.com",
                port=5432,
                dbname="postgres",
            )
        )
        self.engine = create_engine(connection_string)

    def execute_query(self, query, params=None):
        with self.engine.connect() as connection:
            if params:
                res = connection.execute(text(query), parameters=params)
            else:
                res = connection.execute(text(query))
            result_dicts = [row._asdict() for row in res.fetchall()]
            connection.commit()

            return result_dicts

    def execute_dml_query(self, query, params=None):
        with self.engine.connect() as connection:
            if params:
                connection.execute(text(query), parameters=params)
            else:
                connection.execute(text(query))
            connection.commit()

            return None
