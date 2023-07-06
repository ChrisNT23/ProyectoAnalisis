import traceback
import pandas as pd
import mysql.connector
import traceback
from util.db_conn import Db_Connection
import pandas as pd

def ext_per() :
    tablas = ["Usuario","TipoPermiso","TipoContrato","Subsidiaria", "Proyecto", "PermisoProcesado", "Permiso", "MarcadorHoras", "Empleado", "Contrato", "CentroCostos"]

    for tabla in tablas:
        try:
            type= 'mysql'
            host = '192.168.100.53'
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
            
            datos = pd.read_sql(f'SELECT * FROM {tabla}',ses_db_trx)


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

            print(datos.head())        
        
            datos.to_sql(f'ext_{tabla.lower()}', ses_db_stg, if_exists='replace', index=False)

        except:
            traceback.print_exc()
        finally:
            pass


        