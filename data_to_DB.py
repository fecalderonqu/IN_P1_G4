import psycopg2
import pandas as pd

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'auser',
    'password': 'Practica1_g4',
    'dbname': 'postgres'
}
DB_ANOMALIAS = 'postgres'
CSV_PATH = ['/Users/fernandocalderon05/Escritorio2/UIDE/MAESTRIA/4. INTELIGENCIA DE NEGOCIOS/PRACTICA 1/Practica1_G4/IN_P1_G4/dataset/population_data.csv']
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

def crear_tabla(column_names, tabla='population'):
    columns_str = ', '.join([f'"{col}" VARCHAR(100)' for col in column_names])
    sql = f"CREATE TABLE IF NOT EXISTS {tabla} (id SERIAL PRIMARY KEY,{columns_str});"
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                conn.commit()
        print("✅ Tabla creada.")
    except Exception as e:
        print(f"❌ Error al crear la tabla: {e}")


def consulta_a_dataframe(query, params=None):
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            df = pd.read_sql_query(query, conn, params=params)
        print("✅ Consulta ejecutada con éxito.")
        return df
    except Exception as e:
        print(f"❌ Error al ejecutar consulta: {e}")
        return pd.DataFrame()  # retorna vacío si falla


def insertar_registros(data, tabla='population'):
    try:
        # Columnas entre comillas dobles si tienen espacios o mayúsculas
        columnas = ', '.join([f'"{col}"' for col in data.columns])
        placeholders = ', '.join(['%s'] * len(data.columns))
        sql = f"INSERT INTO {tabla} ({columnas}) VALUES ({placeholders});"
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                for row in data.itertuples(index=False, name=None):
                    cur.execute(sql, row)
            conn.commit()

        print(f"✅ Insertados {len(data)} registros.")

    except Exception as e:
        print(f"❌ Error al insertar dato: {e}")



def main():
    try:
        verificar_conexion()

        print("⏳ Leyendo archivo CSV...")
        for csv_path in CSV_PATH:
            df = pd.read_csv(csv_path, delimiter=',', encoding='utf-8')
            column_names = df.columns.tolist()
            crear_tabla(column_names)
            insertar_registros(df)

        ## pueden crear varios df en base a la consulta que deseen hacer por ejemplo: df1
        df1 = consulta_a_dataframe("SELECT * FROM population LIMIT 5;")
        df1.drop(columns=['Unnamed: 62'], inplace=True)


        print("⏳ Insertando registros en la base de datos...")
    except Exception as e:
        print(f"❌ Error en el proceso principal: {e}")

if __name__ == '__main__':
    main()
