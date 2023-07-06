import traceback
import pandas as pd
import mysql.connector
import traceback
from util.db_conn import Db_Connection
import pandas as pd


def extraer_usuario():
    try:
        type= 'mysql'
        host = '192.168.0.101'
        port = '3306'
        user = 'ADMIN'
        pwd = ''
        db = 'proyecto'

        con_db_trx = Db_Connection(type, host, port, user, pwd, db)
        ses_db_trx = con_db_trx.start()
        if ses_db_trx == -1:
            raise Exception("El tipo de base de datos " + type + " no es válido")
        elif ses_db_trx == -2:
            raise Exception("Error al establecer la conexión de pruebas")        
        
        usuarios = pd.read_sql('SELECT * FROM Usuario',ses_db_trx)

        return usuarios
    

        
    except:
        traceback.print_exc()
    finally:
        pass

     
