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

def load_all_pendientes_union(engine, pendientes_tables):
    try:
        print("Cargando todas las tablas 'pendientes_*' en una sola consulta...")
        # Construir la consulta UNION ALL
        union_queries = [f'SELECT "Id", "porcentaje", geometry FROM {table}' for table in pendientes_tables]
        union_all_query = " UNION ALL ".join(union_queries)
        
        # Leer todos los pendientes en un solo GeoDataFrame
        pendientes_union = gpd.read_postgis(text(union_all_query), con=engine, geom_col='geometry')
        print(f"Total de pendientes unificadas: {len(pendientes_union)}")
        return pendientes_union
    except Exception as e:
        print(f"Error al cargar las tablas 'pendientes_*': {e}")
        return None

def add_pendientes_field(engine):
    try:
        print("Agregando el campo 'pendientes' a 'tierras_uso_comun' si no existe...")
        with engine.connect() as conn:
            conn.execute(text("""
                ALTER TABLE tierras_uso_comun
                ADD COLUMN IF NOT EXISTS pendientes TEXT;
            """))
        print("Campo 'pendientes' asegurado en 'tierras_uso_comun'.")
    except Exception as e:
        print(f"Error al agregar el campo 'pendientes': {e}")

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
        
        print("Agrupando porcentajes únicos por tierra y agregando los valores...")
        pendientes_agrupadas = joined.groupby('id_right')['porcentaje'].apply(lambda x: ','.join(x.dropna().astype(str).unique())).reset_index()
        pendientes_agrupadas.rename(columns={'id_right': 'id', 'porcentaje': 'pendientes'}, inplace=True)
        print("Agrupación completada.")
        
        return pendientes_agrupadas
    except Exception as e:
        print(f"Error durante la unión espacial: {e}")
        return None

def update_tierras(engine, pendientes_agrupadas):
    try:
        print("Actualizando la tabla 'tierras_uso_comun' con los porcentajes de pendientes incluidos...")
        with engine.connect() as conn:
            for index, row in pendientes_agrupadas.iterrows():
                tierras_id = row['id']
                pendientes = row['pendientes']
                conn.execute(text("""
                    UPDATE tierras_uso_comun
                    SET pendientes = :pendientes
                    WHERE id = :id;
                """), {'pendientes': pendientes, 'id': tierras_id})
        print("Tabla 'tierras_uso_comun' actualizada exitosamente.")
    except Exception as e:
        print(f"Error al actualizar la tabla 'tierras_uso_comun': {e}")

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
        
        # Agregar el campo 'pendientes' en 'tierras_uso_comun'
        add_pendientes_field(engine)
        
        # Listar todas las tablas de pendientes
        print("Listando todas las tablas de pendientes...")
        pendientes_tables = list_pendientes_tables(engine)
        print(f"Tablas de pendientes encontradas: {pendientes_tables}")
        
        if not pendientes_tables:
            print("No se encontraron tablas que comiencen con 'pendientes_'.")
            return
        
        # Cargar todas las tablas de pendientes y unificarlas
        pendientes_union = load_all_pendientes_union(engine, pendientes_tables)
        
        if pendientes_union is not None:
            # Verificar que sean 32 pendientes
            if len(pendientes_union) == 32:
                print("Se han cargado 32 pendientes correctamente.")
            else:
                print(f"Advertencia: Se han cargado {len(pendientes_union)} pendientes, se esperaban 32.")
            print(pendientes_union.head())
        else:
            print("No se pudo unificar ninguna tabla de pendientes.")
            return
        
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
