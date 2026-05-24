import pandas as pd 
from sqlalchemy import create_engine
import json 

#Extraccion Ventas_historicas
def extraer_ventas(user, password, host, port, db):

    engine_postgres=create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")

    
    query="SELECT * FROM ventas_historicas"

    df_ventas=pd.read_sql(query, engine_postgres)
    return(df_ventas)

def extraer_usuarios():
    
    #Lee el archivo json local con los perfiles de clientes
    with open("perfiles_usuario.json", "r", encoding="utf8") as usuarios:
        datos=json.load(usuarios)
    return datos

