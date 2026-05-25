import pandas as pd
from thefuzz import process

def ejecutar_limpieza(df_ventas, df_usuarios):
    print("\n" + "="*50)
    print("Iniciando fase de limpieza")
    print("="*50)

    # 1. Extracción del Archivo Plano (Inventario)
    print("\n Cargando archivo plano")
    df_inventario = pd.read_csv("INVENTARIO.csv")
    print(f"Se cargó inventario.csv con {df_inventario.shape[0]} filas.")

    # 2. Detectar y corregir nulos
    nulos_detectados = df_inventario.isna().sum().sum()
    print(f"\n Detectando valores nulos: {nulos_detectados}")
    df_inventario_limpio = df_inventario.fillna(0) 

    # 3. Eliminar duplicados en Ventas
    df_ventas_limpio = df_ventas.drop_duplicates(subset=["id_transaccion"])
    
    # 4. Limpieza y estradarizacion de ciudades y estados
    # --- Aplanamiento de JSON ---
    if 'localizacion' in df_usuarios.columns:
        print("\n Aplanando estructura de localización...")
        loc_df = pd.json_normalize(df_usuarios['localizacion'])
        loc_df.columns = ['ciudad', 'estado']
        df_usuarios = pd.concat([df_usuarios.drop(columns=['localizacion']), loc_df], axis=1)

# --- Definición de función de limpieza ---
    def aplicar_fuzzy(df, col, ref):
        if col in df.columns:
            # Añadimos .strip() justo después de str(x) para remover espacios vacíos
            df[col] = df[col].apply(lambda x: process.extractOne(str(x).strip(), ref)[0] 
                                    if process.extractOne(str(x).strip(), ref)[1] >= 80 else str(x).strip())
            print(f"Columna '{col}' normalizada.")

    # Catálogos maestros
    cat_estados = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", "Chihuahua", "Ciudad de México", "Coahuila", "Colima", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "Estado de México", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"]
    cat_capitales = ["Aguascalientes", "Mexicali", "La Paz", "Campeche", "Tuxtla Gutiérrez", "Chihuahua", "Ciudad de México", "Saltillo", "Colima", "Durango", "Guanajuato", "Chilpancingo", "Pachuca", "Guadalajara", "Toluca", "Morelia", "Cuernavaca", "Tepic", "Monterrey", "Oaxaca", "Puebla", "Querétaro", "Chetumal", "San Luis Potosí", "Culiacán", "Hermosillo", "Villahermosa", "Ciudad Victoria", "Tlaxcala", "Xalapa", "Mérida", "Zacatecas"]

    # Ejecución de la limpieza
    print(f"\n Normalizando de localizacion")
    aplicar_fuzzy(df_usuarios, 'estado', cat_estados)
    aplicar_fuzzy(df_usuarios, 'ciudad', cat_capitales)

    # 5. Enriquecimiento
    print(f"\n Aplicando Pandas Left Join")
    df_master_limpio = pd.merge(df_ventas_limpio, df_usuarios, on="id_cliente", how="left")
    
    df_master_limpio.to_csv("datos_fase_limpieza.csv", index=False)
    print("\n Archivo 'datos_fase_limpieza.csv' exportado con éxito.")
    
    return df_master_limpio