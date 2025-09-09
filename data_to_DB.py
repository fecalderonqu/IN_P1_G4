import psycopg2
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'auser',
    'password': 'Practica1_g4',
    'dbname': 'postgres'
}
DB_ANOMALIAS = 'postgres'
CSV_PATH = '/Users/fernandocalderon05/Escritorio2/UIDE/MAESTRIA/4. INTELIGENCIA DE NEGOCIOS/PRACTICA 1/Practica1_G4/IN_P1_G4/dataset/population_data.csv'
BATCH_SIZE = 10
MAX_WORKERS = 10


def verificar_conexion():
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                _ = cur.fetchone()
        print("✅ Conexión exitosa a PostgreSQL.")
    except Exception as e:
        print(f"❌ Error al conectar: {e}")

def insertar_filas_en_bloque(df):
    try:
        for i in range(0, len(df), BATCH_SIZE):
            bloque = df.iloc[i:i + BATCH_SIZE][['id_usario', 'cluster']]
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                executor.map(insertar_registro, [row for _, row in bloque.iterrows()])
    except Exception as e:
        print(f"❌ Error al insertar registros por bloques: {e}")


def main():
    try:
        verificar_conexion()

        print("⏳ Leyendo archivo CSV...")
        df = pd.read_csv(CSV_PATH, delimiter=',', encoding='utf-8')

        print("⏳ Insertando registros en la base de datos...")
        insertar_filas_en_bloque(df)

        print("✅ Inserción con batch completada.")
    except Exception as e:
        print(f"❌ Error en el proceso principal: {e}")


if __name__ == '__main__':
    main()
