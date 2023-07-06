
import requests
import traceback

def convertir_divisas(cantidad, moneda_origen, moneda_destino):
    api_key = '9d28c1643b914d996415fb45'    # Reemplaza 'TU_API_KEY' con tu clave de API

    url = f'https://v6.exchangerate-api.com/v6/{api_key}/pair/{moneda_origen}/{moneda_destino}/{cantidad}'

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            resultado = data['conversion_result']
            return resultado
        else:
            return cantidad
    except requests.exceptions.RequestException as e:
        return cantidad


import requests
import traceback
from util.db_conn import Db_Connection

# Resto del código omitido por simplicidad

def tran_empleado():
    try:
        type = 'mysql'
        host = '127.0.0.1'
        port = '3306'
        user = 'root'
        pwd = '1234'
        # Conexión con el sor
        db_sor = 'sor_proyecto'

        # Conexión a la base de datos de destino (sor_proyecto)
        con_db_sor = Db_Connection(type, host, port, user, pwd, db_sor)
        ses_db_sor = con_db_sor.start()
        if ses_db_sor == -1:
            raise Exception("El tipo de base de datos " + type + " no es válido")
        elif ses_db_sor == -2:
            raise Exception("Error al establecer la conexión de pruebas")

        
        with ses_db_sor.begin() as trans:
            # Comprueba si la columna ya existe en la tabla
            check_column_query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND COLUMN_NAME = %s"
           
            result = trans.execute(check_column_query, (db_sor, 'dim_empleado', 'sueldoDolar')).fetchone()

            if not result:
                # Agregar una nueva columna a la tabla empleado
                alter_table_query = "ALTER TABLE dim_empleado ADD COLUMN sueldoDolar DECIMAL(10, 2)"
                trans.execute(alter_table_query)

            # Obtener los registros de la tabla empleado
            select_query = "SELECT empleadoID, sueldo FROM dim_empleado"
            result = trans.execute(select_query).fetchall()

            # Actualizar los valores de la columna sueldoDolar
            update_query = "UPDATE dim_empleado SET sueldoDolar = %s WHERE empleadoID = %s"
            for row in result:
                # Realizar la consulta del tipo de moneda en que se le paga por contrato
                # Realizar la consulta a la tabla contrato
                select_query = "SELECT monedaPago FROM dim_contrato WHERE contratoID = %s"
                result = trans.execute(select_query, (row[0],)).fetchone()

                # Verificar si se encontró un resultado
                moneda_pago = "USD"
                if result:
                    moneda_pago = result[0]

                # Aquí hay que mandar los datos a la API
                print("sueldo actual row[1]:", row[1])
                print("moneda_pago:", moneda_pago)
                nuevo_sueldo = convertir_divisas(row[1], moneda_pago, "USD")
                sueldo_dolar = nuevo_sueldo  # Multiplicar el sueldo por 2
                empleado_id = row[0]
                trans.execute(update_query, (sueldo_dolar, empleado_id))

    except:
        traceback.print_exc()
    finally:
        con_db_sor.stop()
