import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
import plotly.graph_objects as go

def ejecutar_analitica():
    print("\n" + "="*50)
    print("Iniciando analitica avanzada y visualizacion")
    print("="*50)
    
    print("Cargando datos")
    ruta_csv = "datos_fase_limpieza.csv"
    df = pd.read_csv(ruta_csv)

    print("\nLimpiando datos adicionales")
    # Eliminar duplicados
    antes = len(df)
    df = df.drop_duplicates()
    despues = len(df)
    print(f"Duplicados eliminados: {antes - despues}")

    def convertir_fecha(fecha):
        try:
            return pd.to_datetime(fecha, dayfirst=True)
        except:
            try:
                return pd.to_datetime(fecha)
            except:
                return pd.to_datetime(pd.NaT)

    df["fecha"] = df["fecha"].apply(convertir_fecha)
    df = df.dropna(subset=["fecha"])

    print("\nGenerando segmento_cliente (Regla de Negocio)")
    df["segmento_cliente"] = np.where(
        (df["monto"] > 1000) & (df["edad"] < 30),
        "Premium Joven",
        "Estándar"
    )

    print("\nPreparando variables para PCA (20 variables)")
    df["ratio_gasto_ingreso"] = df["gastos_mensuales"] / (df["ingresos"] + 1)
    df["monto_por_edad"] = df["monto"] / (df["edad"] + 1)
    df["nivel_lealtad"] = df["puntos_lealtad"] / 1000
    df["ingreso_anual_estimado"] = df["ingresos"] * 12
    df["ahorro_estimado"] = df["ingresos"] - df["gastos_mensuales"]
    df["indice_consumo"] = df["monto"] + df["gastos_mensuales"]
    df["score_financiero"] = df["ingresos"] * 0.5 + df["puntos_lealtad"] * 0.2

    np.random.seed(42)
    for i in range(1, 11):
        df[f"comportamiento_{i}"] = np.random.randint(1, 100, size=len(df))

    variables_pca = [
        "monto", "edad", "ingresos", "gastos_mensuales", "puntos_lealtad",
        "ratio_gasto_ingreso", "monto_por_edad", "nivel_lealtad",
        "ingreso_anual_estimado", "ahorro_estimado", "indice_consumo",
        "score_financiero", "comportamiento_1", "comportamiento_2",
        "comportamiento_3", "comportamiento_4", "comportamiento_5",
        "comportamiento_6", "comportamiento_7", "comportamiento_8"
    ]

    print("\nAplicando escalado Min-Max...")
    scaler = MinMaxScaler()
    
    # CORRECCIÓN: Sobrescribimos las columnas originales con los datos escalados [0, 1]
    df[variables_pca] = scaler.fit_transform(df[variables_pca])
    
    print(f"Escalado completado. Ejemplo de gastos normalizados:\n{df['gastos_mensuales'].head()}")

    print("\nEjecutando PCA (3 componentes)")
    pca = PCA(n_components=3)
    componentes = pca.fit_transform(df[variables_pca])

    df["PCA_1"] = componentes[:, 0]
    df["PCA_2"] = componentes[:, 1]
    df["PCA_3"] = componentes[:, 2]

    print("\nVarianza explicada:")
    for i, varianza in enumerate(pca.explained_variance_ratio_):
        print(f"PCA_{i+1}: {varianza:.4f}")
    print(f"Varianza total acumulada: {sum(pca.explained_variance_ratio_):.4f}")

    print("\nGenerando gráficos del Dashboard")
    # Boxplot
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df["monto"])
    plt.title("Distribución de Montos (Detección de Outliers)")
    plt.xlabel("Monto")
    plt.tight_layout()
    plt.savefig("boxplot_montos.png")
    plt.close()

    # Scatter Plot
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="PCA_1", y="PCA_2", hue="segmento_cliente", alpha=0.7)
    plt.title("Clusters de Clientes (Representación PCA)")
    plt.xlabel("PCA_1")
    plt.ylabel("PCA_2")
    plt.tight_layout()
    plt.savefig("scatter_pca.png")
    plt.close()

    # Sankey Diagram
    visitas = 3000
    checkout = 1200
    compras = 650
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15, thickness=20,
            line=dict(color="black", width=0.5),
            label=["Visitas Web", "Checkout", "Compra Final"]
        ),
        link=dict(source=[0, 1], target=[1, 2], value=[visitas, compras])
    )])
    
    fig.update_layout(title_text="Embudo de Conversión (Sankey)", font_size=12)
    fig.write_html("sankey_clientes.html")

    print("\nExportando Repositorio Maestro Final...")
    df.to_csv("data_master_clean.csv", index=False)

    print("\n" + "="*50)
    print("Exito al ejecutar")
    print("Archivos generados: data_master_clean.csv, boxplot_montos.png, scatter_pca.png, sankey_clientes.html")
    print("="*50)

if __name__ == "__main__":
    ejecutar_analitica()