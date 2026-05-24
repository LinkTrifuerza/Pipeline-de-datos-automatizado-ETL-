import pandas as pd
from conexiones import extraer_ventas, extraer_usuarios
from limpieza_datos import ejecutar_limpieza 
from analitica_visualizacion import ejecutar_analitica 

def main():
    # Credenciales de la base de datos
    postgres_user = "postgres"
    postgres_password = "3232"
    postgres_host = "localhost"
    postgres_port = "5432"
    postgres_db = "proyecto_programacion"

    # Extrae las ventas de la base de datos PostgreSQL
    ventas = extraer_ventas(postgres_user, postgres_password, postgres_host, 
                            postgres_port, postgres_db)

    # Extrae los usuarios del archivo JSON y los hace tabla
    usuarios = extraer_usuarios()
    df_usuarios = pd.DataFrame(usuarios)
    
    # Limpia nulos, duplicados y genera 'datos_fase_limpieza.csv'
    ejecutar_limpieza(ventas, df_usuarios)

    # Calcula variables, corre el PCA y genera las 3 gráficas
    ejecutar_analitica()

if __name__ == "__main__":
    main()