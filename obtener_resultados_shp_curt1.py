import geopandas as gpd
from sqlalchemy import create_engine, text
import psycopg2
import pandas as pd

def list_pendientes_tables(engine):
    query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name LIKE 'pendientes_%';
    """
    pendientes_tables = pd.read_sql_query(text(query), con=engine)
    return pendientes_tables['table_name'].tolist()

def load_all_pendientes(engine, pendientes_tables):
    pendientes_list = []
    for table in pendientes_tables:
        try:
            print(f"Cargando la tabla '{table}'...")
            query = f'SELECT "Id", geometry FROM {table};'
            df = gpd.read_postgis(text(query), con=engine, geom_col='geometry')
            pendientes_list.append(df)
            print(f"Tabla '{table}' cargada con {len(df)} registros.")
        except Exception as e:
            print(f"Error al cargar la tabla '{table}': {e}")
    if pendientes_list:
        pendientes_union = pd.concat(pendientes_list, ignore_index=True)
        pendientes_union = gpd.GeoDataFrame(pendientes_union)
        pendientes_union.crs = pendientes_list[0].crs
        print(f"Total de pendientes unificadas: {len(pendientes_union)}")
        return pendientes_union
    else:
        print("No se pudieron cargar tablas de pendientes.")
        return None

def load_tierras(engine):
    try:
        print("Cargando la tabla 'tierras_uso_comun'...")
        query = "SELECT id, geom FROM tierras_uso_comun;"
        tierras = gpd.read_postgis(text(query), con=engine, geom_col='geom')
        print(f"Tabla 'tierras_uso_comun' cargada con {len(tierras)} registros.")
        return tierras
    except Exception as e:
        print(f"Error al cargar la tabla 'tierras_uso_comun': {e}")
        return None

def perform_spatial_join(pendientes_union, tierras):
    try:
        print("Verificando y alineando los CRS...")
        if pendientes_union.crs != tierras.crs:
            print("Transformando 'pendientes_union' al CRS de 'tierras_uso_comun'...")
            pendientes_union = pendientes_union.to_crs(tierras.crs)
            print("Transformación de CRS completada.")
        else:
            print("Ambos GeoDataFrames tienen el mismo CRS.")
        
        print("Realizando la unión espacial para identificar pendientes dentro de cada tierra...")
        joined = gpd.sjoin(pendientes_union, tierras, how='inner', predicate='within')
        print(f"Pendientes asociadas a tierras: {len(joined)}")
        
        if joined.empty:
            print("No se encontraron pendientes dentro de ninguna tierra.")
            return None
        
        print("Agrupando pendientes por tierra y agregando los IDs...")
        pendientes_agrupadas = joined.groupby('id_right')['Id'].apply(lambda x: ','.join(x.astype(str))).reset_index()
        pendientes_agrupadas.rename(columns={'id_right': 'id', 'Id': 'pendientes_incluidas'}, inplace=True)
        print("Agrupación completada.")
        
        return pendientes_agrupadas
    except Exception as e:
        print(f"Error durante la unión espacial: {e}")
        return None

def update_tierras(engine, pendientes_agrupadas):
    try:
        print("Actualizando la tabla 'tierras_uso_comun' con los pendientes incluidos...")
        conn = psycopg2.connect(
            dbname=engine.url.database,
            user=engine.url.username,
            password=engine.url.password,
            host=engine.url.host,
            port=engine.url.port
        )
        cursor = conn.cursor()
        for index, row in pendientes_agrupadas.iterrows():
            tierras_id = row['id']
            pendientes = row['pendientes_incluidas']
            cursor.execute("""
                UPDATE tierras_uso_comun
                SET pendientes_incluidas = %s
                WHERE id = %s;
            """, (pendientes, tierras_id))
        conn.commit()
        print("Tabla 'tierras_uso_comun' actualizada exitosamente.")
    except Exception as e:
        print(f"Error al actualizar la tabla 'tierras_uso_comun': {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("Conexión a la base de datos cerrada.")

def main():
    try:
        # Parámetros de conexión
        user = 'postgres'
        password = 'root'
        host = 'localhost'
        port = '5432'
        database = 'postgis_33_sample'
        
        # Crear la cadena de conexión
        conn_str = f'postgresql://{user}:{password}@{host}:{port}/{database}'
        print("Estableciendo conexión con la base de datos PostgreSQL...")
        
        # Crear el motor de SQLAlchemy
        engine = create_engine(conn_str)
        
        # Listar todas las tablas de pendientes
        print("Listando todas las tablas de pendientes...")
        pendientes_tables = list_pendientes_tables(engine)
        print(f"Tablas de pendientes encontradas: {pendientes_tables}")
        
        if not pendientes_tables:
            print("No se encontraron tablas que comiencen con 'pendientes_'.")
            return
        
        # Cargar todas las tablas de pendientes y unificarlas
        pendientes_union = load_all_pendientes(engine, pendientes_tables)
        
        if pendientes_union is not None:
            # Verificar que sean 32 pendientes
            if len(pendientes_union) == 32:
                print("Se han cargado 32 pendientes correctamente.")
            else:
                print(f"Advertencia: Se han cargado {len(pendientes_union)} pendientes, se esperaban 32.")
            print(pendientes_union.head())
        else:
            print("No se pudo unificar ninguna tabla de pendientes.")
        
        # Cargar la tabla tierras_uso_comun
        tierras = load_tierras(engine)
        
        if tierras is None or tierras.empty:
            print("No se pudo cargar la tabla 'tierras_uso_comun'.")
            return
        
        # Realizar la unión espacial y obtener pendientes agrupadas
        pendientes_agrupadas = perform_spatial_join(pendientes_union, tierras)
        
        if pendientes_agrupadas is None or pendientes_agrupadas.empty:
            print("No hay pendientes para actualizar en 'tierras_uso_comun'.")
            return
        
        # Actualizar la tabla tierras_uso_comun con las pendientes agrupadas
        update_tierras(engine, pendientes_agrupadas)
        
    except Exception as e:
        print(f"Error general: {e}")

# Ejecutar la función principal
main()
