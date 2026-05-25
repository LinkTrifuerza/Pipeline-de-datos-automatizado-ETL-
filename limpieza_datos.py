import pandas as pd

def ejecutar_limpieza(df_ventas, df_usuarios):
    print("\n" + "="*50)
    print("Iniciando fase de limpieza")
    print("="*50)

    # 1. Extracción del Archivo Plano (Inventario)
    print("\n Cargando archivo plano")
    df_inventario = pd.read_csv("INVENTARIO.csv")
    print(f"Se cargó inventario.csv con {df_inventario.shape[0]} filas.")

    # 2. Detectar y corregir nulos en inventario.csv
    nulos_detectados = df_inventario.isna().sum().sum()
    print(f"\n Detectando valores nulos")
    print(f"Valores nulos detectados en Inventario: {nulos_detectados}")
    df_inventario_limpio = df_inventario.fillna(0) # Imputación de nulos con 0
    print("Valores nulos corregidos con éxito.")
    
    # Eliminar transacciones duplicadas en el SQL (Ventas)
    total_antes = df_ventas.shape[0]
    df_ventas_limpio = df_ventas.drop_duplicates(subset=["id_transaccion"])
    duplicados_eliminados = total_antes - df_ventas_limpio.shape[0]
    print(f"\n Eliminando duplicados de SQL")
    print(f"Transacciones duplicadas eliminadas en Ventas: {duplicados_eliminados}")
    
    # 4. Limpieza de strings en categorías
    print(f"\n Limpiando strings en categorías de Geolocalización")
    if 'geolocalizacion' in df_usuarios.columns:
        # Pasamos a minúsculas y quitamos espacios en blanco
        df_usuarios['geolocalizacion'] = df_usuarios['geolocalizacion'].str.lower().str.strip()
        # Estandarizamos las variaciones solicitadas ("mex", "mx" -> "México")
        df_usuarios['geolocalizacion'] = df_usuarios['geolocalizacion'].replace(['mex', 'mx', 'mexico'], 'México')
        print("Categorías geográficas estandarizadas homogéneamente.")

    # 5. Enriquecimiento mediante Left Join (Ventas SQL + Perfiles NoSQL)
    print(f"\n[ETL - Enriquecimiento] 4. Aplicando Pandas Left Join mediante llave id_cliente")
    df_master_limpio = pd.merge(df_ventas_limpio, df_usuarios, on="id_cliente", how="left")
    print(f"Dataset unificado, tamaño del repositorio: {df_master_limpio.shape[0]} filas.")
    
    # Guardamos el archivo final 
    df_master_limpio.to_csv("datos_fase_limpieza.csv", index=False)
    print("\n Archivo 'datos_fase_limpieza.csv' exportado con éxito para Analítica Avanzada.")
    print("="*50 + "\n")
    
    return df_master_limpio