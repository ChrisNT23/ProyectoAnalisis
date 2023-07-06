import traceback
from util.db_conn import Db_Connection
import pandas as pd

def cargar_marcadorhoras():
    try:
        type = 'mysql'
        host = '127.0.0.1'
        port = '3306'
        user = 'root'
        pwd = '1234'
        db_stg = 'stg_proyecto'
        db_sor = 'sor_proyecto'

        con_db_stg = Db_Connection(type, host, port, user, pwd, db_stg)
        ses_db_stg = con_db_stg.start()
        if ses_db_stg == -1:
            raise Exception("El tipo de base de datos " + type + " no es válido")
        elif ses_db_stg == -2:
            raise Exception("Error al establecer la conexión de pruebas")

        con_db_sor = Db_Connection(type, host, port, user, pwd, db_sor)
        ses_db_sor = con_db_sor.start()
        if ses_db_sor == -1:
            raise Exception("El tipo de base de datos " + type + " no es válido")
        elif ses_db_sor == -2:
            raise Exception("Error al establecer la conexión de pruebas")


        consulta_ext_marcadorhoras = "SELECT marcadorHorasID, empleadoID, proyectoID, fecha, cantidadHoras FROM ext_marcadorhoras"
        df_ext_marcadorhoras = pd.read_sql(consulta_ext_marcadorhoras, con=ses_db_stg)

        create_temp_table = """
        CREATE TEMPORARY TABLE temp_ext_marcadorhoras AS (
            SELECT marcadorHorasID, empleadoID, proyectoID, fecha, cantidadHoras
            FROM dim_marcadorhoras
        )
        """
        update_query = """
        UPDATE dim_marcadorhoras AS mh
        JOIN temp_ext_marcadorhoras AS emh ON mh.marcadorHorasID = emh.marcadorHorasID
        SET mh.empleadoID = emh.empleadoID,
            mh.proyectoID = emh.proyectoID,
            mh.fecha = emh.fecha,
            mh.cantidadHoras = emh.cantidadHoras
        """
        insert_query = """
        INSERT INTO dim_marcadorhoras (marcadorHorasID, empleadoID, proyectoID, fecha, cantidadHoras)
        VALUES (%s, %s, %s, %s, %s)
        """

        with ses_db_sor.begin() as conn:
            conn.execute(create_temp_table)
            conn.execute(update_query)

            records = df_ext_marcadorhoras.to_dict(orient='records')

            for record in records:
                values = list(record.values())
                conn.execute(insert_query, values)
                
    except:
        traceback.print_exc()
    finally:
        con_db_stg.stop()
        con_db_sor.stop()
