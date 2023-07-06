import traceback
from util.db_conn import Db_Connection
import pandas as pd

def cargar_empleado():
    try:
        type = 'mysql'
        host = '127.0.0.1'
        port = '3306'
        user = 'root'
        pwd = '1234'
        # Conexión con el staging para la tabla ext_category
        db_stg = 'stg_proyecto'
        # Conexión con el sor
        db_sor = 'sor_proyecto'

        # Conexión a la base de datos de origen (stg_proyecto)
        con_db_stg = Db_Connection(type, host, port, user, pwd, db_stg)
        ses_db_stg = con_db_stg.start()
        if ses_db_stg == -1:
            raise Exception("El tipo de base de datos " + type + " no es válido")
        elif ses_db_stg == -2:
            raise Exception("Error al establecer la conexión de pruebas")

        # Conexión a la base de datos de destino (sor_proyecto)
        con_db_sor = Db_Connection(type, host, port, user, pwd, db_sor)
        ses_db_sor = con_db_sor.start()
        if ses_db_sor == -1:
            raise Exception("El tipo de base de datos " + type + " no es válido")
        elif ses_db_sor == -2:
            raise Exception("Error al establecer la conexión de pruebas")

        # Consulta para obtener los datos de la tabla de extracción (ext_tipo_contrato)
        consulta_ext_empleado = "SELECT empleadoID, contratoID, nombre, cargo, sueldo, nivelK, pais FROM ext_empleado"
        df_ext_empleado = pd.read_sql(consulta_ext_empleado, con=ses_db_stg)

        # Crear una tabla temporal en la base de datos de destino
        create_temp_table = """
        CREATE TEMPORARY TABLE temp_ext_empleado AS (
            SELECT empleadoID, contratoID, nombre, cargo, sueldo, nivelK, pais
            FROM dim_empleado
        )
        """
        # Actualizar los registros existentes en la tabla de dimensión (TipoContrato)
        update_query = """
        UPDATE dim_empleado AS tc
        JOIN temp_ext_empleado AS etc ON tc.empleadoID = etc.empleadoID
        SET tc.contratoID = etc.contratoID,
            tc.nombre = etc.nombre, 
            tc.cargo = etc.cargo,
            tc.sueldo = etc.sueldo,
            tc.nivelK = etc.nivelK,
            tc.pais = etc.pais         
        """
        # Insertar registros nuevos en la tabla de dimensión (TipoContrato)
        insert_query = """
        INSERT INTO dim_empleado (empleadoID, contratoID, nombre, cargo, sueldo, nivelK, pais)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        # Ejecutar las consultas de actualización e inserción
        with ses_db_sor.begin() as conn:
            # Crear la tabla temporal
            conn.execute(create_temp_table)

            # Actualizar los registros existentes
            conn.execute(update_query)

            # Convertir el DataFrame a una lista de diccionarios
            records = df_ext_empleado.to_dict(orient='records')

            # Insertar registros nuevos
            for record in records:
                values = list(record.values())
                conn.execute(insert_query, values)

                
    except:
        traceback.print_exc()
    finally:
        con_db_stg.stop()
        con_db_sor.stop()

