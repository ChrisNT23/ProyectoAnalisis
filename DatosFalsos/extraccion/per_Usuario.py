import traceback
import pandas as pd
import mysql.connector
from util.db_conn import Db_Connection


def persistir_usuario(usuarios):
    try:
        type='mysql'
        host = '127.0.0.1'
        port = '3306'
        user = 'root'
        pwd = '1234'
        db = 'stg_proyecto'

        con_db_stg = Db_Connection(type, host, port, user, pwd, db)
        ses_db_stg= con_db_stg.start()
        if ses_db_stg == -1:
            raise Exception("El tipo de base de datos " + type + " no es válido")
        elif ses_db_stg == -2:
            raise Exception("Error al establecer la conexión de pruebas")        

       
        usuarios.to_sql('ext_usuario', ses_db_stg, if_exists='replace', index=False)

    except:
        traceback.print_exc()
    finally:
        pass