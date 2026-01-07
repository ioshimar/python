import pandas as pd
import psycopg2

# Conectar a la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname="postgis_33_sample",
    user="postgres",
    password="root",
    host="localhost",
    port="5432"
)

# Ruta del archivo Excel
excel_file_path = "D:/RESPALDO/PRUEBAS_CURT/clasi_tipo_roca.xlsx"

# Leer datos desde el archivo Excel
df_excel = pd.read_excel(excel_file_path)

# Crear un cursor para ejecutar consultas
cur = conn.cursor()

# Ejemplo de consulta de actualización con parámetros
consulta_sql = "UPDATE public.unidad_de_roca SET descripcion = %s WHERE tipo = %s;"

# Utilizar parámetros en la consulta SQL para cada fila del DataFrame
for index, row in df_excel.iterrows():
    valor_excel_A1 = row[0]  # Valor en la primera columna (celda A)
    valor_excel_B1 = row[1]  # Valor en la segunda columna (celda B)

    # Escapar caracteres problemáticos en el valor de tipo
    valor_excel_A1 = valor_excel_A1.replace("'", "''")  # Duplicar comillas simples

    cur.execute(consulta_sql, (valor_excel_B1, valor_excel_A1))

# Confirmar los cambios y cerrar la conexión
conn.commit()
cur.close()
conn.close()

# Añadir un mensaje de finalización
print("Proceso completado. Las actualizaciones han sido aplicadas en la base de datos.")